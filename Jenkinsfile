pipeline {
    agent any

    environment {
        GCP_PROJECT = "forward-fuze-468106-f4"
        GKE_CLUSTER = "flask-cluster"
        GKE_ZONE = "us-central1"
        GKE_REGION="us-central1-a"
        BACKEND_IMAGE = "us-docker.pkg.dev/forward-fuze-468106-f4/gcr.io/flask-app"
        FRONTEND_IMAGE = "us-docker.pkg.dev/forward-fuze-468106-f4/gcr.io/frontend"
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
                    def COMMIT_HASH = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                    sh """
                        docker build -t $BACKEND_IMAGE:$COMMIT_HASH ./backend
                        docker build -t $FRONTEND_IMAGE:$COMMIT_HASH ./frontend
                    """
                    env.COMMIT_HASH = COMMIT_HASH
                }
            }
        }

        stage('Push Docker Images to GCP Artifact Registry') {
            steps {
                withCredentials([file(credentialsId: 'gcp-sa-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    sh """
                        gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
                        gcloud auth configure-docker us-docker.pkg.dev
                        docker push $BACKEND_IMAGE:$COMMIT_HASH
                        docker push $FRONTEND_IMAGE:$COMMIT_HASH
                    """
                }
            }
        }

        stage('Connect to GKE') {
            steps {
                withCredentials([file(credentialsId: 'gcp-sa-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    sh """
                        gcloud auth activate-service-account --key-file = $GOOGLE_APPLICATION_CREDENTIALS
                        gcloud config set project $GCP_PROJECT
                        gcloud container clusters get-credentials $GKE_CLUSTER --region $GKE_REGION --project $GCP_PROJECT
                        export USE_GKE_GCLOUD_AUTH_PLUGIN=True
                        kubectl get nodes
                    """
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh """
                    sed -i "s|image: .*/flask-app:.*|image: $BACKEND_IMAGE:$COMMIT_HASH|" deployments/flask-deployment.yaml
                    sed -i "s|image: .*/frontend:.*|image: $FRONTEND_IMAGE:$COMMIT_HASH|" deployments/frontend-deployment.yaml

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
            echo "CI/CD pipeline finished successfully! Deployed commit ${env.COMMIT_HASH}"
        }
        failure {
            echo " Pipeline failed. Check the logs above."
        }
    }
}
