"""
Main API script for Meli Ticket Manager
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Meli Ticket Manager",
    description="""Simplifique o gerenciamento de tickets com nossa API intuitiva.
    Faça perguntas como 'Quantos tickets temos?' ou 'Qual é a prioridade mais alta?' e obtenha respostas claras e imediatas.""",
    version="0.0.0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
