from aws_cdk import (aws_cloudfront as cloudfront,
                     aws_elasticloadbalancingv2 as elbv2,
                     aws_cloudfront_origins as origins,
                     core
                     )


# this will be create a cloudfront distribution with a elb as entry point

class cloudfront_dist(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, props: elbv2.ApplicationLoadBalancer, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.cloud_dist = cloudfront.Distribution(self, "myDist",
                                                  default_behavior=cloudfront.BehaviorOptions(
                                                      origin=origins.LoadBalancerV2Origin(props)),
                                                  )