# Expected results:
#
# {
#     "name": "annotation page",
#     "context": {
#         "trace_id": "0xfe3e6f5eebe586584adb5b079fef6613",
#         "span_id": "0xba08daf97de93613",
#         "trace_state": "[]",
#     },
#     "kind": "SpanKind.INTERNAL",
#     "parent_id": null,
#     "start_time": "2021-07-22T23:40:07.609608Z",
#     "end_time": null,
#     "status": {"status_code": "UNSET"},
#     "attributes": {},
#     "events": [],
#     "links": [],
#     "resource": {
#         "service.name": "ecs-sample-app",
#         "cloud.provider": "aws",
#         "cloud.platform": "aws_ecs",
#         "container.name": "c1ac4ddea3c5",
#         "container.id": "c1ac4ddea3c5d5763da93fa7b1494e38f4f7b2abb50699926cbdb472c2fab2e7",
#     },
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

from opentelemetry.sdk.extension.aws.resource.ecs import AwsEcsResourceDetector


trace.set_tracer_provider(
    TracerProvider(
        resource=get_aggregated_resources([
            AwsEcsResourceDetector()
        ]),
    )
)

tracer = trace.get_tracer(__name__)


@app.route("/")
def call_http():
    with tracer.start_as_current_span("my_ecs_route") as span:
        return json.loads(span._readable_span().to_json())


if __name__ == "__main__":
    # with tracer.start_as_current_span("my_ecs_app") as span:
    app.run(**{"host": "0.0.0.0", "port": 5000, "debug": True})
