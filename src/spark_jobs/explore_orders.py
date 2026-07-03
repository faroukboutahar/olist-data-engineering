from pyspark.sql.functions import col


def explore_orders(orders_df):
    print("Nombre total de commandes :")
    print(orders_df.count())

    print("\nStatuts disponibles :")
    orders_df.select("order_status").distinct().show()

    print("\nNombre de commandes par statut :")
    (
        orders_df
        .groupBy("order_status")
        .count()
        .orderBy("count", ascending=False)
        .show()
    )

    delivered_df = orders_df.filter(col("order_status") == "delivered")

    print("\nNombre de commandes livrées :")
    print(delivered_df.count())