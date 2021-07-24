# Demo of AwsLambdaResourceDetector for OTel Python

Follow these steps to run a demo which automatically populates `resource` attributes for every span on an instrumented Lambda function:

## Run OTel traced function on AWS Lambda
1. Follow the [AWS OTel Getting Started with Lambda for Python Guide](https://aws-otel.github.io/docs/getting-started/lambda/lambda-python) to get OpenTelemetry
1. Upload the [application file](./application.py) to your Lambda function
1. Check out the console output to view the spans with automatically set `resource` attributes!