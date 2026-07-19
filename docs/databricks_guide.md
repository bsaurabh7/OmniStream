# Databricks Guide

- Use a cluster with Python 3.12-compatible libraries.
- Install PySpark, Delta Lake, pandas, NumPy, and scikit-learn.
- Run the streaming notebook or job using the explicit schemas in `pyspark/schemas.py`.
- Configure checkpoint paths before enabling streaming writes.
- Use the `delta/` modules as the logical write targets for Bronze, Silver, and Gold.

The Databricks job should follow the same transformation steps as the local code so the logic remains consistent between development and cloud execution.
