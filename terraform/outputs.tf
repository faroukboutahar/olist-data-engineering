output "gcs_bucket_name" {
  description = "Nom du bucket GCS utilisé comme Data Lake"
  value       = google_storage_bucket.data_lake.name
}

output "bigquery_dataset_id" {
  description = "Identifiant du dataset BigQuery analytics"
  value       = google_bigquery_dataset.analytics.dataset_id
}