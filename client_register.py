# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
CLIENT REGISTER - Entry Point Cliente de Registro
═══════════════════════════════════════════════════════════════════════════════
Cria nova conta via API e salva segredos localmente
Autor: Elias Andrade - Arquiteto de Soluções - Replika AI - Maringá/PR
═══════════════════════════════════════════════════════════════════════════════
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.presentation.cli.register_client import register_new_account

if __name__ == "__main__":
    register_new_account()
