from aws_cdk import (aws_route53 as route53,core,
                     aws_eks as eks)


class Route_53_Stack(core.stack):
    def __init__(self, scope: core.Construct, construct_id: str, props:eks.Cluster.cluster_endpoint, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.route_53= route53.PublicHostedZone(self,"EKS_route_53",
                                                reco


                                                )