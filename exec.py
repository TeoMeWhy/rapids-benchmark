import argparse
import time

import pandas as pd


def pandas_read_csv(n):
    start = time.time()
    df = pd.read_csv(f"data/transactions_{n}.csv", sep=";")
    df.groupby("id_customer").agg({"vl_points": "sum", "uuid":"count"})
    res = time.time() - start
    return res


def pandas_read_parquet(n):
    start = time.time()
    df = pd.read_parquet(f"data/transactions_{n}.parquet")
    df.groupby("id_customer").agg({"vl_points": "sum", "uuid":"count"})
    res = time.time() - start
    return res


def main():

    sizes = [
      1_000_000,
      10_000_000,
      50_000_000,
      100_000_000,
      125_000_000,
      150_000_000,
      200_000_000,
      225_000_000,
      250_000_000,
    ]
        
    parser = argparse.ArgumentParser()
    parser.add_argument("--engine", choices=["pandas", "cudf_pandas"], default="pandas", required=True)
    parser.add_argument("--size", default=sizes[0], required=True, type=int)
    parser.add_argument("--file_format", choices=["parquet", "csv"], default="parquet", required=True)
    args = parser.parse_args()


    execs = {
        "csv":{
            "pandas": pandas_read_csv,
            "cudf_pandas": pandas_read_csv
        },
        "parquet": {
            "pandas": pandas_read_parquet,
            "cudf_pandas": pandas_read_parquet
        }
    }

    res = execs[args.file_format][args.engine](args.size)
    with open("results.txt", "a") as f:
        f.write(f"{args.engine};{args.file_format};{args.size};{res}\n")


if __name__ == "__main__":
    main()