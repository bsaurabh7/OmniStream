# FAQ

## Why use a lakehouse structure?

It keeps raw, cleaned, and business-ready data separate while still using one streaming ingestion path.

## Why use Isolation Forest?

It is a lightweight, explainable anomaly detection method that works well for unsupervised telemetry patterns.

## Can this scale beyond 10,000 vehicles?

Yes. The simulator, Event Hubs ingestion, and Delta writes are all designed around batch and stream processing patterns that can scale horizontally.
