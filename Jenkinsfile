pipeline {

    agent {
        node {
            label 'jenkins-agent-1'
        }
    }
    
//    options {
//       timeout(time: 5, unit: 'MINUTES') // set the timeout to 5 minutes
//   }
    
    environment {
    AWS_ACCOUNT_ID      = "735911875499"
    AWS_DEFAULT_REGION  = "us-east-1"
    IMAGE_REPO_NAME     = "kandula"
    IMAGE_TAG           = "latest"
    REPOSITORY_URI      = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${IMAGE_REPO_NAME}:${IMAGE_TAG}"
    REPO_URL            = "https://github.com/opsschool-project/kandula-app-k8s.git"
    REPO_DIR            = "kandula-app-k8s"
    PYTHON_APP_IMAGE    = "python:3.9-slim"
    CLUSTER_NAME        = "opsschool-eks-diana"
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
        
        // Restarting docker     
    //    stage ('Restart docker') {
    //         steps {
    //             sh 'sudo service docker restart'
    //      }
    //   }
         
        // Building Docker images
        stage('Building image') {
            steps{
                script {
                    dockerImage = docker.build "${IMAGE_REPO_NAME}:${IMAGE_TAG}"
                }
            }
        }
        
         // Uploading Docker images into AWS ECR
        stage('Pushing to ECR') {
            steps{
                script {
                    sh "docker tag ${IMAGE_REPO_NAME}:${IMAGE_TAG} ${REPOSITORY_URI}"
                    sh "docker push ${REPOSITORY_URI}"
                }
            }
        }
                      
        stage ('Delete the docker images') {
             steps {
                 sh "docker rmi -f ${PYTHON_APP_IMAGE}"
                 sh "docker rmi -f ${REPOSITORY_URI}"
                 sh "docker rmi -f ${IMAGE_REPO_NAME}:${IMAGE_TAG}"
          }
        }
                
//         stage ('Delete the folder and the files that has copied from the cloned repo using Dockerfile') {
//              steps {
//                  sh "rm -rf /home/ec2-user/jenkins-agent/jenkins-agent/workspace/kandula"
//                  sh "rm -rf /home/ec2-user/jenkins-agent/jenkins-agent/workspace/kandula@tmp"
//           }
//         }
        
        stage ('Delete the cloned repo') {
             steps {
                 sh "rm -rf ${REPO_DIR}"
          }
        }
        
        stage ("Login to EKS") {
            steps {
                withKubeConfig(caCertificate: '', clusterName: '', contextName: '', credentialsId: 'eks.cred', namespace: '', serverUrl: '') {
                }
              }
            }
        
        stage ("Deploy to EKS") {
            steps {
                sh "aws eks --region=${AWS_DEFAULT_REGION} update-kubeconfig --name ${CLUSTER_NAME}"
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
