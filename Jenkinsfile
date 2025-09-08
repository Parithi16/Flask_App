pipeline {
    agent any
    environment {
        GOOGLE_APPLICATION_CREDENTIALS = credentials('gcp-sa-key')
    }
    stages {
        stage('Connect to GKE') {
            steps {
                sh '''
                  gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
                  gcloud container clusters get-credentials flask-cluster --zone us-central1 --project forward-fuze-468106-f4
                  kubectl get pods
                '''
            }
        }
    }
}
