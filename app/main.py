"""
Main API script for Meli Ticket Manager.

This module initializes and configures the FastAPI application, including the setup
of middleware, routing, and initial database records. It ensures the necessary
elements like the sysadmin user, severities, categories, and subcategories are
created if they do not exist in the database.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router
from app.infrastructure import create_sysadmin, create_categories, create_severities, create_subcategories

create_sysadmin()
create_severities()
create_categories()
create_subcategories()

app = FastAPI(
    title="Meli Ticket Manager",
    description="Simplifique o gerenciamento de tickets com essa API intuitiva.",
    version="0.0.0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
