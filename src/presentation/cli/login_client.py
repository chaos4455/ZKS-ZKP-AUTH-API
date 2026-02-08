# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
LOGIN CLIENT - Cliente de Login ZKP
═══════════════════════════════════════════════════════════════════════════════
Gera prova ZKP e envia para API de Auth
Autor: Elias Andrade - Arquiteto de Soluções
═══════════════════════════════════════════════════════════════════════════════
"""

import requests
import urllib3

from src.shared.config import AUTH_API_URL
from src.infrastructure.crypto.zkp_proof_generator import get_hash_proof
from .user_storage import find_local_user, load_user_secrets, save_session_token

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def perform_login() -> None:
    """Fluxo de login ZKP."""
    print("\n--- INICIANDO PROCESSO DE LOGIN ZKS (CLIENTE) ---")

    user_id = find_local_user()
    if not user_id:
        print("ERRO: Nenhum usuário encontrado na pasta 'user_data'.")
        print("Execute o cliente de registro primeiro para criar uma conta.")
        return

    print(f"1. Usuário identificado localmente: {user_id}")

    secrets = load_user_secrets(user_id)
    if not secrets:
        print(f"ERRO: Não foi possível ler os segredos para {user_id}.")
        return

    print("2. Gerando prova matemática usando a Chave Privada Local...")
    try:
        proof = get_hash_proof(secrets["private_key"], secrets["salt"])
    except Exception as e:
        print(f"ERRO CRÍTICO ao gerar prova: {e}")
        return

    payload = {"user_id": user_id, "proof_of_secret": proof}
    print(f"3. Conectando ao Servidor de Autenticação ({AUTH_API_URL})...")

    try:
        response = requests.post(AUTH_API_URL, json=payload, verify=False)

        if response.status_code == 404:
            print("\n[ERRO 404] O Servidor não encontrou este User ID.")
            return
        elif response.status_code == 401:
            print("\n[ERRO 401] Falha na Prova ZKS.")
            return

        response.raise_for_status()
        auth_data = response.json()
        token = auth_data["access_token"]

        print("\n>>> SUCESSO: LOGIN REALIZADO! <<<")
        print(f"Servidor validou a autoridade sem receber a senha.")
        print(f"Token JWT Recebido: {token[:30]}...")
        save_session_token(user_id, auth_data)

    except requests.exceptions.ConnectionError:
        print("\n[ERRO DE CONEXÃO] Não foi possível conectar. Verifique se a API Auth está rodando.")
    except Exception as e:
        print(f"\n[ERRO INESPERADO] {e}")
