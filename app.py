from aws_cdk import core
from cdk.vpc_construct.fyp_vpc import VPC_stack
from cdk.Database.Auroa_Serverless import Database_Stack
from cdk.Ecr_Commit.ecr_commit_repo import Ecr_Commit_Construct
from cdk.Pipline.Pipeline_Construct import PipleineConstruct
from cdk.Cloudfront.cloudfront_cache import cloudfront_dist
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

pipeline_construct= PipleineConstruct(
    app,
    "CodePipelineFlask",
    env=core.Environment(region="us-east-1",account="169747529889"),
    props=vpc_construct.vpc

)
pipeline_construct.add_dependency(database_construct)

cloudfront= cloudfront_dist(
    app,
    "CloudFrontELB",
    env=env_USA,
    props=pipeline_construct.load_balancer
)
cloudfront.add_dependency(pipeline_construct)
app.synth()
