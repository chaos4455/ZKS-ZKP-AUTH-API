# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
AUTH ROUTER - API de Autenticação
═══════════════════════════════════════════════════════════════════════════════
Endpoint POST /login - Login ZKP e emissão de JWT
Autor: Elias Andrade - Arquiteto de Soluções
═══════════════════════════════════════════════════════════════════════════════
"""

import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.application.auth import LoginUseCase
from src.application.auth.dtos import LoginInput
from src.infrastructure.persistence.account_repository_json import AccountRepositoryJson
from src.infrastructure.security.jwt_service import JwtTokenGenerator
from src.shared.config import JWT_EXPIRATION_MINUTES


class AuthRequest(BaseModel):
    """Schema da requisição de login."""
    user_id: uuid.UUID
    proof_of_secret: str


class AuthResponse(BaseModel):
    """Schema da resposta de login."""
    access_token: str
    token_type: str = "bearer"
    expires_in_minutes: int
    user_id: uuid.UUID


def create_auth_router() -> APIRouter:
    """Factory do router de autenticação."""
    repo = AccountRepositoryJson()
    jwt_gen = JwtTokenGenerator()
    use_case = LoginUseCase(repo, jwt_gen, expires_minutes=JWT_EXPIRATION_MINUTES)

    router = APIRouter(prefix="", tags=["auth"])

    @router.post("/login", response_model=AuthResponse)
    async def login(auth_data: AuthRequest):
        try:
            output = use_case.execute(LoginInput(
                user_id=auth_data.user_id,
                proof_of_secret=auth_data.proof_of_secret,
            ))
            return AuthResponse(
                access_token=output.access_token,
                expires_in_minutes=output.expires_in_minutes,
                user_id=output.user_id,
            )
        except ValueError as e:
            msg = str(e)
            if "não encontrado" in msg.lower():
                raise HTTPException(status_code=404, detail=msg)
            raise HTTPException(status_code=401, detail=msg)

    return router
