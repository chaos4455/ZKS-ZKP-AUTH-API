# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
LOGIN USE CASE
═══════════════════════════════════════════════════════════════════════════════
Caso de uso: Autenticar usuário via prova ZKP e emitir JWT
Autor: Elias Andrade - Arquiteto de Soluções
═══════════════════════════════════════════════════════════════════════════════
"""

from typing import Protocol

from src.domain.account import Account, UserId
from .dtos import LoginInput, LoginOutput


class IAccountRepository(Protocol):
    """Interface do repositório."""
    def find_by_id(self, user_id: UserId) -> Account | None: ...
    def reload(self) -> None: ...


class IJwtTokenGenerator(Protocol):
    """Interface para geração de JWT."""
    def generate(self, user_id: UserId, expires_minutes: int) -> str: ...


class LoginUseCase:
    """Caso de uso: Login com prova ZKP."""

    def __init__(
        self,
        account_repository: IAccountRepository,
        jwt_generator: IJwtTokenGenerator,
        expires_minutes: int = 30,
    ):
        self._repo = account_repository
        self._jwt = jwt_generator
        self._expires = expires_minutes

    def execute(self, input_data: LoginInput) -> LoginOutput:
        """Executa o fluxo de login."""
        user_id = UserId(input_data.user_id)
        account = self._repo.find_by_id(user_id)

        if not account:
            self._repo.reload()
            account = self._repo.find_by_id(user_id)

        if not account:
            raise ValueError("User ID não encontrado. Você registrou a conta?")

        if not account.verify_proof(input_data.proof_of_secret):
            raise ValueError("Prova ZKP inválida.")

        token = self._jwt.generate(user_id, self._expires)
        return LoginOutput(
            access_token=token,
            expires_in_minutes=self._expires,
            user_id=user_id.value,
        )
