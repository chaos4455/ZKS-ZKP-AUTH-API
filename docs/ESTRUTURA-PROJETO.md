# 📁 Estrutura do Projeto - Simple Message Xchanger

**Autor:** Elias Andrade - Replika AI - Maringá/PR

---

## Mapeamento de Arquivos

### Antes (monolítico) → Depois (DDD)

| Arquivo Antigo | Novo Local / Módulo |
|----------------|---------------------|
| SERVER-CREATE-ACCOUNT-API-V1.PY | `main_register.py` + `src/presentation/api/` + `src/application/register/` + `src/infrastructure/` |
| SERVER-AUTH-API-V1.PY | `main_auth.py` + `src/presentation/api/` + `src/application/auth/` + `src/infrastructure/` |
| CONSOLE-APP-API-CREATE-ACCOUNT-TEST-V1.PY | `client_register.py` + `src/presentation/cli/` |
| CONSOLE-APP-CLIENT-LOGIN-TEST-V1.PY | `client_login.py` + `src/presentation/cli/` |

---

## Entry Points

| Comando | Descrição |
|---------|-----------|
| `python main_register.py` | Inicia API de Registro (HTTPS:8891) |
| `python main_auth.py` | Inicia API de Auth (HTTPS:8892) |
| `python client_register.py` | Cria nova conta via API |
| `python client_login.py` | Login via prova ZKP |

---

## Dependências de Pastas

- `api_certs/` - Certificados TLS (gerados automaticamente)
- `user_data/{uuid}/` - Segredos do usuário (private_key, secrets.json, etc.)
- `database.db` - Persistência JSON das contas
