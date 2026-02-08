# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
MAIN AUTH - Entry Point API de Autenticação
═══════════════════════════════════════════════════════════════════════════════
Inicia a API de auth na porta 8892 (HTTPS)
Autor: Elias Andrade - Arquiteto de Soluções - Replika AI - Maringá/PR
═══════════════════════════════════════════════════════════════════════════════
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import uvicorn

from src.presentation.api.app_factory import create_auth_app
from src.infrastructure.crypto.tls_cert_generator import TlsCertGenerator
from src.shared.config import CERTS_DIR, AUTH_CERT_PATH, AUTH_KEY_PATH, AUTH_API_PORT

if __name__ == "__main__":
    try:
        TlsCertGenerator().generate(AUTH_CERT_PATH, AUTH_KEY_PATH, CERTS_DIR)
    except Exception:
        pass

    print(f"Auth API rodando em HTTPS://localhost:{AUTH_API_PORT}")
    uvicorn.run(
        create_auth_app(),
        host="0.0.0.0",
        port=AUTH_API_PORT,
        ssl_keyfile=AUTH_KEY_PATH,
        ssl_certfile=AUTH_CERT_PATH,
    )
