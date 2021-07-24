# Expected results:
#
# {
#     "attributes": {},
#     "context": {
#         "span_id": "0x7ba8321ebe7d438e",
#         "trace_id": "0xb4ae45973c28d6ee9ba661835a0192c9",
#         "trace_state": "[]",
#     },
#     "end_time": null,
#     "events": [],
#     "kind": "SpanKind.INTERNAL",
#     "links": [],
#     "name": "my_eks_route",
#     "parent_id": null,
#     "resource": {
#         "cloud.platform": "aws_eks",
#         "cloud.provider": "aws",
#         "container.id": "52a55b4ce22d018b295b7e20e570f54c7ec76684f9c71caebb3827d2cc8bf9d3",
#         "k8s.cluster.name": "resource-detectors-test-eks-cluster",
#         "service.name": "eks-sample-resource-detectors-app",
#     },
#     "start_time": "2021-07-23T19:12:56.113035Z",
#     "status": {"status_code": "UNSET"},
# }

from flask import Flask

app = Flask(__name__)

import json

# OpenTelemetry API

from opentelemetry import trace

# OpenTelemetry SDK Components

from opentelemetry.sdk.resources import get_aggregated_resources
from opentelemetry.sdk.trace import TracerProvider

# AWS X-Ray SDK Extension Components

from opentelemetry.sdk.extension.aws.resource.eks import AwsEksResourceDetector


trace.set_tracer_provider(
    TracerProvider(
        resource=get_aggregated_resources([
            AwsEksResourceDetector()
        ]),
    )
)

tracer = trace.get_tracer(__name__)


@app.route("/")
def call_http():
    with tracer.start_as_current_span("my_eks_route") as span:
        return json.loads(span._readable_span().to_json())


if __name__ == "__main__":
    # with tracer.start_as_current_span("my_eks_app") as span:
    app.run(**{"host": "0.0.0.0", "port": 5000, "debug": True})

