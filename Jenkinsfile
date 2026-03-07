pipeline {
    agent {
        docker { image 'python:3.11-slim' }
    }

    stages {
        
        // Build Stage
        stage('Build') {
            steps {
                echo 'Entering Build Stage..'
                sh 'pip install -r requirements.txt'
                echo 'Installed code - Successfull'
                sh 'ruff check . --fix'
                echo 'Ruff Lintern: Success'
            }
        }
        
        // Build Stage
        stage('Test') {
            steps {
                echo 'Entering Test Stage.'
                sh 'pytest tests/'
                echo 'Tests: Success'
            }
        }
        
        // Build Stage
        stage('Security') {
            steps {
                sh 'trivy image aeyzaguirre/products-ecommerce:latest'
            }
        }

        stage('container-build') {
            steps {
                echo "Entering Build Container Stage"
            }
        }
        stage('container-push') {
            steps {
                echo "Entering Push Container Stage"
            }
        }
        stage('deploy') {
            steps {
                echo "Entering Deploy Stage"
            }
        }
    }
}

