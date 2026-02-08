# 🔐 Simple Message Xchanger - POC ZKP

**Autor:** Elias Andrade - Arquiteto de Soluções - Replika AI - Maringá/PR  
**Arquitetura:** DDD | SOLID | Clean Architecture

---

## 📌 Sobre

Sistema de mensageria segura com **Zero Knowledge Proof (ZKP)**. O servidor valida a prova criptográfica sem jamais receber o segredo (chave privada).

---

## 🚀 Como Executar

### 1. Instalar dependências

```powershell
pip install -r requirements.txt
```

### 2. Iniciar as APIs (em terminais separados)

```powershell
# Terminal 1 - API de Registro (porta 8891)
python main_register.py

# Terminal 2 - API de Autenticação (porta 8892)
python main_auth.py
```

### 3. Usar os clientes

```powershell
# Criar nova conta (com API de Registro rodando)
python client_register.py

# Fazer login (com API Auth rodando)
python client_login.py
```

---

## 📂 Estrutura DDD

```
src/
├── domain/          # Entidades, Value Objects
├── application/     # Use Cases (CreateAccount, Login)
├── infrastructure/  # Repositório, Crypto, JWT, TLS
├── presentation/    # API FastAPI + CLI
└── shared/          # Config centralizado
```

Consulte [`docs/ARQUITETURA.md`](docs/ARQUITETURA.md) para detalhes.

---

## 📄 Entry Points

| Arquivo | Descrição |
|---------|-----------|
| `main_register.py` | API de Registro (HTTPS:8891) |
| `main_auth.py` | API de Autenticação (HTTPS:8892) |
| `client_register.py` | Cliente para criar conta |
| `client_login.py` | Cliente para login ZKP |

---

## 🔒 Segurança

- **ZKP:** Prova PBKDF2 derivada da chave privada (480.000 iterações)
- **HTTPS:** Certificados TLS auto-assinados
- **JWT:** Tokens de sessão com expiração
