from pyspark.sql import SparkSession


def main():
    spark = (
        SparkSession.builder
        .appName("Olist Data Engineering")
        .getOrCreate()
    )

    print("===================================")
    print(" Spark fonctionne correctement !")
    print("===================================")

    spark.stop()


if __name__ == "__main__":
    main()