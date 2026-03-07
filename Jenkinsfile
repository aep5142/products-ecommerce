pipeline {
    agent none

    environment {
        IMAGE = 'aeyzaguirre/products-ecommerce'
        REGISTRY_CREDENTIALS = 'dockerhub-credentials'
    }

    stages {

        // Runs on every branch and every PR
        stage('Build') {
            agent { docker { image 'python:3.11-slim' } }
            steps {
                echo 'Entering Build Stage....'
                sh 'pip install -r requirements.txt'
                echo 'Installed dependencies - Successful'
                sh 'ruff check . --fix'
                echo 'Ruff Linter: Success'
            }
        }

        // Runs on every branch and every PR
        stage('Test') {
            agent { docker { image 'python:3.11-slim' } }
            steps {
                echo 'Entering Test Stage.'
                sh 'pip install -r requirements.txt'
                sh 'pytest tests/'
                echo 'Tests: Success'
            }
        }

        // Runs on every branch and every PR
        stage('Security') {
            agent { docker { image 'python:3.11-slim' } }
            steps {
                echo 'Entering Security Scan...'
                sh '''
                    apt-get update && apt-get install -y curl
                    curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin
                    trivy image --exit-code 0 --severity HIGH,CRITICAL ${IMAGE}:latest
                '''
            }
        }

        // Only on develop, release/*, main — needs Docker
        stage('Container Build') {
            agent any
            when {
                anyOf {
                    branch 'develop'
                    branch 'release/*'
                    branch 'main'
                }
            }
            steps {
                script {
                    // Tagging strategy: env-tag + git commit + build number
                    def envTag = env.BRANCH_NAME == 'main' ? 'latest'
                              : env.BRANCH_NAME == 'develop' ? 'dev'
                              : 'staging'
                    def gitTag = "git-${env.GIT_COMMIT.take(7)}-${env.BUILD_NUMBER}"

                    echo "Building image with tags: ${envTag}, ${gitTag}"
                    sh "docker build -t ${IMAGE}:${envTag} -t ${IMAGE}:${gitTag} ."

                    // Store tags for later stages
                    env.ENV_TAG = envTag
                    env.GIT_TAG = gitTag
                }
            }
        }

        // Only on develop, release/*, main
        stage('Container Push') {
            agent any
            when {
                anyOf {
                    branch 'develop'
                    branch 'release/*'
                    branch 'main'
                }
            }
            steps {
                withCredentials([usernamePassword(credentialsId: REGISTRY_CREDENTIALS, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker push ${IMAGE}:${ENV_TAG}
                        docker push ${IMAGE}:${GIT_TAG}
                    '''
                }
            }
        }

        // Deploy Dev — only on develop
        stage('Deploy Dev') {
            agent any
            when { branch 'develop' }
            steps {
                echo 'Deploying to Dev environment...'
                sh """
                    docker pull ${IMAGE}:${ENV_TAG}
                    docker stop products || true
                    docker rm products || true
                    docker run -d --name products --network ecomm-net \\
                        -p 3001:3001 \\
                        -e DB_HOST=db \\
                        -e DB_USER=postgres \\
                        -e DB_PASSWORD=password \\
                        -e DB_NAME=ecommerce \\
                        ${IMAGE}:${ENV_TAG}
                """
            }
        }

        // Deploy Staging — only on release/*
        stage('Deploy Staging') {
            agent any
            when { branch 'release/*' }
            steps {
                echo 'Deploying to Staging environment...'
                sh """
                    docker pull ${IMAGE}:${ENV_TAG}
                    docker stop products-staging || true
                    docker rm products-staging || true
                    docker run -d --name products-staging --network ecomm-net \\
                        -p 3011:3001 \\
                        -e DB_HOST=db \\
                        -e DB_USER=postgres \\
                        -e DB_PASSWORD=password \\
                        -e DB_NAME=ecommerce \\
                        ${IMAGE}:${ENV_TAG}
                """
            }
        }

        // Deploy Prod — only on main, manual approval required
        stage('Deploy Prod') {
            agent any
            when { branch 'main' }
            steps {
                input message: 'Deploy products to Production?', ok: 'Approve'
                echo 'Deploying to Production environment...'
                sh """
                    docker pull ${IMAGE}:${ENV_TAG}
                    docker stop products-prod || true
                    docker rm products-prod || true
                    docker run -d --name products-prod --network ecomm-net \\
                        -p 3001:3001 \\
                        -e DB_HOST=db \\
                        -e DB_USER=postgres \\
                        -e DB_PASSWORD=password \\
                        -e DB_NAME=ecommerce \\
                        ${IMAGE}:${ENV_TAG}
                """
            }
        }
    }

    post {
        success {
            echo "Pipeline succeeded on branch: ${env.BRANCH_NAME}"
        }
        failure {
            echo "Pipeline failed on branch: ${env.BRANCH_NAME}"
        }
    }
}
