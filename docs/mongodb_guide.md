# MongoDB Guide

- Create a MongoDB Atlas cluster.
- Create a database named `omnistream` and a collection named `anomalies`.
- Add indexes on `vehicle_id`, `timestamp`, `trip_id`, and `anomaly_type`.
- Store only anomaly events and operational metadata in MongoDB.

The repository includes a small connection manager and repository wrapper so the persistence logic stays isolated from the ML scoring code.
