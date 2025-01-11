rm results.txt

for i in {1..12}
do
    python -m cudf.pandas exec.py --exec_type cudf_pandas_csv
    python -m cudf.pandas exec.py --exec_type cudf_pandas_parquet
    python exec.py --exec_type pandas_parquet
    python exec.py --exec_type pandas_csv
done

python analysis.py