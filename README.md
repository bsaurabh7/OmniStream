# OmniStream – Fleet Telemetry & Lakehouse

![OmniStream Banner](images/banner.png)

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/Tests-pytest-green.svg)](https://docs.pytest.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Azure](https://img.shields.io/badge/Azure-Data%20Engineering-orange.svg)](https://azure.microsoft.com/)

## Overview

OmniStream is a data engineering portfolio project that simulates connected vehicle telemetry and processes it through an Azure lakehouse pipeline.

The project demonstrates real-world data engineering concepts:

- Real-time telemetry ingestion
- Spark Structured Streaming
- Delta Lake architecture
- Data cleaning and transformation
- Machine learning anomaly detection
- Operational storage
- BI-ready analytics

The goal is to build a practical streaming data platform similar to systems used in modern fleet monitoring solutions.

---

# Business Problem

Fleet operators collect millions of vehicle events every day. Raw telemetry data is difficult to analyze without proper processing.

OmniStream provides a solution by:

- Collecting vehicle sensor data in real time
- Validating and cleaning incoming events
- Creating analytics-ready datasets
- Detecting abnormal vehicle behavior
- Supporting operational dashboards

---

# Architecture

```
Vehicle Simulator
        |
        v
Azure Event Hubs
        |
        v
Databricks Structured Streaming
        |
        v
+----------------+
| Bronze Delta   |
| Raw Events     |
+----------------+
        |
        v
+----------------+
| Silver Delta   |
| Clean Data     |
+----------------+
        |
        v
+----------------+
| Gold Delta     |
| Business KPIs  |
+----------------+
        |
        +----------------+
        |                |
        v                v
Isolation Forest     Power BI
        |
        v
MongoDB Atlas
```

---

# Technology Stack

## Data Engineering

- Python 3.12
- PySpark
- Azure Event Hubs
- Azure Databricks
- Azure Data Lake Storage Gen2
- Delta Lake

## Machine Learning

- pandas
- NumPy
- scikit-learn
- Isolation Forest

## Storage & Analytics

- MongoDB Atlas
- Power BI

## Development Tools

- Docker
- pytest
- GitHub Actions
- python-dotenv

---

# Repository Structure

```
OmniStream-Fleet-Telemetry-Lakehouse/

├── vehicle_simulator/     # Generates telemetry events
├── streaming/             # Event ingestion components
├── pyspark/               # Spark streaming jobs
├── delta/                 # Bronze, Silver, Gold layers
├── ml/                    # ML anomaly detection
├── mongodb/               # MongoDB integration
├── powerbi/               # Dashboard documentation
├── config/                # Configuration management
├── tests/                 # Automated tests
├── scripts/               # Utility scripts
├── docs/                  # Documentation
└── sample_data/           # Sample telemetry data
```

---

# Data Pipeline

## Bronze Layer

Stores raw vehicle telemetry events.

Example fields:

- Vehicle ID
- Timestamp
- GPS location
- Speed
- Fuel level
- Engine temperature
- Battery status

---

## Silver Layer

Transforms raw events into clean data.

Operations include:

- Schema validation
- Data quality checks
- Deduplication
- Watermark handling
- Data cleaning

---

## Gold Layer

Creates business-ready datasets:

- Fleet health score
- Vehicle performance metrics
- Fuel consumption analysis
- Route statistics
- Daily fleet summaries

---

# Machine Learning

OmniStream uses Isolation Forest for anomaly detection.

The model identifies:

- Abnormal engine temperature
- Sudden fuel changes
- Unexpected speed patterns
- Battery problems

Detected anomalies are stored in MongoDB Atlas for operational analysis.

---

# Installation

## Create Virtual Environment

```bash
python -m venv .venv

source .venv/bin/activate

pip install --upgrade pip

pip install -r requirements.txt
```

For Conda:

```bash
conda env create -f environment.yml

conda activate omnistream
```

---

# Configuration

Create your environment file:

```bash
cp .env.example .env
```

Configure:

- Azure Event Hub connection
- ADLS Gen2 storage
- MongoDB connection
- Application settings

No secrets are stored inside the repository.

---

# Running Locally

Typical execution flow:

### 1. Start services

```bash
docker compose up
```

### 2. Generate telemetry

```bash
python vehicle_simulator/main.py
```

### 3. Run Spark streaming pipeline

```bash
python pyspark/streaming_job.py
```

### 4. Train anomaly detection model

```bash
python ml/train.py
```

### 5. Score new events

```bash
python ml/predict.py
```

---

# Azure Deployment

Cloud architecture includes:

## Azure Event Hubs

Used for real-time vehicle telemetry ingestion.

## Azure Databricks

Used for:

- Structured Streaming
- Spark transformations
- Delta Lake processing

## Azure Data Lake Storage Gen2

Used for:

- Bronze storage
- Silver storage
- Gold analytics tables

## Power BI

Used for fleet dashboards and reporting.

---

# MongoDB Integration

MongoDB Atlas stores anomaly events.

Features include:

- Connection management
- Collection creation
- Index management
- Retry handling
- CRUD operations

---

# Power BI Dashboard

Gold datasets support dashboards for:

- Vehicle count
- Average speed
- Fuel consumption
- Engine temperature
- Battery health
- Fleet health score
- Route analysis
- Anomaly monitoring

---

# Testing

Testing uses pytest.

Test coverage includes:

- Simulator functions
- Spark transformations
- ML modules
- Utility functions

Run tests:

```bash
pytest
```

---

# Future Enhancements

- Add geofencing alerts
- Add route optimization analytics
- Improve anomaly detection models
- Add Databricks notebooks
- Create complete Power BI dashboards
- Add CI/CD deployment pipelines

---

# Learning Outcomes

This project demonstrates:

- Streaming data engineering
- Azure cloud architecture
- Lakehouse design patterns
- Spark Structured Streaming
- Delta Lake implementation
- Machine learning integration
- Production-style project organization

---

# License

MIT License