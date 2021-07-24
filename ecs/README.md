# Demo of AwsEcsResourceDetector for OTel Python

Follow these steps to run a demo which automatically populates `resource` attributes for every span on an instrumented ECS initiated instance:

## Upload this app as a Docker Image to AWS Elastic Container Registry (ECR)
1. From the AWS ECR console, click Create Repository
1. Name the repository "resource-detectors-test" and write down the ECR repository URL (e.g. `123456789012.dkr.ecr.us-west-2.amazonaws.com`)
1. Ensure you at least have the following permissions:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ecr:BatchGetImage",
                "ecr:BatchCheckLayerAvailability",
                "ecr:CompleteLayerUpload",
                "ecr:DescribeImages",
                "ecr:DescribeRepositories",
                "ecr:GetDownloadUrlForLayer",
                "ecr:InitiateLayerUpload",
                "ecr:ListImages",
                "ecr:PutImage",
                "ecr:UploadLayerPart"
            ],
            "Resource": "arn:aws:ecr:*:<YOUR_ACCOUNT_NUMBER>:repository/*"
        },
        {
            "Effect": "Allow",
            "Action": "ecr:GetAuthorizationToken",
            "Resource": "*"
        }
    ]
}
```
1. Run `aws ecr get-login-password --region us-west-2` and remember the token in the output
1. Run `docker login --username AWS -p <TOKEN> <ECR_REPO_URL>`
1. Run `docker build -t <ECR_REPO_URL>/resource-detectors-test:ecs-test-latest` in the `ecs/` directory.
1. `docker push <ECR_REPO_URL>/resource-detectors-test:ecs-test-latest`
1. Verify that the image with this tag appears in your ECR repository

## Run the image on AWS ECS
1. Go to the AWS ECS console > Clusters > ECS Linux + Networking.
  1. Name the cluster "ResourceDetectorsTestCluster"
  1. Use the `t2.micro` instance
  1. Use the default VPC
  1. Use the first subnet
  1. Enable Auto assign public IP
  1. Use the default security group
  1. Click Create
1. Go to the AWS ECS console > Task Definition > EC2
  1. Name the task "ResourceDetectorsTestTask"
  1. Set Task memory to 512
  1. Set task CPU to 1024
  1. Click Add container
    1. Name the container "MyEKSResourceDetectorsTestContainer"
    1. Enter the tag for the container you pushed to ECR above. (e.g. `<ECR_REPO_URL>/resource-detectors-test:ecs-test-latest`)
    1. In port mappings, write `8888` for the host port, `5000` for the container port
    1. Click Create
1. Go back to the AWS ECS console > Clusters > Tasks
  1. Click Run new Task
  1. Set Launch type to EC2
  1. Select the task you created above (e.g. `ResourceDetectorsTestTask`)
  1. Click Run Task
1. Wait a few minutes on the Tasks tab until the tasks successful transitions from PENDING to RUNNING
1. Go to the AWS EC2 console > Click the instance ECS just spun up > Security groups > view inbound rules > Click on the security group you set in the step above > Edit inbound rules
  1. Add rule
  1. Select Custom TCP rule
  1. Protocol TCP
  1. Port range 8888
  1. Add Custom `0.0.0.0/0`
  1. Add another rule for Custom `::/0`
1. Go to public DNS of the EC2 instance spun up by ECS at port 8888
1. Run `brew tap weaveworks/tap`
1. Run `brew install weaveworks/tap/eksctl`
1. Ensure you have the following AWS permissions:
1. You should see a span with automatically set `resource` attributes every time you refresh this page!

## Optional:

### ssh onto ECS created EC2 instances
1. Use `eb ssh --setup` to be able to ssh onto the EC2 instances created by Elastic Beanstalk.
1. Use `eb ssh` to ssh onto an instance

Links:
* [YouTuber - How to Deploy a Docker App to AWS using Elastic Container Service (ECS)](https://www.youtube.com/watch?v=zs3tyVgiBQQ)
