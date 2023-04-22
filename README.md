# kandula-app

This app is for managing ec2 instances schedulling in AWS.

I will need to build the image, tag it and push it to my ECR private registry.

These are the push commands (they are available in ECR as well):

1. sudo aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 735911875499.dkr.ecr.us-east-1.amazonaws.com

2. sudo docker build -t kandula .

3. sudo docker tag kandula:latest 735911875499.dkr.ecr.us-east-1.amazonaws.com/kandula:latest

4. sudo docker push 735911875499.dkr.ecr.us-east-1.amazonaws.com/kandula:latest

#For non interactive login
sudo docker login -u AWS -p $(aws ecr get-login-password --region us-east-1) 735911875499.dkr.ecr.us-east-1.amazonaws.com

It is going to be implemnetd to k8s with jenkins.

This is the k8s link repo:

https://github.com/modules-terraform-cloud/terraform-eks-k8s

***

I have configured webhooks to trigger runs in jenkins ui, whenever a commin has been submitted to this repo.
