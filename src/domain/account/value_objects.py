# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
ACCOUNT VALUE OBJECTS
═══════════════════════════════════════════════════════════════════════════════
Value Objects do Agregado Account - Imutáveis, identificados por atributos
Autor: Elias Andrade - Arquiteto de Soluções
═══════════════════════════════════════════════════════════════════════════════
"""

import uuid
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class UserId:
    """Value Object - Identificador único do usuário (UUID)."""
    value: uuid.UUID

    def __post_init__(self):
        if not isinstance(self.value, uuid.UUID):
            object.__setattr__(self, 'value', uuid.UUID(str(self.value)))

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class ZkpVerifier:
    """Value Object - Verificador ZKP (prova derivada, nunca o segredo)."""
    value: str


@dataclass(frozen=True)
class Salt:
    """Value Object - Salt para KDF (PBKDF2)."""
    hex_value: str
