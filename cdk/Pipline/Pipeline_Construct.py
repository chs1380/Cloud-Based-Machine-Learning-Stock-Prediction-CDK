from aws_cdk import (
    aws_codecommit as codecommit,
    aws_codepipeline as codepipeline,
    aws_codebuild as codebuild,
    aws_codedeploy as codedeploy,
    aws_codepipeline_actions as codepipeline_actions,
    aws_ecr as ecr,
    aws_ecs as ecs,
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2,

    core
)


class PipleineConstruct(core.Stack):
    def __init__(
            self,
            scope: core.Construct,
            construct_id: str,
            props:ec2.Vpc,
            **kwargs

    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # Code Pipline
        pipeline = codepipeline.Pipeline(self, "Flask_App_Pipeline",
                                         pipeline_name="Flask_App_Pipeline"
                                         )

        source_output = codepipeline.Artifact(artifact_name="source_output")
        docker_output = codepipeline.Artifact(artifact_name="Docker")

        self.container_repository = ecr.Repository(
            scope=self,
            id="containter_repo",
            repository_name="container_repo"
        )

        # code commit repo
        self.codecommit_repo = codecommit.Repository(
            scope=self,
            id="flask-repo",
            repository_name="flask-repo",
            description="flask app and docker code"
        )




        get_source = codepipeline_actions.CodeCommitSourceAction(
            action_name="get_source_from_codeCommit",
            repository=self.codecommit_repo,
            output=source_output,
            branch="master"
        )

        # pipline add first stage get repo code.
        pipeline.add_stage(
            stage_name="Source",
            actions=[get_source]
        )

        # pipleine define build stage

        # defind docker build spec
        buildspec_docker = codebuild.BuildSpec.from_source_filename("buildspec.yml")

        # define action of build docker
        build_docker = codebuild.PipelineProject(
            self,
            "Build Docker",
            environment=dict(
                build_image=codebuild.LinuxBuildImage.AMAZON_LINUX_2_3,
                privileged=True),
            environment_variables={
                'REPO_ECR': codebuild.BuildEnvironmentVariable(
                    value=self.container_repository.repository_uri),
            },
            build_spec=buildspec_docker
        )
        # define role for building docker and grant push pull right to repo.

        build_docker.add_to_role_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["ecr:BatchCheckLayerAvailability", "ecr:GetDownloadUrlForLayer", "ecr:BatchGetImage"],
            resources=[
                f"arn:{core.Stack.of(self).partition}:ecr:{core.Stack.of(self).region}:{core.Stack.of(self).account}:repository/*"], ))

        self.container_repository.grant_pull_push(build_docker.role)

        # stage in pipeline

        pipeline.add_stage(
            stage_name="DockerBuild",
            actions=[
                codepipeline_actions.CodeBuildAction(
                    action_name="Build_docker_and_push_to_ECR",
                    project=build_docker,
                    input=source_output,
                    outputs=[docker_output])
            ]
        )

        # define deploy stage.
        application = codedeploy.EcsApplication(
            self,
            "FLASK_APPLICATION",
            application_name="FLASK_APPLICATION"
        )

        # create ecs cluster
        cluster = ecs.Cluster(self, "Cluster",
                              vpc=props
                              )

        # create task defintion
        task_definiton = ecs.FargateTaskDefinition(
            self, "TaskDef",
        )
        # task defintion policy
        task_definiton.add_to_task_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                resources=["*"],
                actions=[
                    "ecr:GetAuthorizationToken",
                    "ecr:BatchCheckLayerAvailability",
                    "ecr:GetDownloadUrlForLayer",
                    "ecr:BatchGetImage",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents"
                ]
            )
        )
        # create container
        task_definiton.add_container("WebContainer",
                                     image=ecs.ContainerImage.from_ecr_repository(
                                         self.container_repository),
                                     memory_limit_mib=512,
                                     cpu=256,
                                     port_mappings=[ecs.PortMapping(container_port=8000)]
                                     )
        # cluster Service
        self.cluster_service = ecs.FargateService(
            self,
            "ECS-FARGATE-SERVICE",
            cluster=cluster,
            task_definition=task_definiton,
            desired_count=2
        )

        scaling = self.cluster_service.auto_scale_task_count(max_capacity=6,
                                                             min_capacity=2)
        scaling.scale_on_cpu_utilization("cpu_scaling", target_utilization_percent=50)

        load_balancer = elbv2.ApplicationLoadBalancer(self, "LB_FOR_FARGATE",
                                                      vpc=props,
                                                      vpc_subnets={"subnet_type": ec2.SubnetType.PUBLIC},
                                                      internet_facing=True
                                                      )
        listener = load_balancer.add_listener("Listener", port=8000)
        listener.add_targets("ECS-FARGATE",
                             port=8000,
                             targets=[self.cluster_service])

        cfn_deployment_config = codedeploy.CfnDeploymentConfig(self, "MyCfnDeploymentConfig",
                                                               compute_platform="computePlatform",
                                                               deployment_config_name="deploymentConfigName",
                                                               minimum_healthy_hosts=codedeploy.CfnDeploymentConfig.MinimumHealthyHostsProperty(
                                                                   type="type",
                                                                   value=2
                                                               ),
                                                               traffic_routing_config=codedeploy.CfnDeploymentConfig.TrafficRoutingConfigProperty(
                                                                   type="type",
                                                                   # the properties below are optional
                                                                   time_based_canary=codedeploy.CfnDeploymentConfig.TimeBasedCanaryProperty(
                                                                       canary_interval=5,
                                                                       canary_percentage=20
                                                                                ),
                                                                        )
                                                               )

        ecs_deploymentGroup = codedeploy.EcsDeploymentGroup.from_ecs_deployment_group_attributes(self,
                                                                                                 "ecs_deployment_gorup",
                                                                                                 application=application,
                                                                                                 deployment_group_name="Fargate_Deployment_Group",
                                                                                                 deployment_config=cfn_deployment_config
                                                                                                 )
        pipeline.add_stage(
            stage_name="deploy_to_ecs",
            actions=[
                codepipeline_actions.EcsDeployAction(
                    action_name='Deploy_to_ECS',
                    service=self.cluster_service,
                    image_file=codepipeline.ArtifactPath(docker_output,"imagedefinitions.json"),
                )
            ]
        )
