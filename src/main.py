from pyspark.sql import SparkSession

from spark_jobs.build_sales_dataset import build_sales_dataset


def main():

    spark = (
        SparkSession.builder
        .appName("Olist Data Engineering")
        .getOrCreate()
    )

    base_path = "/workspace/data/sample"

    orders_df = spark.read.csv(
        f"{base_path}/olist_orders_dataset.csv",
        header=True,
        inferSchema=True,
    )

    customers_df = spark.read.csv(
        f"{base_path}/olist_customers_dataset.csv",
        header=True,
        inferSchema=True,
    )

    order_items_df = spark.read.csv(
        f"{base_path}/olist_order_items_dataset.csv",
        header=True,
        inferSchema=True,
    )

    products_df = spark.read.csv(
        f"{base_path}/olist_products_dataset.csv",
        header=True,
        inferSchema=True,
    )

    payments_df = spark.read.csv(
        f"{base_path}/olist_order_payments_dataset.csv",
        header=True,
        inferSchema=True,
    )

    sales_df = build_sales_dataset(
        orders_df,
        customers_df,
        order_items_df,
        products_df,
        payments_df,
    )

    print("\n===== SALES DATASET =====")

    print("Nombre de lignes :", sales_df.count())

    sales_df.printSchema()

    sales_df.show(5, truncate=False)

    spark.stop()


if __name__ == "__main__":
    main()