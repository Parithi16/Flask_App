pipeline {
    agent any

    environment {
        GCP_PROJECT = "forward-fuze-468106-f4"
        GKE_CLUSTER = "flask-cluster"
        GKE_ZONE = "us-central1"
        BACKEND_IMAGE = "gcr.io/forward-fuze-468106-f4/flask-app:v3"
        FRONTEND_IMAGE = "gcr.io/forward-fuze-468106-f4/frontend:v3"
    }

    stages {

        stage('Authenticate to GCP') {
            steps {
                withCredentials([file(credentialsId: 'gcp-sa-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    sh '''
                        gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
                        gcloud config set project $GCP_PROJECT
                    '''
                }
            }
        }

        stage('Connect to GKE') {
            steps {
                sh '''
                    gcloud container clusters get-credentials $GKE_CLUSTER --zone $GKE_ZONE --project $GCP_PROJECT
                    kubectl get nodes
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    kubectl apply -f deployments/postgres-secret.yaml
                    kubectl apply -f deployments/postgres-deployment.yaml
                    kubectl apply -f deployments/flask-deployment.yaml
                    kubectl apply -f deployments/frontend-deployment.yaml
                    kubectl get pods
                    kubectl get svc
                '''
            }
        }
    }
}
