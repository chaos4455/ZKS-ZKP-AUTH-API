# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
REGISTER ROUTER - API de Registro
═══════════════════════════════════════════════════════════════════════════════
Endpoint POST /register - Criação de conta ZKP
Autor: Elias Andrade - Arquiteto de Soluções
═══════════════════════════════════════════════════════════════════════════════
"""

import uuid
from fastapi import APIRouter
from pydantic import BaseModel

from src.application.register import CreateAccountUseCase
from src.application.register.dtos import RegisterAccountOutput
from src.infrastructure.persistence.account_repository_json import AccountRepositoryJson
from src.infrastructure.crypto.key_pair_generator import KeyPairGenerator
from src.infrastructure.crypto.zkp_verifier_generator import ZkpVerifierGenerator


class RegisterResponse(BaseModel):
    """Schema da resposta da API."""
    user_id: uuid.UUID
    public_key: str
    private_key: str
    salt: str
    zkp_verifier: str
    message: str = "Conta criada."


def create_register_router() -> APIRouter:
    """Factory do router de registro."""
    repo = AccountRepositoryJson()
    key_gen = KeyPairGenerator()
    zkp_gen = ZkpVerifierGenerator()
    use_case = CreateAccountUseCase(repo, key_gen, zkp_gen)

    router = APIRouter(prefix="", tags=["register"])

    @router.post("/register", response_model=RegisterResponse, status_code=201)
    async def create_account():
        output: RegisterAccountOutput = use_case.execute()
        return RegisterResponse(
            user_id=output.user_id,
            public_key=output.public_key,
            private_key=output.private_key,
            salt=output.salt,
            zkp_verifier=output.zkp_verifier,
        )

    return router
