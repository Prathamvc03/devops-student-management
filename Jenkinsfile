pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'student-api'
        DOCKER_TAG   = "v${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code from Git repository...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                sh 'pip install --no-cache-dir -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running automated Pytest test suite for Student Management System...'
                sh 'pytest test_main.py -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image: ${DOCKER_IMAGE}:${DOCKER_TAG} and ${DOCKER_IMAGE}:latest..."
                sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} -t ${DOCKER_IMAGE}:latest ."
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo "Deploying ${DOCKER_IMAGE}:${DOCKER_TAG} to Kubernetes cluster..."
                sh 'kubectl apply -f k8s/deployment.yaml'
                sh 'kubectl apply -f k8s/service.yaml'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully! Student Management System API is tested, built, and deployed.'
        }
        failure {
            echo 'Pipeline failed. Check stage logs for errors.'
        }
        always {
            echo 'Pipeline execution finished.'
        }
    }
}
