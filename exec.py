import argparse
import time

import pandas as pd


def pandas_csv():
    start = time.time()
    df = pd.read_csv("data/transactions.csv", sep=";")
    df.groupby("id_customer").agg({"vl_points": "sum", "uuid":"count"})
    res = time.time() - start
    return res


def pandas_parquet():
    start = time.time()
    df = pd.read_parquet("data/transactions.parquet")
    df.groupby("id_customer").agg({"vl_points": "sum", "uuid":"count"})
    res = time.time() - start
    return res


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--exec_type", choices=["pandas_csv", "pandas_parquet", "cudf_pandas_parquet", "cudf_pandas_csv"], default="pandas_csv", required=True)
    args = parser.parse_args()

    execs = {
        "pandas_csv": pandas_csv,
        "pandas_parquet": pandas_parquet,
        "cudf_pandas_csv": pandas_csv,
        "cudf_pandas_parquet": pandas_parquet,
    }

    res = execs[args.exec_type]()

    with open("results.txt", "a") as f:
        f.write(f"{args.exec_type};{res}\n")


if __name__ == "__main__":
    main()