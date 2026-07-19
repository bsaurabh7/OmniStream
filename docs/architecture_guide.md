# Architecture Guide

OmniStream follows a simple Kappa-style pattern:

1. Generate telemetry from a simulator.
2. Publish the stream to Azure Event Hubs.
3. Consume and transform the data in Databricks.
4. Store raw and curated outputs in Delta Lake.
5. Train and apply an Isolation Forest model.
6. Persist anomalies in MongoDB Atlas.
7. Expose Gold outputs to Power BI.

The design keeps one source of truth for telemetry and reuses the same event schema across the entire pipeline.
