"""
Web UI module for NeurIPS Abstracts.

This module provides a Flask-based web interface for exploring
the NeurIPS abstracts database.
"""

from .app import app, run_server

__all__ = ["app", "run_server"]
