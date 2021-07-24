# Demo of AwsEc2ResourceDetector for OTel Python

Follow these steps to run a demo which automatically populates `resource` attributes for every span on an instrumented EC2 instance:

## Run OTel app on AWS EC2
1. Start an EC2 instance from the AWS console, enable `ssh` access during setup
1. `ssh` onto the EC2 instance using your key pair (e.g. `ssh -i "/path/to/MyKeyPair.pem" ec2-user@ec2-12-345-678-90.us-west-2.compute.amazonaws.com`)
1. Upload the files in this `ec2/` directory to your EC2 instance (e.g. `scp -i /path/to/MyKeyPair.pem -r ./* ec2-user@ec2-12-345-678-90.us:~`)
1. Install the requirements specified in [requirements.txt](./requirements.txt) (e.g. `python3 -m pip install requirements.txt`)
1. Run the [application.py](./application.py). (e.g. `python3 application.py`)
1. Check out the console output to view the spans with automatically set `resource` attributes!
