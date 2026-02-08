# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
KEY PAIR GENERATOR - Gerador de Par de Chaves EC
═══════════════════════════════════════════════════════════════════════════════
Gera par EC SECP256R1 (P-256) para identidade ZKP
Autor: Elias Andrade - Arquiteto de Soluções
═══════════════════════════════════════════════════════════════════════════════
"""

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization


class KeyPairGenerator:
    """Gera par de chaves EC para ZKP."""

    def generate(self) -> tuple[str, str]:
        """Retorna (private_pem, public_pem)."""
        private_key = ec.generate_private_key(ec.SECP256R1())
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        ).decode("utf-8")
        public_pem = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode("utf-8")
        return private_pem, public_pem
