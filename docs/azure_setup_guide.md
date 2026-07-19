# Azure Setup Guide

## Event Hubs

Create an Event Hubs namespace and event hub for telemetry ingestion. Store the connection string in an environment variable or Databricks secret scope.

## ADLS Gen2

Create a storage account and container for the Delta Lake tables. The Bronze, Silver, and Gold paths should match the values in `.env`.

## Databricks

Attach the cluster to the storage account and configure access to Event Hubs. Use the structured streaming job from the `pyspark/` folder as the base implementation.

Keep secrets out of the repository. Use Azure Key Vault or Databricks secret scopes for credentials.
