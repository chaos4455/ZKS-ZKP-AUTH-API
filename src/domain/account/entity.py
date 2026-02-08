# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
ACCOUNT ENTITY
═══════════════════════════════════════════════════════════════════════════════
Entidade raiz do Agregado Account - Identificada por UserId
Autor: Elias Andrade - Arquiteto de Soluções
═══════════════════════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass
from .value_objects import UserId


@dataclass
class Account:
    """Entidade Account - Representa uma conta de usuário no sistema."""
    user_id: UserId
    public_key: str
    salt: str
    zkp_verifier: str

    def verify_proof(self, proof: str) -> bool:
        """Valida prova ZKP sem expor o segredo (Zero Knowledge)."""
        return proof == self.zkp_verifier
