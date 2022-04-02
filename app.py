from aws_cdk import core
from cdk.vpc_construct.fyp_vpc import VPC_stack
from cdk.Database.Auroa_Serverless import Database_Stack
from cdk.Pipline.Pipeline_Construct import PipleineConstruct
from cdk.Cloudfront.cloudfront_cache import cloudfront_dist
import os


app = core.App()
env = core.Environment(account="169747529889", region="ap-southeast-1")

vpc_construct = VPC_stack(
    app,
    "infraVpc",
    env=env
)

database_construct = Database_Stack(
    app,
    "auroraDB",
    props=vpc_construct.vpc,
    env=env
)

database_construct.add_dependency(vpc_construct)

pipeline_construct= PipleineConstruct(
    app,
    "CodePipelineFlask",
    env=env,
    props=vpc_construct.vpc

)
pipeline_construct.add_dependency(database_construct)

cloudfront= cloudfront_dist(
    app,
    "CloudFrontELB",
    env=env,
    props=pipeline_construct.load_balancer
)
cloudfront.add_dependency(pipeline_construct)
app.synth()
