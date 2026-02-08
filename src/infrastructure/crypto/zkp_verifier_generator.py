# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
ZKP VERIFIER GENERATOR
═══════════════════════════════════════════════════════════════════════════════
Deriva o verifier ZKP via PBKDF2 - O servidor nunca vê o segredo
Autor: Elias Andrade - Arquiteto de Soluções
═══════════════════════════════════════════════════════════════════════════════
"""

import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class ZkpVerifierGenerator:
    """Gera salt + verifier a partir da chave privada."""

    def __init__(self, iterations: int = 480_000, length: int = 32):
        self._iterations = iterations
        self._length = length

    def generate(self, private_key_pem: str) -> tuple[str, str]:
        """Retorna (salt_hex, verifier_hex)."""
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=self._length,
            salt=salt,
            iterations=self._iterations,
        )
        key_material = private_key_pem.encode("utf-8")
        verifier_bytes = kdf.derive(key_material)
        return salt.hex(), verifier_bytes.hex()
