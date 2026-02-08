# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
REGISTER CLIENT - Cliente de Registro
═══════════════════════════════════════════════════════════════════════════════
Chama API de registro e salva segredos localmente
Autor: Elias Andrade - Arquiteto de Soluções
═══════════════════════════════════════════════════════════════════════════════
"""

import requests
import urllib3

from src.shared.config import REGISTER_API_URL
from .user_storage import store_user_secrets

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def register_new_account() -> None:
    """Fluxo de registro de nova conta."""
    print(f"Tentando conectar à API de Registro em {REGISTER_API_URL}...")
    try:
        response = requests.post(REGISTER_API_URL, verify=False)
        response.raise_for_status()
        user_data = response.json()

        user_data["user_id"] = str(user_data["user_id"])
        print("\n--- Resposta da API de Registro Recebida ---")
        print(f"Mensagem do Servidor: {user_data.get('message', 'Conta registrada.')}")
        print(f"Novo User ID: {user_data['user_id']}")

        store_user_secrets(user_data)
        print("\nRegistro concluído. O usuário possui agora o segredo necessário para o login ZKP.")
    except requests.exceptions.ConnectionError:
        print("\nERRO: Falha na conexão. Certifique-se de que a API de registro esteja rodando em HTTPS.")
    except requests.exceptions.RequestException as e:
        print(f"\nERRO na Requisição: {e}")
