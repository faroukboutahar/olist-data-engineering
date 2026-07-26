# Docker

This directory contains the Docker configuration used to reproduce the
Spark execution environment of the Olist data engineering pipeline.

## Spark image

The `Dockerfile.spark` image contains:

- Ubuntu 24.04
- Java 17
- Python 3
- PySpark 3.5.1
- The Python source code of the pipeline

## Build

Run the following command from the root of the repository:

```bash
docker build -f Docker/Dockerfile.spark -t olist-spark:1.0 .