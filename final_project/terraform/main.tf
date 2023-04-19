terraform {
  required_version = ">= 1.0"
  backend "local" {}
  required_providers {
    google = {
      source  = "hashicorp/google"
    }
  }
}

provider "google" {
  project = var.project
  region = var.region
  credentials = file(var.credentials)
}

# GCE Instance
resource "google_compute_instance" "vm_instance" {
  name         = "${local.resource_name}"
  machine_type = "e2-medium"
  zone         = var.zone
  tags         = ["http-server", "https-server", "project"]

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  network_interface {
    network = "default"

    access_config {
      nat_ip = google_compute_address.external_ip.address
    }
  }

  metadata = {
    "startup-script" = "apt-get update && apt-get install -y docker.io && chmod 666 /var/run/docker.sock"
  }

  can_ip_forward = true
}

resource "google_compute_address" "external_ip" {
  name = "external-ip"
}

# Firewall Rule
resource "google_compute_firewall" "prefect_ui" {
  name    = "prefect-ui"
  network = "default"
  target_tags = ["project"]

  allow {
    protocol = "tcp"
    ports    = ["4200"]
  }

  source_ranges = ["0.0.0.0/0"]
}

# GCS Bucket
resource "google_storage_bucket" "data-lake-bucket" {
  name          = "${local.resource_name}"
  location      = var.region

  storage_class = var.storage_class
  uniform_bucket_level_access = true

  versioning {
    enabled     = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30  // days
    }
  }

  force_destroy = true
}

# GBQ Dataset
resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.BQ_DATASET
  project    = var.project
  location   = var.region
}
