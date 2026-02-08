# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
CLIENT LOGIN - Entry Point Cliente de Login
═══════════════════════════════════════════════════════════════════════════════
Autentica via prova ZKP e salva token de sessão
Autor: Elias Andrade - Arquiteto de Soluções - Replika AI - Maringá/PR
═══════════════════════════════════════════════════════════════════════════════
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.presentation.cli.login_client import perform_login

if __name__ == "__main__":
    perform_login()
