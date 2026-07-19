# Setup Guide

1. Create and activate a Python 3.12 environment.
2. Install dependencies from `requirements.txt`.
3. Copy `.env.example` to `.env` and fill in Azure and MongoDB values.
4. Generate sample data with `python scripts/generate_sample_data.py`.
5. Run the simulator with `python scripts/run_simulator.py`.
6. Train the model with `python scripts/train_model.py --input sample_data/telemetry_sample.csv`.

This guide keeps the first-time setup intentionally simple so the project can be run locally before moving to Azure services.
