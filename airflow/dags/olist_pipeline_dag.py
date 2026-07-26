from datetime import datetime
from pathlib import Path
import sys

from airflow.sdk import dag, task
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import (
    GCSToBigQueryOperator,
)
from docker.types import Mount


HOST_DATA_PATH = (
    "C:/Users/bouta/OneDrive/Documents/"
    "DE_PORTFOLIO_PROJECT/project/"
    "olist-data-engineering/data"
)

HOST_DBT_PATH = (
    "C:/Users/bouta/OneDrive/Documents/"
    "DE_PORTFOLIO_PROJECT/project/"
    "olist-data-engineering/dbt/olist_dbt"
)

HOST_DBT_PROFILES_PATH = (
    "C:/Users/bouta/OneDrive/Documents/"
    "DE_PORTFOLIO_PROJECT/project/"
    "olist-data-engineering/dbt/.dbt"
)

HOST_DBT_KEYS_PATH = (
    "C:/Users/bouta/OneDrive/Documents/"
    "DE_PORTFOLIO_PROJECT/project/"
    "olist-data-engineering/dbt/.keys"
)


@dag(
    dag_id="olist_pipeline",
    schedule=None,
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["olist", "pipeline"],
)
def olist_pipeline():

    @task
    def check_csv_files():
        data_path = Path("/workspace/data/sample")
        csv_files = list(data_path.glob("*.csv"))

        print("=" * 50)
        print("Vérification des fichiers CSV")
        print("=" * 50)
        print(f"Nombre de CSV trouvés : {len(csv_files)}")

        if not csv_files:
            raise FileNotFoundError(
                "Aucun fichier CSV trouvé dans /workspace/data/sample"
            )

        for csv_file in csv_files:
            print(csv_file.name)

        print("Tous les fichiers CSV sont présents.")

    check_csv = check_csv_files()

    run_spark = DockerOperator(
        task_id="run_spark",
        image="olist-spark:1.0",
        command=["python", "src/main.py"],
        docker_url="unix:///var/run/docker.sock",
        mounts=[
            Mount(
                source=HOST_DATA_PATH,
                target="/workspace/data",
                type="bind",
            )
        ],
        mount_tmp_dir=False,
        auto_remove="success",
        force_pull=False,
    )

    @task
    def check_parquet():
        parquet_path = Path(
            "/workspace/data/processed/sales_dataset.parquet"
        )

        if not parquet_path.exists():
            raise FileNotFoundError(
                f"Le résultat Parquet est introuvable : {parquet_path}"
            )

        parquet_parts = list(parquet_path.glob("*.parquet"))

        if not parquet_parts:
            raise FileNotFoundError(
                f"Aucun fichier .parquet trouvé dans : {parquet_path}"
            )

        print(f"Dataset Parquet trouvé : {parquet_path}")
        print(f"Nombre de fichiers Parquet : {len(parquet_parts)}")

        for parquet_file in parquet_parts:
            print(f"- {parquet_file.name}")

    verify_parquet = check_parquet()

    @task
    def upload_to_gcs():
        sys.path.insert(0, "/workspace/src")

        from gcp.upload_to_gcs import upload_parquet_directory

        upload_parquet_directory()

    upload_gcs = upload_to_gcs()

    load_bigquery = GCSToBigQueryOperator(
        task_id="load_to_bigquery",
        bucket="olist-data-lake-farouk-2026",
        source_objects=[
            "processed/sales_dataset.parquet/*.parquet"
        ],
        destination_project_dataset_table=(
            "silken-network-417920.analytics.sales_dataset"
        ),
        source_format="PARQUET",
        autodetect=True,
        create_disposition="CREATE_IF_NEEDED",
        write_disposition="WRITE_TRUNCATE",
        gcp_conn_id="google_cloud_default",
        location="US",
    )

    run_dbt = DockerOperator(
        task_id="run_dbt",
        image="ghcr.io/dbt-labs/dbt-bigquery:1.8.2",
        command=["run"],
        docker_url="unix:///var/run/docker.sock",
        mounts=[
            Mount(
                source=HOST_DBT_PATH,
                target="/usr/app",
                type="bind",
            ),
            Mount(
                source=HOST_DBT_PROFILES_PATH,
                target="/root/.dbt",
                type="bind",
            ),
            Mount(
                source=HOST_DBT_KEYS_PATH,
                target="/root/.keys",
                type="bind",
                read_only=True,
            ),
        ],
        mount_tmp_dir=False,
        auto_remove="success",
        force_pull=False,
    )

    test_dbt = DockerOperator(
        task_id="test_dbt",
        image="ghcr.io/dbt-labs/dbt-bigquery:1.8.2",
        command=["test"],
        docker_url="unix:///var/run/docker.sock",
        mounts=[
            Mount(
                source=HOST_DBT_PATH,
                target="/usr/app",
                type="bind",
            ),
            Mount(
                source=HOST_DBT_PROFILES_PATH,
                target="/root/.dbt",
                type="bind",
            ),
            Mount(
                source=HOST_DBT_KEYS_PATH,
                target="/root/.keys",
                type="bind",
                read_only=True,
            ),
        ],
        mount_tmp_dir=False,
        auto_remove="success",
        force_pull=False,
    )

    (
        check_csv
        >> run_spark
        >> verify_parquet
        >> upload_gcs
        >> load_bigquery
        >> run_dbt
        >> test_dbt
    )


olist_pipeline()