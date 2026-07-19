# Troubleshooting

- If Event Hubs publishing fails, verify the connection string and event hub name.
- If Spark cannot write Delta tables locally, make sure the output directories exist and the checkpoint path is writable.
- If MongoDB connection errors occur, check the Atlas IP allowlist and URI.
- If model scoring fails, verify that the saved joblib file matches the expected feature columns.
