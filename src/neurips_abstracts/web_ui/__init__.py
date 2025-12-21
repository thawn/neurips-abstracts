"""
Web UI module for NeurIPS Abstracts.

This module provides a Flask-based web interface for exploring
the NeurIPS abstracts database.

Note: This module requires Flask and related dependencies.
Install with: pip install neurips-abstracts[web]
"""

__all__ = ["app", "run_server"]


def __getattr__(name):
    """
    Lazy-load web UI components to avoid importing Flask unless needed.

    This allows the CLI and other parts of the package to work without
    the web dependencies installed.
    """
    if name in __all__:
        from .app import app, run_server

        if name == "app":
            return app
        elif name == "run_server":
            return run_server
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
