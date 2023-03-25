locals {
  data_lake_bucket = "dezoomcamp_final_project"
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

variable "credentials" {
  description = "Path to credential file"
  default = "<path-to-service-account-keyfile>"
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