# 🏗️ ARQUITETURA - Simple Message Xchanger

**Autor:** Elias Andrade - Arquiteto de Soluções - Replika AI - Maringá/PR  
**Versão:** 1.0.0 | Micro-revisão: 000000001

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Arquitetura DDD](#arquitetura-ddd)
3. [Estrutura de Pastas](#estrutura-de-pastas)
4. [Camadas](#camadas)
5. [Fluxos](#fluxos)
6. [Padrões Utilizados](#padrões-utilizados)

---

## Visão Geral

Sistema de mensageria segura com **Zero Knowledge Proof (ZKP)** para autenticação. O servidor nunca recebe o segredo (chave privada); apenas valida a prova criptográfica.

### Componentes

- **API de Registro** (porta 8891): Cria contas e retorna segredos ao cliente
- **API de Autenticação** (porta 8892): Valida prova ZKP e emite JWT
- **Cliente de Registro**: Cria conta e salva segredos em `user_data/`
- **Cliente de Login**: Gera prova ZKP e obtém token de sessão

---

## Arquitetura DDD

O projeto segue **Domain-Driven Design (DDD)** com camadas bem definidas:

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION                              │
│  API (FastAPI)          │  CLI (Console Clients)            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION                               │
│  CreateAccountUseCase   │  LoginUseCase                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      DOMAIN                                  │
│  Account (Entity)       │  UserId (Value Object)            │
│  verify_proof()         │  Regras de negócio                │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │
┌─────────────────────────────────────────────────────────────┐
│                   INFRASTRUCTURE                             │
│  AccountRepositoryJson  │  KeyPairGenerator                 │
│  ZkpVerifierGenerator   │  JwtTokenGenerator                │
│  TlsCertGenerator       │  ZkpProofGenerator (cliente)      │
└─────────────────────────────────────────────────────────────┘
```

---

## Estrutura de Pastas

```
PROJETO-BASE-POC-CONCEITO-SIMPLE-MESSAGE-XCHANGER/
├── src/
│   ├── domain/                    # Camada de Domínio
│   │   ├── account/
│   │   │   ├── entity.py          # Entidade Account
│   │   │   └── value_objects.py   # UserId, Salt, ZkpVerifier
│   │   └── auth/
│   │
│   ├── application/               # Casos de Uso
│   │   ├── register/
│   │   │   ├── create_account_use_case.py
│   │   │   └── dtos.py
│   │   └── auth/
│   │       ├── login_use_case.py
│   │       └── dtos.py
│   │
│   ├── infrastructure/            # Implementações
│   │   ├── persistence/
│   │   │   └── account_repository_json.py
│   │   ├── crypto/
│   │   │   ├── key_pair_generator.py
│   │   │   ├── zkp_verifier_generator.py
│   │   │   ├── zkp_proof_generator.py
│   │   │   └── tls_cert_generator.py
│   │   └── security/
│   │       └── jwt_service.py
│   │
│   ├── presentation/              # Interface com usuário
│   │   ├── api/
│   │   │   ├── register_router.py
│   │   │   ├── auth_router.py
│   │   │   └── app_factory.py
│   │   └── cli/
│   │       ├── register_client.py
│   │       ├── login_client.py
│   │       └── user_storage.py
│   │
│   └── shared/
│       └── config.py
│
├── api_certs/                     # Certificados TLS
├── user_data/                     # Segredos dos usuários
├── docs/                          # Documentação
│
├── main_register.py               # Entry point API Registro
├── main_auth.py                   # Entry point API Auth
├── client_register.py             # Entry point Cliente Registro
├── client_login.py                # Entry point Cliente Login
├── database.db                    # Persistência JSON
└── requirements.txt
```

---

## Camadas

### Domain
- **Account**: Entidade raiz do agregado. Método `verify_proof()` encapsula validação ZKP.
- **UserId, Salt, ZkpVerifier**: Value Objects imutáveis.

### Application
- **CreateAccountUseCase**: Orquestra geração de chaves, ZKP e persistência.
- **LoginUseCase**: Orquestra busca de conta, validação de prova e emissão de JWT.

### Infrastructure
- **AccountRepositoryJson**: Persistência em arquivo JSON.
- **KeyPairGenerator**: Par EC SECP256R1.
- **ZkpVerifierGenerator**: PBKDF2 para derivar verifier.
- **JwtTokenGenerator**: Tokens JWT para sessão.

### Presentation
- **API**: FastAPI com routers modulares.
- **CLI**: Clientes de console para registro e login.

---

## Fluxos

### Registro
1. Cliente chama `POST /register`
2. CreateAccountUseCase gera UserId, par de chaves, salt e verifier ZKP
3. Account é persistido (apenas public_key, salt, zkp_verifier)
4. Cliente recebe private_key, salt, zkp_verifier e salva em `user_data/{user_id}/`

### Login
1. Cliente carrega secrets de `user_data/{user_id}/secrets.json`
2. Gera prova: `get_hash_proof(private_key, salt)` → proof
3. Envia `POST /login` com `{user_id, proof_of_secret}`
4. LoginUseCase busca Account, chama `account.verify_proof(proof)`
5. Se válido, emite JWT e retorna token

---

## Padrões Utilizados

| Padrão | Aplicação |
|--------|-----------|
| **DDD** | Domain, Application, Infrastructure, Presentation |
| **SOLID** | Dependency Inversion (Protocols/Interfaces) |
| **DRY** | Config centralizado, geradores reutilizáveis |
| **Repository** | AccountRepositoryJson abstrai persistência |
| **Use Case** | CreateAccountUseCase, LoginUseCase |
| **Factory** | create_register_router, create_auth_router |
