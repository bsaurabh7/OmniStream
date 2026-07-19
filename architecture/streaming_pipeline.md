# Streaming Pipeline

```mermaid
flowchart TD
    A[JSON Telemetry] --> B[Event Hubs Producer]
    B --> C[Event Hubs Namespace]
    C --> D[Databricks Structured Streaming]
    D --> E[Schema Validation]
    E --> F[Deduplication]
    F --> G[Watermarking]
    G --> H[Delta Bronze]
    H --> I[Delta Silver]
    I --> J[Delta Gold]
```

The streaming layer is intentionally simple: parse the JSON payload, validate the schema, handle late events with watermarks, and persist the data to Delta Lake in separate stages.
