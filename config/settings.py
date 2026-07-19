"""Backward-compatible settings module for OmniStream."""

from __future__ import annotations

from .config import AppConfig, load_config

__all__ = ["AppConfig", "load_config"]
