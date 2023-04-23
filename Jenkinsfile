pipeline {

    agent {
        node {
            label 'linux'
        }
    }
    
//    options {
//       timeout(time: 5, unit: 'MINUTES') // set the timeout to 5 minutes
//   }
    
    environment {
    AWS_ACCOUNT_ID        = "735911875499"
    AWS_DEFAULT_REGION    = "us-east-1"
    IMAGE_REPO_NAME       = "kandula"
    IMAGE_TAG             = "latest"
    REPOSITORY_URI        = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${IMAGE_REPO_NAME}"
    REPO_URL              = "https://github.com/GoddessDianas/kandula-app.git"
    REPO_DIR              = "kandula-app-k8s"
    PYTHON_APP_IMAGE      = "python:3.9-slim"
    CLUSTER_NAME          = "opsschool-eks-diana"
    }
    
    stages {   
        
        stage('Cloning Git') {
            steps {
                git url: "${REPO_URL}", branch: 'main',
                 credentialsId: 'Github_token'
            }
        } 
        
        stage('Logging into AWS ECR') {
            steps {
                script {
                    sh "aws ecr get-login-password --region ${AWS_DEFAULT_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com"
                }
             }
        }
        
         
        // Building Docker images
        stage('Building latest image') {
            steps{
                script {
                    dockerImage = docker.build "${IMAGE_REPO_NAME}:${IMAGE_TAG}"
                }
            }
        }
        
         // Uploading Docker images into AWS ECR
        stage('Pushing latest to ECR') {
            steps{
                script {
                    sh "docker tag ${IMAGE_REPO_NAME}:${IMAGE_TAG} ${REPOSITORY_URI}:${IMAGE_TAG}"
                    sh "docker push ${REPOSITORY_URI}:${IMAGE_TAG}"
                }
            }
        }
        
        
        stage('Pushing build No. to ECR') {
            steps{
                script {
                    sh "docker tag ${IMAGE_REPO_NAME}:${IMAGE_TAG} ${REPOSITORY_URI}:${env.BUILD_ID}"
                    sh "docker push ${REPOSITORY_URI}:${env.BUILD_ID}"
                }
            }
        }
        
        stage ("Update kubeconfig file") {
            steps {
                sh "aws eks --region=${AWS_DEFAULT_REGION} update-kubeconfig --name ${CLUSTER_NAME}"
                }
              }
        
        stage ("Deploy to EKS") {
            steps {
                sh "kubectl apply -f kandula-app.yaml"
                }
              } 
          
        
        stage('Slack notifications') {
            steps {
                script {
                    def status = currentBuild.currentResult // Get the result of the current build
                    def message = status == 'SUCCESS' ? "Job name: ${env.JOB_NAME}\n Build #${env.BUILD_NUMBER} succeeded!" : "Build #${env.BUILD_NUMBER} failed!"
//      (<${env.BUILD_URL}|Open>)         
                    try {
                        slackSend channel: 'jenkins-notifications', color: status == 'SUCCESS' ? '#36a64f' : '#ff0000', message: message, tokenCredentialId: 'slack.integration'
                    } catch (Exception err) {
                        echo "Slack notification failed with error: ${e.getMessage()}"
                    }
//                  post {
//                     always {
//                         echo "Build finished with ${end}:${JOB_NAME} #${BUILD_NUMBER}"
//                     }
//                   }        
             
                }
            }
        }    
     
 
  }
 }   
