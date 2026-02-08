# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
ZKP PROOF GENERATOR (CLIENTE)
═══════════════════════════════════════════════════════════════════════════════
Gera a prova de posse no cliente - usa os mesmos parâmetros do servidor
Autor: Elias Andrade - Arquiteto de Soluções
═══════════════════════════════════════════════════════════════════════════════
"""

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def get_hash_proof(private_key_pem: str, salt_hex: str) -> str:
    """
    Gera a PROVA DE POSSE (ZKP).
    Parâmetros idênticos ao servidor (PBKDF2-SHA256, 32 bytes, 480000 iterations).
    """
    salt = bytes.fromhex(salt_hex)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480_000,
    )
    key_material = private_key_pem.encode("utf-8")
    proof_bytes = kdf.derive(key_material)
    return proof_bytes.hex()
