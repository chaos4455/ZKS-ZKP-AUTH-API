# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
CREATE ACCOUNT USE CASE
═══════════════════════════════════════════════════════════════════════════════
Caso de uso: Criar nova conta com identidade ZKP
Autor: Elias Andrade - Arquiteto de Soluções
═══════════════════════════════════════════════════════════════════════════════
"""

import uuid
from abc import ABC, abstractmethod
from typing import Protocol

from src.domain.account import Account, UserId
from .dtos import RegisterAccountOutput


class IAccountRepository(Protocol):
    """Interface do repositório (Dependency Inversion - SOLID)."""
    def save(self, account: Account) -> None: ...
    def find_by_id(self, user_id: UserId) -> Account | None: ...


class IKeyPairGenerator(Protocol):
    """Interface para geração de par de chaves."""
    def generate(self) -> tuple[str, str]: ...


class IZkpVerifierGenerator(Protocol):
    """Interface para geração do verifier ZKP."""
    def generate(self, private_key_pem: str) -> tuple[str, str]: ...


class CreateAccountUseCase:
    """Caso de uso: Criar conta com ZKP."""

    def __init__(
        self,
        account_repository: IAccountRepository,
        key_pair_generator: IKeyPairGenerator,
        zkp_verifier_generator: IZkpVerifierGenerator,
    ):
        self._repo = account_repository
        self._key_gen = key_pair_generator
        self._zkp_gen = zkp_verifier_generator

    def execute(self) -> RegisterAccountOutput:
        """Executa o fluxo de criação de conta."""
        user_id = UserId(uuid.uuid4())
        private_key, public_key = self._key_gen.generate()
        salt, verifier = self._zkp_gen.generate(private_key)

        account = Account(
            user_id=user_id,
            public_key=public_key,
            salt=salt,
            zkp_verifier=verifier,
        )
        self._repo.save(account)

        return RegisterAccountOutput(
            user_id=user_id.value,
            public_key=public_key,
            private_key=private_key,
            salt=salt,
            zkp_verifier=verifier,
        )
