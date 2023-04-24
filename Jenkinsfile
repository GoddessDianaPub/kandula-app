def notifySlack(String buildStatus = 'STARTED') {
    // Build status of null means success.
    buildStatus = buildStatus ?: 'SUCCESS'

    def color

    if (buildStatus == 'STARTED') {
        color = '#D4DADF'
    } else if (buildStatus == 'SUCCESS') {
        color = '#BDFFC3'
    } else if (buildStatus == 'UNSTABLE') {
        color = '#FFFE89'
    } else {
        color = '#FF9FA1'
    }

    def msg = "${buildStatus}: `${env.JOB_NAME}` #${env.BUILD_NUMBER}:\n${env.BUILD_URL}"

    slackSend(color: color, message: msg)
}

pipeline {

    agent {
        node {
            label 'linux'
            }
            try {
                notifySlack()

                // Existing build steps.
            } catch (e) {
                currentBuild.result = 'FAILURE'
                throw e
            } finally {
                notifySlack(currentBuild.result)
            }
        }   
        
    
    environment {
        AWS_ACCOUNT_ID        = "735911875499"
        AWS_DEFAULT_REGION    = "us-east-1"
        IMAGE_REPO_NAME       = "kandula"
        REPOSITORY_URI        = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${IMAGE_REPO_NAME}"
        REPO_URL              = "https://github.com/GoddessDianas/kandula-app.git"
        REPO_DIR              = "kandula-app-k8s"
        PYTHON_APP_IMAGE      = "python:3.9-slim"
        CLUSTER_NAME          = "opsschool-eks-diana"
    }
    
    stages {   
        
        stage ('Cloning Git') {
            steps {
                git url: "${REPO_URL}", branch: 'main',
                    credentialsId: 'Github_token'
            }
        } 
        
        stage ('Logging into AWS ECR') {
            steps {
                script {
                    sh "aws ecr get-login-password --region ${AWS_DEFAULT_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com"
                }
            }
        }
         
        // Restarting docker     
        stage ('Start docker') {
             steps {
                 sh 'sudo service docker start'
             }
        }
         
        // Building Docker images
        stage ('Building latest image') {
            steps {
                script {
                    sh "docker build -t ${IMAGE_REPO_NAME}:${env.BUILD_ID} ."
                }
            }
        }
      
        
        stage ('Pushing build No. to ECR') {
            steps {
                script {
                    sh "docker tag ${IMAGE_REPO_NAME}:${env.BUILD_ID} ${REPOSITORY_URI}:${env.BUILD_ID}"
                    sh "docker push ${REPOSITORY_URI}:${env.BUILD_ID}"
                }
            }
        }
        
        
//         stage ("Update kubeconfig file") {
//              steps {
//                  sh "aws eks --region=${AWS_DEFAULT_REGION} update-kubeconfig --name ${CLUSTER_NAME}"
//              }
//         }
        
//         stage ("Deploy to EKS") {
//              steps {
//                 sh "kubectl apply -f kandula-app.yaml"
//              }
//         } 

    }
}
