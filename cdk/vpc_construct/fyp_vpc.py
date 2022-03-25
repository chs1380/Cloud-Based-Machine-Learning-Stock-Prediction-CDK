from aws_cdk import (aws_ec2 as ec2,
                     core
                     )
# create vpc with 4 subnet
class VPC_stack(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.vpc = ec2.Vpc(self, "Infra_VPC",
                           cidr="10.0.0.0/16",
                           max_azs=2,
                           # 2 public and private subnet with 2 nat instance.
                           subnet_configuration=[
                               ec2.SubnetConfiguration(
                                   name='Public-Subnet',
                                   subnet_type=ec2.SubnetType.PUBLIC,
                                   cidr_mask=24
                               ),
                               ec2.SubnetConfiguration(
                                   name='Private-Subnet',
                                   subnet_type=ec2.SubnetType.PRIVATE,
                                   cidr_mask=24)
                           ],
                           nat_gateways=2
                           )

