locals {
  resource_name = "dezoomcamp-final-project"
}

variable "project" {
  description = "Your GCP Project ID"
  default = "<gcp-project-id>"
}

variable "region" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  default = "asia-southeast2"
  type = string
}

variable "zone" {
  description = "Zone for GCP resources."
  default = "asia-southeast2-a"
  type = string
}

variable "credentials" {
  description = "Path to credential file"
  default = "../config/keyfile.json"
}

variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default = "STANDARD"
}

variable "BQ_DATASET" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type = string
  default = "final_project"
}
