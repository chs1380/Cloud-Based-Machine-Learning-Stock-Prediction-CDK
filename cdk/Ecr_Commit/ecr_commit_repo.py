import ntpath

from aws_cdk import (
    aws_codecommit as codecommit,
    aws_codepipeline as codepipeline,
    aws_codebuild as codebuild,
    aws_codedeploy as codedeploy,
    aws_codepipeline_actions as codepipeline_actions,
    aws_ecr as ecr,
    aws_ecs as ecs,
    aws_iam as iam,
    aws_ecr_assets as ecr_assets,
    core
)

from aws_cdk.aws_ecr_assets import DockerImageAsset



class Ecr_Commit_Construct(core.Stack):
    def __init__(
            self,
            scope: core.Construct,
            id: str,

    ) -> None:
        super().__init__(scope=scope, id=id)
        # ECR repositories
        self.container_repository = ecr.Repository(
            scope=self,
            id="containter_repo",
            repository_name="container_repo"
        )

        image_asset=ecr_assets.DockerImageAsset(self,"Flask_docker_image",
                                    directory="/home/ec2-user/environment/hkbu_fyp_website",
                                    repository_name="container_repo1")




        self.container_repository.ap
        # code commit repo
        self.codecommit_repo = codecommit.Repository(
            scope=self,
            id="flask-repo",
            repository_name="flask-repo",
            description="flask app and docker code"
        )


