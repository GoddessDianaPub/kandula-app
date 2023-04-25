# Kandula app deployment

This app is for managing AWS ec2 instances and schedulling.

- No change is going to be made until the deploy repo is going to be updated with the new release tag.
- [Deploy repo link](https://github.com/GoddessDianas/terraform-aws-deploy)
- [EKS repo link](https://github.com/GoddessDianas/terraform-eks-eks)


## Requirements

- Change the jenkins alb address on the webhook configured acoording your URL.
- 

## Notes

- There is a webhook configured that trigger runs in jenkins ui, whenever a commin has been submitted to this repo.
- Repo URI: 735911875499.dkr.ecr.us-east-1.amazonaws.com
- Push commands can be found on ECR as follows: 
  - aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin (Repo URI)
  - docker build -t (Repo URI):${env.BUILD_ID} .
  - docker push <Repo URI>/kandula:${env.BUILD_ID}
- For non interactive login (if you have any problem):
  - docker login -u AWS -p $(aws ecr get-login-password --region us-east-1) (Repo URI)
