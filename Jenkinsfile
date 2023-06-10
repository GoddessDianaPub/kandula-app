def notifySlack(buildStatus = null) {
    // Build status of null means success.
    buildStatus = buildStatus ?: 'SUCCESS'
    def color

    if (buildStatus == 'SUCCESS') {
        color = '#5dff54'
//     } else if (buildStatus == 'STARTED') {
//         color = '#f9c815'
    } else if (buildStatus == 'UNSTABLE') {
        color = '#fffe89'
    } else {
        color = '#ff0000'
    }

    def msg = "${buildStatus}:\n Job Name: ${env.JOB_NAME}\n Build Number #${env.BUILD_NUMBER}"
    slackSend(color: color, message: msg, channel: '#jenkins-notifications')
}

pipeline {
    agent {
        node {
            label 'linux'
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
        CLUSTER_NAME          = "opsschool-eks-QP4igSZ5"
//         BUILD_ID              = "${currentBuild.number}"
    }
    
    stages {
        stage ('Cloning Git') {
            steps {
                git url: "${REPO_URL}", branch: 'main', credentialsId: 'Github_token'
            }
        } 
        
        stage('Logging into AWS ECR') {
            steps {
                script {
                    sh "aws ecr get-login-password --region ${AWS_DEFAULT_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com"
                }
             }
        }
         
//         // Restarting Docker     
//         stage ('Start Docker') {
//              steps {
//                  sh 'sudo service docker start'
//              }
//         }
         
        // Building Docker images
        stage ('Building latest image') {
            steps {
                script {
                    sh "docker build -t ${REPOSITORY_URI}:${env.BUILD_ID} ."
                }
            }
        }
      
        stage ('Pushing build No. to ECR') {
            steps {
                script {
//                     sh "docker tag ${IMAGE_REPO_NAME}:${LATEST_TAG} ${REPOSITORY_URI}:${env.BUILD_ID}"
                    sh "docker push ${REPOSITORY_URI}:${env.BUILD_ID}"
                }
            }
        }
        
//         stage ("Login to EKS") {
//              steps {
//                  withKubeConfig(caCertificate: '', clusterName: '', contextName: '', credentialsId: 'eks.cred', namespace: '', serverUrl: '') {
//                  }
//                }
//              }

        
        stage ("Deploy to EKS") {
            steps {
//                 sh "aws eks --region=${AWS_DEFAULT_REGION} update-kubeconfig --name ${CLUSTER_NAME}"
//                 sh "kubectl edit image deployment kandula-app kandula-app=${REPOSITORY_URI}:${env.BUILD_ID}"
                sh "sed -i 's|image: .*|image: ${REPOSITORY_URI}:${env.BUILD_ID}|g' kandula-app.yaml"
                sh "kubectl apply -f kandula-app.yaml"
                }
              }         
  
    }
    post {
        always {
            notifySlack(currentBuild.result)
            script {
                deleteDir() //built-in step to clean up the workspace
            }
        }
    }
}
