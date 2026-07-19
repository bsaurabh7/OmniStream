# Delta Lake Pipeline

```mermaid
flowchart LR
    Raw[Raw Stream] --> Bronze[Bronze]
    Bronze --> Silver[Silver]
    Silver --> Gold[Gold]
    Gold --> BI[Power BI]
```

- Bronze stores raw telemetry with minimal transformation.
- Silver normalizes, validates, and deduplicates the records.
- Gold exposes KPI-ready aggregations for reporting and dashboarding.
