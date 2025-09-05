terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "7.0.1"
    }
  }
}

provider "google" {
  project = "forward-fuze-468106-f4"
  credentials = "forward-fuze-468106-f4-400e1bdb1141.json"
  region  = "us-central1"
  zone="us-central1-a"
}

data "google_client_config" "default" {}