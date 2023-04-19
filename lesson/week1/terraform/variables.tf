locals {
  data_lake_bucket = "dtc_data_lake"
}

variable "project" {
  description = "Your GCP Project ID"
  default = "de-zoomcamp-375916"
}

variable "region" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  default = "asia-southeast2"
  type = string
}

variable "credentials" {
  description = "Path to credential file"
  default = "/home/rizky/zoomcamp/de-zoomcamp-375916-7d3bc8537cc2.json"
}

variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default = "STANDARD"
}

variable "BQ_DATASET" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type = string
  default = "staging"
}
