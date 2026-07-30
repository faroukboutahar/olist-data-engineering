resource "google_storage_bucket" "data_lake" {
  name     = "olist-data-lake-farouk-2026"
  location = var.region

  storage_class               = "STANDARD"
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"

  encryption {
    customer_managed_encryption_enforcement_config {
      restriction_mode = "NotRestricted"
    }

    customer_supplied_encryption_enforcement_config {
      restriction_mode = "FullyRestricted"
    }

    google_managed_encryption_enforcement_config {
      restriction_mode = "NotRestricted"
    }
  }
}

resource "google_bigquery_dataset" "analytics" {
  dataset_id = "analytics"
  location   = var.region
}