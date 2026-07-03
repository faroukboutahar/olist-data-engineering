from pyspark.sql import DataFrame
from pyspark.sql.functions import sum as spark_sum


def build_sales_dataset(
    orders_df: DataFrame,
    customers_df: DataFrame,
    order_items_df: DataFrame,
    products_df: DataFrame,
    payments_df: DataFrame,
) -> DataFrame:

    payments_agg_df = (
        payments_df
        .groupBy("order_id")
        .agg(
            spark_sum("payment_value").alias("total_payment_value")
        )
    )

    sales_df = (
        order_items_df
        .join(orders_df, on="order_id", how="left")
        .join(customers_df, on="customer_id", how="left")
        .join(products_df, on="product_id", how="left")
        .join(payments_agg_df, on="order_id", how="left")
    )

    output_path = "/workspace/data/processed/sales_dataset.parquet"

    sales_df.write.mode("overwrite").parquet(output_path)

    print("\n==============================")
    print("Dataset sauvegardé en Parquet")
    print(output_path)
    print("==============================\n")
    return sales_df