# Kandula app deployment

This app is for managing AWS ec2 instances and schedulling.


## Requirements

- Change the jenkins ALB URL, on the webhook configured to this repo, acoording your ALB URL.
- In the environment section in Jenkinsfile, update the value of the CLUSTER_NAME variable.

## Notes

- There is a webhook configured that trigger runs in jenkins ui, whenever a commit has been submitted to this repo.
- Repo URI: 735911875499.dkr.ecr.us-east-1.amazonaws.com
- Push commands can be found on ECR as follows: 
  - aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin (Repo URI)
  - docker build -t (Repo URI):${env.BUILD_ID} .
  - docker push (Repo URI)/kandula:${env.BUILD_ID}
- For non interactive login (if you have any problem):
  - docker login -u AWS -p $(aws ecr get-login-password --region us-east-1) (Repo URI)

- There is a cli option to describe instances as well as stop, start and terminate instances, the file named: aws_cli.py
  - To use it type: "python aws_cli.py" on your terminal
  - Make sure you have the aws credentials configured with the appropriate permissions

- I trying to make my project better all the time, so i am constantly updating this repo
