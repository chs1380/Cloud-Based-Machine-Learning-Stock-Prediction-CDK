from aws_cdk import core
from vpc_construct.fyp_vpc import VPC_stack
from Database.Auroa_Serverless import Database_Stack
from flux_cd.fluxcd_construct import  FluxcdConstruct
from eks_cluster_construct.eks_cluster_construct import ClusterConstruct
import os

git_auth_user = os.environ["GIT_AUTH_USER"]
git_auth_key = os.environ["GIT_AUTH_KEY"]


app = core.App()

name = app.node.try_get_context("name")
region = app.node.try_get_context("region")

aws_env = core.Environment(region=region)

stack = core.Stack(scope=app, env=aws_env, id=f"{name}-stack")

vpc_construct = VPC_stack(
    app,
    "infraVpc",
    env={'region': 'us-east-1',
         'account': '169747529889'}
)

database_construct = Database_Stack(
    app,
    "auroraDB",
    vpc_construct.vpc,
    env={'region': 'us-east-1',
         'account':'169747529889'}
)

database_construct.add_dependency(vpc_construct)

# kubernetes_cluster='pass'


cluster_construct = ClusterConstruct(
    scope=stack,
    id=f"{name}-cluster",
    cluster_name=f"{name}-cluster"
)


fluxcd_construct = FluxcdConstruct(
    scope=stack,
    id=f"{name}-fluxcd",
    git_user=git_auth_user,
    git_password=git_auth_key,
    eks_base_cluster=cluster_construct.cluster
)

# route_53='pass'

# cloudfront='pass'

# cicd_pipeline='pass'

app.synth()
