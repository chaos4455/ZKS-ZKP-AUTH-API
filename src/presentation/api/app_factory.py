# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
APP FACTORY - Criação das aplicações FastAPI
═══════════════════════════════════════════════════════════════════════════════
Factory para Register API e Auth API (separadas por porta)
Autor: Elias Andrade - Arquiteto de Soluções
═══════════════════════════════════════════════════════════════════════════════
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .register_router import create_register_router
from .auth_router import create_auth_router


@asynccontextmanager
async def _lifespan(app: FastAPI):
    """Lifespan - startup/shutdown da aplicação."""
    yield


def create_register_app() -> FastAPI:
    """Cria app FastAPI para API de Registro."""
    app = FastAPI(title="API Registro ZKP", lifespan=_lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["POST"],
        allow_headers=["*"],
    )
    app.include_router(create_register_router())
    return app


def create_auth_app() -> FastAPI:
    """Cria app FastAPI para API de Auth."""
    app = FastAPI(title="API Auth ZKS", lifespan=_lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(create_auth_router())
    return app
