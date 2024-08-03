"""Create a TestClient instance for the FastAPI application."""

import os
import sys
from importlib import import_module
from fastapi.testclient import TestClient


def create_client():
    """Create a TestClient instance for the FastAPI application.

    Returns:
        TestClient: A TestClient instance for the FastAPI application.
    """
    app_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    sys.path.insert(0, app_root)

    try:
        app = import_module("app.main").app
    except ImportError:
        sys.path.insert(0, os.path.join(app_root, "app"))
        app = import_module("main").app

    client = TestClient(app)
    return client
