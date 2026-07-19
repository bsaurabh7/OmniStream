# Lessons Learned

- Separate raw ingestion from transformation logic to keep the pipeline easier to debug.
- Keep environment settings in one place so local and Azure runs use the same configuration model.
- Use a simple, explainable anomaly detector before adding more advanced ML approaches.
- Treat Power BI as a consumer of curated outputs rather than raw telemetry.
