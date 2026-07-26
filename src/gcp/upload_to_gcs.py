from pathlib import Path

from google.cloud import storage


BUCKET_NAME = "olist-data-lake-farouk-2026"
LOCAL_PARQUET_DIR = Path(
    "/workspace/data/processed/sales_dataset.parquet"
)
GCS_PREFIX = "processed/sales_dataset.parquet/"


def upload_parquet_directory() -> None:
    if not LOCAL_PARQUET_DIR.is_dir():
        raise FileNotFoundError(
            f"Dossier Parquet introuvable : {LOCAL_PARQUET_DIR}"
        )

    # On envoie uniquement les vraies parties Parquet.
    # On ignore _SUCCESS et les fichiers cachés .crc.
    parquet_files = sorted(LOCAL_PARQUET_DIR.glob("*.parquet"))

    if not parquet_files:
        raise FileNotFoundError(
            f"Aucun fichier .parquet trouvé dans : {LOCAL_PARQUET_DIR}"
        )

    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)

    print("=" * 60)
    print("Nettoyage de l'ancienne version dans GCS")
    print(f"Préfixe : gs://{BUCKET_NAME}/{GCS_PREFIX}")
    print("=" * 60)

    old_blobs = list(client.list_blobs(BUCKET_NAME, prefix=GCS_PREFIX))

    for blob in old_blobs:
        blob.delete()
        print(f"Ancien objet supprimé : gs://{BUCKET_NAME}/{blob.name}")

    print("=" * 60)
    print("Upload de la nouvelle version du dataset")
    print(f"Nombre de fichiers Parquet : {len(parquet_files)}")
    print("=" * 60)

    for local_file in parquet_files:
        blob_name = f"{GCS_PREFIX}{local_file.name}"
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(str(local_file))

        print(f"Upload réussi : gs://{BUCKET_NAME}/{blob_name}")

    print("=" * 60)
    print("Remplacement du dataset GCS terminé avec succès.")
    print("=" * 60)


if __name__ == "__main__":
    upload_parquet_directory()