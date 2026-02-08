# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
AUTH DTOs - Data Transfer Objects
═══════════════════════════════════════════════════════════════════════════════
Objetos de transferência para autenticação
Autor: Elias Andrade - Arquiteto de Soluções
═══════════════════════════════════════════════════════════════════════════════
"""

import uuid
from dataclasses import dataclass


@dataclass
class LoginInput:
    """Input do caso de uso Login."""
    user_id: uuid.UUID
    proof_of_secret: str


@dataclass
class LoginOutput:
    """Output do caso de uso Login."""
    access_token: str
    token_type: str = "bearer"
    expires_in_minutes: int = 30
    user_id: uuid.UUID = None
