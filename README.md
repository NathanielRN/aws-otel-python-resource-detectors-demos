# Demo of AWS OTel for Python Resource Detectors

This repo contains demos of `ResourceDetectors` for 5 different AWS services. This includes:

* EB (Elastic Beanstalk)
* ECS (Elastic Container Service)
* EC2 (Elastic Cloud Compute)
* EKS (Elastic Kubernetes Service)
* Lambda

When these services are instrumented with [OpenTelemetry for Python](https://github.com/open-telemetry/opentelemetry-python), these AWS `ResourceDetectors` can be used to automatically determine information about the runtime and populate attributes under the `resource` namespace of every trace.

For example if running on EC2 with the `AWSEc2ResourceDetector`, every span generated would automatically get populate with attributes like these:

```
"resource": {
    "cloud.provider": "aws",
    "cloud.platform": "aws_ec2",
    "cloud.account.id": "123456789012",
    "cloud.region": "us-west-2",
    "cloud.availability_zone": "us-west-2a",
    "host.id": "i-0957ce47cd1f56d17",
    "host.type": "t2.micro",
    "host.name": "ip-172-31-26-212.us-west-2.compute.internal"
}
```

## WARNING
At the time of upload, these demo explanations won't work out of the box! This is because although the `AwsResourceDetectors` have been merged upstream, they have yet to be release by OpenTelemetry for Python (OTel Python) upstream. A temporary workaround includes downloading the [OTel Python Core](https://github.com/open-telemetry/opentelemetry-python) and [OTel Python Contrib](https://github.com/open-telemetry/opentelemetry-python-contrib) repositories to the demo folders and updating the `requirements.txt` file to do a local install instead to get the latest code.

## Links
Check out the [OpenTelemetry SDK Extension for X-Ray package](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/sdk-extension/opentelemetry-sdk-extension-aws) for more information.