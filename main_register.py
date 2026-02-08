# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
MAIN REGISTER - Entry Point API de Registro
═══════════════════════════════════════════════════════════════════════════════
Inicia a API de registro na porta 8891 (HTTPS)
Autor: Elias Andrade - Arquiteto de Soluções - Replika AI - Maringá/PR
═══════════════════════════════════════════════════════════════════════════════
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import uvicorn

from src.presentation.api.app_factory import create_register_app
from src.infrastructure.crypto.tls_cert_generator import TlsCertGenerator
from src.shared.config import CERTS_DIR, REGISTER_CERT_PATH, REGISTER_KEY_PATH, REGISTER_API_PORT

if __name__ == "__main__":
    try:
        TlsCertGenerator().generate(
            REGISTER_CERT_PATH, REGISTER_KEY_PATH, CERTS_DIR,
            common_name="localhost", org_name="SecureMessenger ZKS"
        )
    except Exception as e:
        print(f"Erro fatal ao criar certificados: {e}")
        sys.exit(1)

    print(f"Iniciando API de Registro na porta {REGISTER_API_PORT}...")
    uvicorn.run(
        create_register_app(),
        host="0.0.0.0",
        port=REGISTER_API_PORT,
        ssl_keyfile=REGISTER_KEY_PATH,
        ssl_certfile=REGISTER_CERT_PATH,
    )
