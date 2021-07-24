# Expected results:
#


# OpenTelemetry API

from opentelemetry import trace

# OpenTelemetry SDK Components

from opentelemetry.sdk.resources import get_aggregated_resources
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleSpanProcessor
)

# AWS X-Ray SDK Extension Components

from opentelemetry.sdk.extension.aws.resource._lambda import AwsLambdaResourceDetector


trace.set_tracer_provider(
    TracerProvider(
        active_span_processor=SimpleSpanProcessor(ConsoleSpanExporter()),
        resource=get_aggregated_resources(
            [
                AwsLambdaResourceDetector(),
            ]
        ),
    )
)

tracer = trace.get_tracer(__name__)


if __name__ == "__main__":
    with tracer.start_as_current_span("my_lambda_function") as span:
        print("Done a span!")
