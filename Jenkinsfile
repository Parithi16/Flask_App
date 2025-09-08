pipeline {
    agent any

    environment {
        GCP_PROJECT = "forward-fuze-468106-f4"
        GKE_CLUSTER = "flask-cluster"
        GKE_ZONE = "us-central1"
        BACKEND_IMAGE = "gcr.io/forward-fuze-468106-f4/flask-app"
        FRONTEND_IMAGE = "gcr.io/forward-fuze-468106-f4/frontend"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/Parithi16/Flask_App.git'
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    // Use Git short hash as image tag
                    COMMIT_HASH = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                    sh """
                        docker build -t $BACKEND_IMAGE:$COMMIT_HASH ./backend
                        docker build -t $FRONTEND_IMAGE:$COMMIT_HASH ./frontend
                    """
                }
            }
        }

        stage('Push Docker Images to GCR') {
            steps {
                withCredentials([file(credentialsId: 'gcp-sa-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    sh """
                        gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
                        gcloud auth configure-docker
                        docker push $BACKEND_IMAGE:$COMMIT_HASH
                        docker push $FRONTEND_IMAGE:$COMMIT_HASH
                    """
                }
            }
        }

        stage('Authenticate to GCP') {
            steps {
                withCredentials([file(credentialsId: 'gcp-sa-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    sh """
                        gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
                        gcloud config set project $GCP_PROJECT
                    """
                }
            }
        }

        stage('Connect to GKE') {
            steps {
                sh """
                    gcloud container clusters get-credentials $GKE_CLUSTER --zone $GKE_ZONE --project $GCP_PROJECT
                    kubectl get nodes
                """
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh """
                    # Update YAML files to use new image tags
                    sed -i "s|image: gcr.io/.*/flask-app:.*|image: $BACKEND_IMAGE:$COMMIT_HASH|" deployments/flask-deployment.yaml
                    sed -i "s|image: gcr.io/.*/frontend:.*|image: $FRONTEND_IMAGE:$COMMIT_HASH|" deployments/frontend-deployment.yaml

                    # Apply manifests
                    kubectl apply -f deployments/postgres-secret.yaml
                    kubectl apply -f deployments/postgres-deployment.yaml
                    kubectl rollout status deployment/postgres

                    kubectl apply -f deployments/flask-deployment.yaml
                    kubectl rollout status deployment/flask-app

                    kubectl apply -f deployments/frontend-deployment.yaml
                    kubectl rollout status deployment/frontend

                    kubectl get pods
                    kubectl get svc
                """
            }
        }
    }

    post {
        success {
            echo "CI/CD pipeline finished successfully! Deployed commit $COMMIT_HASH"
        }
        failure {
            echo "Pipeline failed. Check the logs above."
        }
    }
}
