# Repository Structure

```mermaid
tree
    root[OmniStream-Fleet-Telemetry-Lakehouse]
    root --> config[config/]
    root --> simulator[vehicle_simulator/]
    root --> streaming[streaming/]
    root --> pyspark[pyspark/]
    root --> delta[delta/]
    root --> ml[ml/]
    root --> mongodb[mongodb/]
    root --> powerbi[powerbi/]
    root --> scripts[scripts/]
    root --> tests[tests/]
    root --> docs[docs/]
    root --> architecture[architecture/]
    root --> sample_data[sample_data/]
```

This structure keeps the code for each layer separate while still making it easy to find the modules that support a specific part of the pipeline.
