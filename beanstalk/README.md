# Demo of AwsBeanstalkResourceDetector for OTel Python

Follow these steps to run a demo which automatically populates `resource` attributes for every span on an instrumented EB initiated instance:

## Use AWS Elastic Beanstalk to run OTel app on EC2 instances
1. Create a Python Elastic Beanstalk environment
1. **IMPORTANT:** Enable the X-Ray daemon on elastic beanstalk. See the [X-Ray docs for running the daemon on Elastic Beanstalk](https://docs.aws.amazon.com/xray/latest/devguide/xray-daemon-beanstalk.html#xray-daemon-beanstalk-option)
1. Install the `awsecli` on your local machine. See [the Elastic Beanstalk for docs for installing the EB CLI](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install-osx.html)
1. In this `./beanstalk` folder, run `eb init`. Go through the configuration steps to initialize this directory for the environment you just created. This should create a `./elasticbeanstalk/config.yaml` file.
1. In `./beanstalk`, run `eb deploy` to upload this folder as an application version on Elastic Beanstalk. As a python environment, elastic beanstalk will automatically know to install the `requirements.txt` file for its Python dependencies and will start `application.py`. Notice that logs are configured to be output to `/tmp/sample-app.log`.
1. Use the AWS Beanstalk console to find the running EC2 instances. Go to public DNS address for that EC2 instance in your browser to see the Beanstalk welcome page.
1. Go back to the AWS Beanstalk console > Logs > Request Logs > Last 100 Lines. Under the `/tmp/sample-app.log` header, you should see spans with automatically set `resource` attributes!

## Optional:

### ssh onto EB created EC2 instances
1. Use `eb ssh --setup` to be able to ssh onto the EC2 instances created by Elastic Beanstalk.
1. Use `eb ssh` to ssh onto an instance

Links:
* [Getting started with Elastic Beanstalk](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/GettingStarted.html)