"""Shared pytest fixtures."""

from __future__ import annotations

import os

import pytest

pytest.importorskip("pyspark")

from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark() -> SparkSession:
    """Create a local Spark session for transformation tests."""

    os.environ.setdefault("SPARK_LOCAL_HOSTNAME", "localhost")
    session = (
        SparkSession.builder.master("local[1]")
        .appName("omnistream-tests")
        .config("spark.ui.showConsoleProgress", "false")
        .getOrCreate()
    )
    yield session
    session.stop()
