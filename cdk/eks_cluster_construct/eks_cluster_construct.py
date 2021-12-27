from aws_cdk import (
    aws_ecs as ecs,
    aws_rds as rds,
    core,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_rds as rds,
    aws_elasticloadbalancingv2 as elbv2,
    aws_ecr as ecr
)


class ClusterConstruct(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, props: ec2.Vpc, repo: ecr.Repository,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # create ecs cluster
        cluster = ecs.Cluster(self, "Cluster",
                              vpc=props
                              )

        # create task defintion
        task_definiton = ecs.FargateTaskDefinition(
            self, "TaskDef"
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
                                          repo),
                                     memory_limit_mib=256,
                                     cpu=256,
                                     port_mappings=[ecs.PortMapping(container_port=8000)]
                                     )
        # cluster Service
        cluster_service = ecs.FargateService(
            self,
            "ECS-FARGATE-SERVICE",
            cluster=cluster,
            task_definition=task_definiton,
            desired_count=2
        )

        scaling = cluster_service.auto_scale_task_count(max_capacity=6,
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
                             targets=[cluster_service])
