from aws_cdk import core
from cdk.vpc_construct.fyp_vpc import VPC_stack
from cdk.Database.Auroa_Serverless import Database_Stack
from cdk.eks_cluster_construct.eks_cluster_construct import ClusterConstruct
from cdk.docker_pipeline.docker_pipleine import DockerPipelineConstruct
import os


app = core.App()
vpc_construct = VPC_stack(
    app,
    "infraVpc",
    env={'region': 'us-east-1',
         'account': '169747529889'}
)

database_construct = Database_Stack(
    app,
    "auroraDB",
    props=vpc_construct.vpc,
    env={'region': 'us-east-1',
         'account': '169747529889'}
)

database_construct.add_dependency(vpc_construct)

docker_pipeline_construct= DockerPipelineConstruct(
    app,
    "ECR-REPO"
)

cluster_construct = ClusterConstruct(
    app,
    "ecs-fargate-cluster",
    props=vpc_construct.vpc,
    env={'region': 'us-east-1',
         'account': '169747529889'},
    repo=docker_pipeline_construct.container_repository
)

cluster_construct.node.add_dependency(vpc_construct)
cluster_construct.add_dependency(database_construct)



# route_53='pass'
# cloudfront='pass'
app.synth()
