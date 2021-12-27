import ntpath

from aws_cdk import (
    aws_codecommit as codecommit,
    aws_codepipeline as codepipeline,
    aws_codebuild as codebuild,
    aws_codedeploy as codedeploy,
    aws_codepipeline_actions as codepipeline_actions,
    aws_ecr as ecr,
    aws_iam as iam,
    core
)
from aws_cdk.aws_ecr_assets import DockerImageAsset

class DockerPipelineConstruct(core.Stack):
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

        asset=DockerImageAsset(self,"Flask_Docker_Image",
                               directory="")

