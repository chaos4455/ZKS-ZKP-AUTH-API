# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
JWT SERVICE
═══════════════════════════════════════════════════════════════════════════════
Gera tokens JWT para sessão autenticada
Autor: Elias Andrade - Arquiteto de Soluções
═══════════════════════════════════════════════════════════════════════════════
"""

import datetime
import jwt

from src.domain.account import UserId
from src.shared.config import JWT_SECRET, JWT_ALGORITHM


class JwtTokenGenerator:
    """Gera tokens JWT."""

    def __init__(self, secret: str = JWT_SECRET, algorithm: str = JWT_ALGORITHM):
        self._secret = secret
        self._algorithm = algorithm

    def generate(self, user_id: UserId, expires_minutes: int = 30) -> str:
        """Gera token JWT para o usuário."""
        now = datetime.datetime.utcnow()
        expiration = now + datetime.timedelta(minutes=expires_minutes)
        payload = {
            "sub": str(user_id.value),
            "exp": expiration,
            "iat": now,
            "type": "access",
        }
        return jwt.encode(payload, self._secret, algorithm=self._algorithm)
