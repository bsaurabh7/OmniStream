# Deployment Guide

## Local

Use Docker Compose to start Spark, MongoDB, and the optional Jupyter environment.

## Azure

- Publish telemetry to Event Hubs.
- Run the Databricks job for the streaming transformations.
- Store Delta outputs in ADLS Gen2.
- Persist anomaly records to MongoDB Atlas.
- Connect Power BI to the Gold outputs.

The deployment plan mirrors the repository structure so each folder maps to one part of the pipeline.
