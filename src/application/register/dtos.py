# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
REGISTER DTOs - Data Transfer Objects
═══════════════════════════════════════════════════════════════════════════════
Objetos de transferência para o caso de uso de registro
Autor: Elias Andrade - Arquiteto de Soluções
═══════════════════════════════════════════════════════════════════════════════
"""

import uuid
from dataclasses import dataclass


@dataclass
class RegisterAccountOutput:
    """Output do caso de uso CreateAccount."""
    user_id: uuid.UUID
    public_key: str
    private_key: str
    salt: str
    zkp_verifier: str
    message: str = "Conta criada."
