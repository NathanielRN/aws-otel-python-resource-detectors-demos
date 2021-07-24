# Expected results:
#
# {
#     "name": "my_beanstalk_app",
#     "context": {
#         "trace_id": "0xc2675b64287bc4f4c15e22406fce97ee",
#         "span_id": "0x41139b7f40d5acbf",
#         "trace_state": "[]"
#     },
#     "kind": "SpanKind.INTERNAL",
#     "parent_id": null,
#     "start_time": "2021-07-22T18:57:04.224392Z",
#     "end_time": "2021-07-22T18:57:04.224597Z",
#     "status": {
#         "status_code": "UNSET"
#     },
#     "attributes": {},
#     "events": [],
#     "links": [],
#     "resource": {
#         "cloud.provider": "aws",
#         "cloud.platform": "aws_elastic_beanstalk",
#         "service.name": "aws_elastic_beanstalk",
#         "service.namespace": "Otelpythonflaskwithresourcedetector-env",
#         "service.version": "app-210722_115156",
#         "service.instance.id": 20
#     }
# }

import logging
import logging.handlers

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

# Handler 
LOG_FILE = '/tmp/sample-app.log'
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1048576, backupCount=5)
handler.setLevel(logging.DEBUG)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add Formatter to Handler
handler.setFormatter(formatter)

# add Handler to Logger
logger.addHandler(handler)

welcome = """
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
  <!--
    Copyright 2012 Amazon.com, Inc. or its affiliates. All Rights Reserved.

    Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at

        http://aws.Amazon/apache2.0/

    or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
  -->
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <title>Welcome</title>
  <style>
  body {
    color: #ffffff;
    background-color: #E0E0E0;
    font-family: Arial, sans-serif;
    font-size:14px;
    -moz-transition-property: text-shadow;
    -moz-transition-duration: 4s;
    -webkit-transition-property: text-shadow;
    -webkit-transition-duration: 4s;
    text-shadow: none;
  }
  body.blurry {
    -moz-transition-property: text-shadow;
    -moz-transition-duration: 4s;
    -webkit-transition-property: text-shadow;
    -webkit-transition-duration: 4s;
    text-shadow: #fff 0px 0px 25px;
  }
  a {
    color: #0188cc;
  }
  .textColumn, .linksColumn {
    padding: 2em;
  }
  .textColumn {
    position: absolute;
    top: 0px;
    right: 50%;
    bottom: 0px;
    left: 0px;

    text-align: right;
    padding-top: 11em;
    background-color: #1BA86D;
    background-image: -moz-radial-gradient(left top, circle, #6AF9BD 0%, #00B386 60%);
    background-image: -webkit-gradient(radial, 0 0, 1, 0 0, 500, from(#6AF9BD), to(#00B386));
  }
  .textColumn p {
    width: 75%;
    float:right;
  }
  .linksColumn {
    position: absolute;
    top:0px;
    right: 0px;
    bottom: 0px;
    left: 50%;

    background-color: #E0E0E0;
  }

  h1 {
    font-size: 500%;
    font-weight: normal;
    margin-bottom: 0em;
  }
  h2 {
    font-size: 200%;
    font-weight: normal;
    margin-bottom: 0em;
  }
  ul {
    padding-left: 1em;
    margin: 0px;
  }
  li {
    margin: 1em 0em;
  }
  </style>
</head>
<body id="sample">
  <div class="textColumn">
    <h1>Congratulations</h1>
    <p>Your first BOB LE PONGE Elastic Beanstalk Python Application is now running on your own dedicated environment in the AWS Cloud</p>
    <p>This environment is launched with Elastic Beanstalk Python Platform</p>
  </div>
  
  <div class="linksColumn"> 
    <h2>What's Next?</h2>
    <ul>
    <li><a href="http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/">AWS Elastic Beanstalk overview</a></li>
    <li><a href="http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/index.html?concepts.html">AWS Elastic Beanstalk concepts</a></li>
    <li><a href="http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/create_deploy_Python_django.html">Deploy a Django Application to AWS Elastic Beanstalk</a></li>
    <li><a href="http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/create_deploy_Python_flask.html">Deploy a Flask Application to AWS Elastic Beanstalk</a></li>
    <li><a href="http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/create_deploy_Python_custom_container.html">Customizing and Configuring a Python Container</a></li>
    <li><a href="http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/using-features.loggingS3.title.html">Working with Logs</a></li>

    </ul>
  </div>
</body>
</html>
"""

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

from opentelemetry.sdk.extension.aws.resource.beanstalk import (
    AwsBeanstalkResourceDetector,
)


class MyExportWriter:
  def __init__(self, logger_to_use):
    self.logger = logger_to_use

  def write(self, string_to_output):
    self.logger.warning(string_to_output)
  
  def flush(self):
    pass

# Setup OpenTelemetry Python

trace.set_tracer_provider(
    TracerProvider(
        active_span_processor=SimpleSpanProcessor(ConsoleSpanExporter(out=MyExportWriter(logger))),
        resource=get_aggregated_resources(
            [
                AwsBeanstalkResourceDetector(),
            ]
        ),
    )
)

tracer = trace.get_tracer(__name__)

def application(environ, start_response):
    path = environ['PATH_INFO']
    method = environ['REQUEST_METHOD']
    if method == 'POST':
        try:
            if path == '/':
                request_body_size = int(environ['CONTENT_LENGTH'])
                request_body = environ['wsgi.input'].read(request_body_size)
                logger.info("Received message: %s" % request_body)
            elif path == '/scheduled':
                logger.info("Received task %s scheduled at %s", environ['HTTP_X_AWS_SQSD_TASKNAME'],
                            environ['HTTP_X_AWS_SQSD_SCHEDULED_AT'])
        except (TypeError, ValueError):
            logger.warning('Error retrieving request body for async work.')
        response = ''
    else:
        response = welcome
    with tracer.start_as_current_span("my_beanstalk_app") as span:
        print("Done a span!")
    start_response("200 OK", [
        ("Content-Type", "text/html"),
        ("Content-Length", str(len(response)))
    ])
    return [bytes(response, 'utf-8')]
