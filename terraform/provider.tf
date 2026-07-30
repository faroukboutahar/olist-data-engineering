terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 7.0"
    }
  }
}

provider "google" {
  credentials = file("../dbt/.keys/dbt-bigquery-sa.json")
  project     = var.project_id
  region      = var.region
}