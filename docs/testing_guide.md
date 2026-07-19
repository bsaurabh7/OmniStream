# Testing Guide

Run the test suite with:

```bash
pytest
```

Recommended test areas:

- telemetry generator output
- PySpark transformation helpers
- Isolation Forest training and scoring
- MongoDB repository methods with mocked collections
- command-line scripts for sample-data generation

Coverage should focus on the business logic that can be validated locally without Azure resources.
