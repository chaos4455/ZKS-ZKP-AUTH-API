# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
ACCOUNT REPOSITORY JSON
═══════════════════════════════════════════════════════════════════════════════
Implementação do repositório de contas usando JSON em disco
Autor: Elias Andrade - Arquiteto de Soluções
═══════════════════════════════════════════════════════════════════════════════
"""

import json
import os
import uuid

from src.domain.account import Account, UserId
from src.shared.config import DB_FILE


class AccountRepositoryJson:
    """Repositório de Account persistido em JSON."""

    def __init__(self, db_path: str = DB_FILE):
        self._db_path = db_path
        self._cache: dict[uuid.UUID, dict] = {}

    def _load(self) -> None:
        """Carrega DB do disco para cache."""
        if os.path.exists(self._db_path):
            try:
                with open(self._db_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._cache = {uuid.UUID(k): v for k, v in data.items()}
            except Exception as e:
                print(f"DB vazio ou corrompido: {e}")

    def _save(self) -> None:
        """Persiste cache no disco."""
        with open(self._db_path, "w", encoding="utf-8") as f:
            serializable = {str(k): v for k, v in self._cache.items()}
            json.dump(serializable, f, indent=4)

    def save(self, account: Account) -> None:
        """Persiste conta."""
        self._load()
        self._cache[account.user_id.value] = {
            "public_key": account.public_key,
            "salt": account.salt,
            "zkp_verifier": account.zkp_verifier,
        }
        self._save()

    def find_by_id(self, user_id: UserId) -> Account | None:
        """Busca conta por ID."""
        self._load()
        raw = self._cache.get(user_id.value)
        if not raw:
            return None
        return Account(
            user_id=user_id,
            public_key=raw["public_key"],
            salt=raw["salt"],
            zkp_verifier=raw["zkp_verifier"],
        )

    def reload(self) -> None:
        """Recarrega DB do disco (para sincronizar entre APIs)."""
        self._load()
