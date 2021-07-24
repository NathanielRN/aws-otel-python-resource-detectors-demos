# Demo of AwsEksResourceDetector for OTel Python

Follow these steps to run a demo which automatically populates `resource` attributes for every span on an instrumented EKS initiated instance:

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
1. Run `docker build -t <ECR_REPO_URL>/resource-detectors-test:eks-test-latest` in the `eks/` directory.
1. `docker push <ECR_REPO_URL>:eks-test-latest`
1. Verify that the image with this tag appears in your ECR repository

## Run the image on AWS EKS
1. Run `brew tap weaveworks/tap`
1. Run `brew install weaveworks/tap/eksctl`
1. Ensure you have the following AWS permissions:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "cloudwatch:*",
                "ec2:*",
                "cloudformation:*",
                "kms:DescribeKey",
                "elasticloadbalancing:*",
                "eks:*",
                "autoscaling:*",
                "kms:CreateGrant"
            ],
            "Resource": "*"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": "iam:CreateServiceLinkedRole",
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "iam:AWSServiceName": [
                        "autoscaling.amazonaws.com",
                        "ec2scheduled.amazonaws.com",
                        "elasticloadbalancing.amazonaws.com",
                        "spot.amazonaws.com",
                        "spotfleet.amazonaws.com",
                        "transitgateway.amazonaws.com"
                    ]
                }
            }
        },
        {
            "Sid": "VisualEditor2",
            "Effect": "Allow",
            "Action": "iam:CreateServiceLinkedRole",
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "iam:AWSServiceName": [
                        "eks.amazonaws.com",
                        "eks-nodegroup.amazonaws.com",
                        "eks-fargate.amazonaws.com"
                    ]
                }
            }
        },
        {
            "Sid": "VisualEditor3",
            "Effect": "Allow",
            "Action": "iam:GetRole",
            "Resource": "arn:aws:iam::<YOUR_ACCOUNT_NUM>:role/*"
        },
        {
            "Sid": "VisualEditor4",
            "Effect": "Allow",
            "Action": [
                "iam:CreateInstanceProfile",
                "iam:DeleteInstanceProfile",
                "iam:GetRole",
                "iam:GetInstanceProfile",
                "iam:TagRole",
                "iam:RemoveRoleFromInstanceProfile",
                "iam:CreateRole",
                "iam:DeleteRole",
                "iam:AttachRolePolicy",
                "iam:PutRolePolicy",
                "ssm:GetParameters",
                "iam:ListInstanceProfiles",
                "ssm:GetParameter",
                "iam:AddRoleToInstanceProfile",
                "iam:CreateOpenIDConnectProvider",
                "iam:ListInstanceProfilesForRole",
                "iam:PassRole",
                "iam:DetachRolePolicy",
                "iam:ListAttachedRolePolicies",
                "iam:DeleteRolePolicy",
                "iam:GetOpenIDConnectProvider",
                "iam:DeleteOpenIDConnectProvider",
                "iam:GetRolePolicy"
            ],
            "Resource": [
                "arn:aws:iam::<YOUR_AWS_ACCOUNT_ID>:instance-profile/eksctl-*",
                "arn:aws:iam::<YOUR_AWS_ACCOUNT_ID>:role/eksctl-*",
                "arn:aws:iam::<YOUR_AWS_ACCOUNT_ID>:role/aws-service-role/eks-nodegroup.amazonaws.com/AWSServiceRoleForAmazonEKSNodegroup",
                "arn:aws:iam::<YOUR_AWS_ACCOUNT_ID>:role/eksctl-managed-*",
                "arn:aws:iam::<YOUR_AWS_ACCOUNT_ID>:oidc-provider/*",
                "arn:aws:ssm:*:<YOUR_AWS_ACCOUNT_ID>:parameter/aws/*",
                "arn:aws:ssm:*::parameter/aws/*"
            ]
        }
    ]
}
```
1. Run
```bash
eksctl create cluster \
--name resource-detectors-test-eks-cluster \
--version 1.17 \
--region us-west-2 \ # Remove this line if it is not working!
--nodegroup-name resource-detectors-linux-nodes \
--node-type t2.micro \
--nodes 2
```
1. The `eksctl` command can take ~30 minutes so please be patient!
1. Ensure you have the `kubectl` command installed
1. Confirm the `eksctl` command was successful by running `kubectl get nodes` and `kubectl get ns`. You should see 2 nodes each time.
1. Give the default kubernetes service account admin permission (might be possible with weaker permissions?). This is necessary for `AwsEksResourceDetector` to be able to make requests to the Kubernetes endpoints and get information about the currently running instance. Run `kubectl --namespace kube-system --clusterrole=cluster-admin --serviceaccount=default:default create clusterrolebinding default-has-cluster-admin-rights-rule`
1. **IMPORTANT** Create an `amazon-cloudwatch` namespace. See the [AWS CloudWatch Docs - Create a namespace for CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Container-Insights-setup-metrics.html#create-namespace-metrics) (e.g. `kubectl apply -f https://raw.githubusercontent.com/aws-samples/amazon-cloudwatch-container-insights/latest/k8s-deployment-manifest-templates/deployment-mode/daemonset/container-insights-monitoring/cloudwatch-namespace.yaml`)
1. **IMPORTANT** Add a `cluster-info` configmap to the `amazon-cloudwatch` namespace. See the [AWS CloudWatch Docs - Quick Start with the CloudWatch agent and Fluentd ](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Container-Insights-setup-EKS-quickstart.html) (e.g. `curl -s https://raw.githubusercontent.com/aws-samples/amazon-cloudwatch-container-insights/latest/k8s-deployment-manifest-templates/deployment-mode/daemonset/container-insights-monitoring/quickstart/cwagent-fluentd-quickstart.yaml | sed "s/{{cluster_name}}/resource-detectors-test-eks-cluster/;s/{{region_name}}/${AWS_REGION}/" | kubectl apply -f -`)
1. Using the Docker Image URL you uploaded to ECR, run `kubectl run my-eks-py-app --image=<ECR_REPO_URL>/resource-detectors-test:ecs-test-latest --port=5000`
1. Confirm the image was pulled and started by running `kubectl get pods`. You should see the pod transition to `RUNNING` state. (It may take so time so please be patient!)
1. Expose the Kubernetes Deployment through a Load Balancer, run `kubectl expose pod my-eks-py-app --type=LoadBalancer --port=8888 --target-port=5000`
1. Find the public DNS for your container, run `kubectl get svc` and record the `EXTERNAL-IP`.
1. In your browser, go to `<POD_EXTERNAL_IP>:8888`. (It can take a while for the app to be ready to receive requests so please be patient!)
1. You should see a span with automatically set `resource` attributes every time you refresh this page!

## Optional:

### Bash on Kubernetes Nodes
1. Run `kubectl exec --stdin --tty my-eks-py-app -- /bin/bash` to get a bash session on an instance created with Kubernetes

### Rolling Update to Kubernetes Pod
1. After pushing a _new_ tag for a docker image, run `kubectl set image pod/my-eks-py-app my-eks-py-app=<ECR_REPO_URL>/resource-detectors-test:eks-v2`

### Clean Up

#### Only the images
1. Run `kubectl delete pod my-eks-py-app`
1. Run `kubectl delete svc my-eks-py-app`

#### Everything kubernetes
1. Run `eksctl delete cluster --name resource-detectors-test-eks-cluster`

Links:
* [YouTuber - How to Deploy a Docker App to AWS using Elastic Container Service (ECS)](https://www.youtube.com/watch?v=zs3tyVgiBQQ)
* [YouTuber - An easy way to create Kubernetes cluster on Amazon EKS](https://www.youtube.com/watch?v=p6xDCz00TxU)
* [Medium Article - Deploy a Docker Container With Kubernetes in 5 minutes](https://codeburst.io/getting-started-with-kubernetes-deploy-a-docker-container-with-kubernetes-in-5-minutes-eb4be0e96370)