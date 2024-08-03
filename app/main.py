"""
Main API script for Meli Ticket Manager
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router
from app.infrastructure import create_sysadmin


create_sysadmin()

app = FastAPI(
    title="Meli Ticket Manager",
    description="""Simplifique o gerenciamento de tickets com essa API intuitiva.""",
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
