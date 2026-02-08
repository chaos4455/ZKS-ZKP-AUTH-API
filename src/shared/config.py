# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
SHARED CONFIG - Configurações Centralizadas
═══════════════════════════════════════════════════════════════════════════════
Configurações globais do projeto (DRY - Single Source of Truth)
Autor: Elias Andrade - Arquiteto de Soluções - Replika AI
═══════════════════════════════════════════════════════════════════════════════
"""

import os
from pathlib import Path

# Path raiz do projeto
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# API
REGISTER_API_PORT = 8891
AUTH_API_PORT = 8892
CERTS_DIR = str(PROJECT_ROOT / "api_certs")
REGISTER_CERT_PATH = os.path.join(CERTS_DIR, "register_cert.pem")
REGISTER_KEY_PATH = os.path.join(CERTS_DIR, "register_key.key")
AUTH_CERT_PATH = os.path.join(CERTS_DIR, "auth_cert.pem")
AUTH_KEY_PATH = os.path.join(CERTS_DIR, "auth_key.key")

# Persistência
DB_FILE = str(PROJECT_ROOT / "database.db")
USER_DATA_DIR = str(PROJECT_ROOT / "user_data")

# JWT
JWT_SECRET = os.environ.get("JWT_SECRET", "UMA_CHAVE_SUPER_SECRETA_FIXA_PARA_TESTES")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 30

# URLs (para clientes)
REGISTER_API_URL = f"https://localhost:{REGISTER_API_PORT}/register"
AUTH_API_URL = f"https://localhost:{AUTH_API_PORT}/login"
