pipeline {
    agent any

    environment {
        GCP_PROJECT = "forward-fuze-468106-f4"
        GKE_CLUSTER = "flask-cluster"
        GKE_ZONE = "us-central1"
        BACKEND_IMAGE = "us-docker.pkg.dev/forward-fuze-468106-f4/gcr.io/flask-app"
        FRONTEND_IMAGE = "us-docker.pkg.dev/forward-fuze-468106-f4/gcr.io/frontend"
    }
    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/Parithi16/Flask_App.git'
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
                    # Optionally update YAML files if you need to change image tags
                    sed -i "s|image: .*/flask-app:.*|image: $BACKEND_IMAGE|" deployments/flask-deployment.yaml
                    sed -i "s|image: .*/frontend:.*|image: $FRONTEND_IMAGE|" deployments/frontend-deployment.yaml

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
            echo "CI/CD pipeline finished successfully!"
        }
        failure {
            echo "Pipeline failed. Check the logs above."
        }
    }
}
