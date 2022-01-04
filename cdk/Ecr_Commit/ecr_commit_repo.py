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
    core
)



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

        # code commit repo
        self.codecommit_repo = codecommit.Repository(
            scope=self,
            id="flask-repo",
            repository_name="flask-repo",
            description="flask app and docker code"
        )


