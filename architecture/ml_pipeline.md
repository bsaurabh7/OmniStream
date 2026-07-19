# Machine Learning Pipeline

```mermaid
flowchart TD
    A[Silver Delta] --> B[Feature Engineering]
    B --> C[Isolation Forest Training]
    C --> D[Persist joblib Model]
    D --> E[Batch Scoring]
    E --> F[MongoDB Anomaly Storage]
```

The anomaly detection workflow is designed as a small, explainable layer built on top of the Silver data. The model flags unusual telemetry patterns that can be investigated operationally.
