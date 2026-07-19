# Deployment Architecture

```mermaid
flowchart TD
    Dev[Local Development] --> Docker[Docker Compose]
    Docker --> Spark[PySpark Container]
    Docker --> Mongo[MongoDB Container]
    Azure[Azure Cloud] --> EH[Event Hubs]
    Azure --> ADLS[ADLS Gen2]
    Azure --> DBX[Databricks]
    Azure --> PBI[Power BI]
```

Local development supports quick validation of the simulator, MongoDB utilities, and PySpark transformation logic. The Azure deployment path matches the same logical flow using managed services.
