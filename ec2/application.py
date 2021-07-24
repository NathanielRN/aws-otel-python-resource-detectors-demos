# Expected results:
#
# {
#     "name": "my_ec2_app",
#     "context": {
#         "trace_id": "0x0e042b3e28a1c836e4712622bd666bb6",
#         "span_id": "0x389f8abc1d052b86",
#         "trace_state": "[]"
#     },
#     "kind": "SpanKind.INTERNAL",
#     "parent_id": null,
#     "start_time": "2021-07-13T00:30:42.371664Z",
#     "end_time": "2021-07-13T00:30:42.371857Z",
#     "status": {
#         "status_code": "UNSET"
#     },
#     "attributes": {},
#     "events": [],
#     "links": [],
#     "resource": {
#         "cloud.provider": "aws",
#         "cloud.platform": "aws_ec2",
#         "cloud.account.id": "<YOUR_AWS_ACCOUNT_ID>",
#         "cloud.region": "us-west-2",
#         "cloud.availability_zone": "us-west-2a",
#         "host.id": "i-0957ce47cd1f56d17",
#         "host.type": "t2.micro",
#         "host.name": "ip-172-31-26-212.us-west-2.compute.internal"
#     }
# }

# OpenTelemetry API

from opentelemetry import trace

# OpenTelemetry SDK Components

from opentelemetry.sdk.resources import get_aggregated_resources
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)

# AWS X-Ray SDK Extension Components

from opentelemetry.sdk.extension.aws.resource.ec2 import AwsEc2ResourceDetector


# Setup OpenTelemetry Python

trace.set_tracer_provider(
    TracerProvider(
        active_span_processor=SimpleSpanProcessor(ConsoleSpanExporter()),
        resource=get_aggregated_resources(
            [
                AwsEc2ResourceDetector(),
            ]
        ),
    )
)

tracer = trace.get_tracer(__name__)


if __name__ == "__main__":
    with tracer.start_as_current_span("my_ec2_app") as span:
        print("Done a span!")
