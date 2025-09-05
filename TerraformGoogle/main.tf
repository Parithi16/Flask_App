resource "google_container_cluster" "flask-cluster" {
  name     = "flask-cluster"
  location = "us-central1"

  initial_node_count = 1

  node_config {
    machine_type  = "e2-medium"
    disk_size_gb  = 20
  }
}

output "kubernetes_cluster_name" {
  value = google_container_cluster.flask-cluster.name
}

output "kubernetes_cluster_endpoint" {
  value = google_container_cluster.flask-cluster.endpoint
}