# 🔐 Simple Message Xchanger - PoC Zero Knowledge Authentication

<!-- Badges (Orange style requested) -->
[![Project Type](https://img.shields.io/badge/Status-Proof%20of%20Concept-orange?style=for-the-badge)](https://github.com/EliasAndrade)
[![Architecture](https://img.shields.io/badge/Arquitetura-DDD%20%7C%20Clean%20Architecture-orange?style=for-the-badge)](https://github.com/EliasAndrade)
[![Authentication](https://img.shields.io/badge/M%C3%A9todo-Zero%20Knowledge%20Proof%20(ZKP)-orange?style=for-the-badge)](https://en.wikipedia.org/wiki/Zero-knowledge_proof)
[![Concept](https://img.shields.io/badge/Foco-Blind%20Proof%20of%20Authority-orange?style=for-the-badge)](https://github.com/EliasAndrade)
[![Framework](https://img.shields.io/badge/API-FastAPI-orange?style=for-the-badge)](https://fastapi.tiangolo.com/)
[![Language](https://img.shields.io/badge/Linguagem-Python%203.10+-orange?style=for-the-badge)](https://www.python.org/)

***

## 🌟 O Que É Este Projeto?

Este é um **Portfólio de Prova de Conceito (PoC)** que demonstra uma arquitetura completa para **Autenticação de Posse Cega (Blind Proof of Authority)**, utilizando o princípio de **Zero Knowledge Proof (ZKP)** aplicado via **Key Derivation Function (PBKDF2)**.

O objetivo principal é ilustrar uma solução onde o servidor (API de Auth) pode verificar criptograficamente que o cliente possui o segredo correto, **sem jamais receber a senha ou chave privada real**.

### 💡 Casos de Uso e Lógica

1.  **Registro (Cliente):** O cliente gera um par de chaves EC e usa a chave privada para derivar um verificador ZKP (`zkp_verifier`) e um `salt`. Apenas o `salt` e o `zkp_verifier` são enviados e persistidos na `Register API`. A chave privada (o segredo mestre) permanece **somente** no lado do cliente.
2.  **Login (Cliente):** Para autenticar, o cliente usa sua chave privada local, combinada com o `salt` salvo, para gerar uma `proof_of_secret` (A Prova ZKP).
3.  **Verificação (Servidor):** A `Auth API` recebe a `proof_of_secret` e simplesmente a compara com o `zkp_verifier` armazenado. Se coincidirem, o login é válido, e um JWT é emitido. O servidor nunca viu a chave privada.

Este método de autoridade cega (Blind Proof of Authority) é um forte pilar para sistemas onde a confiança na custódia de segredos deve ser zero.

## 📐 Arquitetura DDD & Clean

O projeto é estruturado em camadas seguindo o design **Domain-Driven Design (DDD)** e **Clean Architecture**, garantindo total separação de responsabilidades e aplicando os princípios **SOLID**.

| Camada | Detalhe | Classes/Componentes Principais |
| :--- | :--- | :--- |
| **`domain/`** | Agregado `Account`, VOs (`UserId`). Define as regras de verificação ZKP. | `Account`, `UserId` |
| **`application/`** | Core Business Logic. Define os Use Cases. | `LoginUseCase`, `CreateAccountUseCase` |
| **`infrastructure/`** | Implementações concretas de interfaces (`Protocolos`). | `AccountRepositoryJson`, `JwtTokenGenerator`, `ZkpVerifierGenerator` |
| **`presentation/`** | Interfaces externas (APIs e CLIs). | `auth_router.py`, `login_client.py` |

## ⚙️ Componentes e Fluxo de Execução

O sistema é dividido em duas APIs independentes (simulando microsserviços) e dois clientes console.

| Arquivo (Entry Point) | Função Primária | Detalhe Criptográfico |
| :--- | :--- | :--- |
| `main_register.py` | **API de Registro** (`HTTPS:8891`) | Recebe `public_key`, armazena `zkp_verifier` (verificador). |
| `main_auth.py` | **API de Autenticação** (`HTTPS:8892`) | Verifica a `proof_of_secret` contra o `zkp_verifier` e emite JWT. |
| `client_register.py` | **Cliente de Criação** | Gera `private_key` (segredo) e a identidade EC. Salva segredos localmente (`user_data/`). |
| `client_login.py` | **Cliente de Login ZKP** | Calcula a prova (`PBKDF2`) usando a chave local e envia a prova à `Auth API`. |

## 🔒 Segurança Implementada

- **Zero Knowledge Proof (ZKP):** O segredo do usuário (Private Key) nunca é transmitido ou armazenado no servidor.
- **KDF Robusta:** Utiliza **PBKDF2-HMAC-SHA256** com 480.000 iterações para derivar a prova/verificador.
- **TLS/HTTPS:** Comunicação segura entre cliente e servidor usando certificados auto-assinados (`tls_cert_generator.py`).
- **JWT:** Tokens de sessão com expiração para controle de acesso após a autenticação ZKP.

***

**Desenvolvido por:** Elias Andrade | Arquiteto de Soluções
**Empresa:** O2 Data Solutions
