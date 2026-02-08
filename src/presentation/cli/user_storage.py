# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
USER STORAGE - Armazenamento local de segredos do usuário
═══════════════════════════════════════════════════════════════════════════════
Salva e carrega secrets.json, chaves, session_token
Autor: Elias Andrade - Arquiteto de Soluções
═══════════════════════════════════════════════════════════════════════════════
"""

import json
import os
import uuid
import datetime
from typing import Any, Dict, Optional

from src.shared.config import USER_DATA_DIR


def store_user_secrets(user_data: Dict[str, Any]) -> None:
    """Salva segredos do usuário em user_data/{user_id}/."""
    user_id = str(user_data["user_id"])
    user_dir = os.path.join(USER_DATA_DIR, user_id)
    os.makedirs(user_dir, exist_ok=True)

    print(f"\n--- Salvando segredos para o usuário ID: {user_id} ---")

    data_to_save = {k: v for k, v in user_data.items() if k != "message"}
    if "user_id" in data_to_save:
        data_to_save["user_id"] = str(data_to_save["user_id"])

    json_path = os.path.join(user_dir, "secrets.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data_to_save, f, indent=4)
    print(f"  [OK] Segredos salvos em JSON: {json_path}")

    yaml_path = os.path.join(user_dir, "secrets.yaml")
    try:
        import yaml
        with open(yaml_path, "w", encoding="utf-8") as f:
            yaml.dump(data_to_save, f, default_flow_style=False)
        print(f"  [OK] Segredos salvos em YAML: {yaml_path}")
    except ImportError:
        pass

    private_key_path = os.path.join(user_dir, "private_key.key")
    with open(private_key_path, "w", encoding="utf-8") as f:
        f.write(user_data["private_key"])
    print(f"  [OK] Chave Privada (SEGREDO) salva: {private_key_path}")

    public_key_path = os.path.join(user_dir, "public_key.pem")
    with open(public_key_path, "w", encoding="utf-8") as f:
        f.write(user_data["public_key"])
    print(f"  [OK] Chave Pública salva: {public_key_path}")

    summary_path = os.path.join(user_dir, "summary.txt")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(f"--- Dados Essenciais de Login ---\n")
        f.write(f"User ID: {user_id}\n")
        f.write(f"Salt: {user_data['salt']}\n")
        f.write(f"ZKP Verifier: {user_data['zkp_verifier']}\n")
        f.write(f"\nATENÇÃO: A private_key.key é sua senha mestra. Não a compartilhe.\n")
    print(f"  [OK] Resumo salvo em TXT: {summary_path}")


def find_local_user() -> Optional[str]:
    """Procura primeiro diretório UUID válido em user_data."""
    if not os.path.exists(USER_DATA_DIR):
        return None
    for item in os.listdir(USER_DATA_DIR):
        path = os.path.join(USER_DATA_DIR, item)
        if os.path.isdir(path):
            try:
                uuid.UUID(item)
                return item
            except ValueError:
                continue
    return None


def load_user_secrets(user_id: str) -> Optional[Dict[str, Any]]:
    """Carrega secrets.json do usuário."""
    path = os.path.join(USER_DATA_DIR, user_id, "secrets.json")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_session_token(user_id: str, auth_response: Dict[str, Any]) -> None:
    """Salva token JWT em session_token.json."""
    user_dir = os.path.join(USER_DATA_DIR, user_id)
    token_path = os.path.join(user_dir, "session_token.json")
    data = {
        "access_token": auth_response["access_token"],
        "expires_in_minutes": auth_response["expires_in_minutes"],
        "created_at": str(datetime.datetime.now()),
        "token_type": auth_response.get("token_type", "bearer"),
    }
    with open(token_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"  [DISK] Token de sessão salvo em: {token_path}")
