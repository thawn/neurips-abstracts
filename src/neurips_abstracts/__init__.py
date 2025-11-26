"""
NeurIPS Abstracts Package
==========================

A Python package for downloading NeurIPS conference data and loading it into a SQLite database.

Main Components
---------------
- downloader: Download JSON data from configurable URLs
- database: Load JSON data into SQLite database
- embeddings: Generate and store text embeddings for papers
"""

from .config import Config, get_config
from .downloader import download_json, download_neurips_data
from .database import DatabaseManager
from .embeddings import EmbeddingsManager
from .rag import RAGChat

__version__ = "0.1.0"
__all__ = [
    "Config",
    "get_config",
    "download_json",
    "download_neurips_data",
    "DatabaseManager",
    "EmbeddingsManager",
    "RAGChat",
]
