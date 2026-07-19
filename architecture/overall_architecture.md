# Overall Architecture

```mermaid
flowchart LR
    Simulator[Vehicle Simulator] --> EventHubs[Azure Event Hubs]
    EventHubs --> Databricks[Azure Databricks Structured Streaming]
    Databricks --> Bronze[Bronze Delta]
    Bronze --> Silver[Silver Delta]
    Silver --> Gold[Gold Delta]
    Gold --> ML[Isolation Forest]
    ML --> Mongo[MongoDB Atlas]
    Gold --> PowerBI[Power BI]
```

This architecture uses a single streaming ingress and a layered lakehouse model so telemetry can be reused for analytics, reporting, and anomaly detection without building separate pipelines for each consumer.
