pipeline {
    agent any

    environment {
        AWS_REGION = 'ap-south-1'
        ECR_REPO = 'cloudforge-backend'
        IMAGE_TAG = 'latest'
        ACCOUNT_ID = 'ACCOUNT_ID'
        IMAGE_URI = "${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}:${IMAGE_TAG}"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/YOUR_USERNAME/cloudforge-backend.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t cloudforge-backend .'
            }
        }

        stage('Authenticate ECR') {
            steps {
                sh '''
                aws ecr get-login-password --region $AWS_REGION | \
                docker login --username AWS --password-stdin \
                $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
                '''
            }
        }

        stage('Tag Docker Image') {
            steps {
                sh 'docker tag cloudforge-backend:latest $IMAGE_URI'
            }
        }

        stage('Push Docker Image') {
            steps {
                sh 'docker push $IMAGE_URI'
            }
        }

        stage('Deploy To Kubernetes') {
            steps {
        sh 'kubectl apply -f ../cloudforge-k8s/'
            }
        }

        stage('Verify Deployment') {
            steps {
                sh 'kubectl get pods -n cloudforge'
            }
        }
    }
}