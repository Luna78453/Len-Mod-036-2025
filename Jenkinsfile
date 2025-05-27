pipeline{
    agent any
    environment{
        AWS_REGION = 'us-east-2'
        IMAGE_NAME = 'ecdc-flask'
        REPO_NAME = 'lenmod/ecdc'
    }
    stages{
        stage('checkout'){
            steps{
                git 'git@github.com:Luna78453/Len-Mod-036-2025.git'
            }
        }
        stage('tag the image'){
            steps{
                script(
                    IMAGE_TAG = 'latest'
                )
            }   
        }
        stage('login to ECR'){
            steps{
                withAWS(region: "${env.AWS_REGION}", credentials: 'aws-creds'){
                    powershell'''
                    $ecrLogin - aws ecr get-login-password --region $env.AWS-REGION

                    docker login --username AWS --password $ecrLogin https://916965752431.dkr.ecr.us-east-2.amazonaws.com/lenmod/ecdc
                    '''
                }
            }
        }
        stage('Build Docker image'){
            steps{
                powershell '''
                docker build -t $env.IMAGE_NAME:$env.IMAGE_TAG .
                docker tag $env.IMAGE_NAME:$env.IMAGE_TAG 916965752431.dkr.ecr.us-east-2.amazonaws.com/lenmod/ecdc:latest
                '''
            }
        }
        stage('Push to ECR'){
            steps{
                powershell '''
                docker push 916965752431.dkr.ecr.us-east-2.amazonaws.com/lenmod/ecdc
                '''
            }
        }
    }
}
