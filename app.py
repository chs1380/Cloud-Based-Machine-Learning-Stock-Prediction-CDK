from aws_cdk import core
from cdk.vpc_construct.fyp_vpc import VPC_stack
from cdk.Database.Auroa_Serverless import Database_Stack
from cdk.ecs_cluster_construct.ecs_cluster_construct import ClusterConstruct
from cdk.Ecr_Commit.ecr_commit_repo import Ecr_Commit_Construct
from cdk.Pipline.Pipeline_Construct import PipleineConstruct
import os


app = core.App()
env_USA = core.Environment(account="169747529889", region="us-east-1")

vpc_construct = VPC_stack(
    app,
    "infraVpc",
    env=env_USA
)

database_construct = Database_Stack(
    app,
    "auroraDB",
    props=vpc_construct.vpc,
    env=env_USA
)

database_construct.add_dependency(vpc_construct)

docker_pipeline_construct= Ecr_Commit_Construct(
    app,
    "ECR-REPO",
)



pipeline_construct= PipleineConstruct(
    app,
    "CodePipelineFlask",
    env=core.Environment(region="us-east-1",account="169747529889"),
    props=vpc_construct.vpc

)



# route_53='pass'
# cloudfront='pass'
app.synth()
