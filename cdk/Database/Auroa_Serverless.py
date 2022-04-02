from aws_cdk import (aws_rds as rds,
                     aws_ec2 as ec2,
                     core
                     )
from cdk.vpc_construct.fyp_vpc import VPC_stack



class Database_Stack(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, props: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        auroa_sec_group = ec2.SecurityGroup(self, "AuroraSecurityGroup",
                                            vpc=props,
                                            description="Allow database access",
                                            allow_all_outbound=True)

        auroa_sec_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(3306), "allow mysql access")

        self.cluster = rds.ServerlessCluster(self, "AuroraCluster",
                                             engine=rds.DatabaseClusterEngine.AURORA_MYSQL,
                                             scaling=rds.ServerlessScalingOptions(
                                                 auto_pause=core.Duration.minutes(10),
                                                 # default is to pause after 10 minutes of idle time
                                                 min_capacity=rds.AuroraCapacityUnit.ACU_8,
                                                 # default is 2 Aurora capacity units (ACUs)
                                                 max_capacity=rds.AuroraCapacityUnit.ACU_32
                                             ),
                                             vpc=props,
                                             vpc_subnets={"subnet_type": ec2.SubnetType.PRIVATE},
                                             security_groups=[auroa_sec_group]
                                             )
        self.database_endpoint = self.cluster.cluster_endpoint
