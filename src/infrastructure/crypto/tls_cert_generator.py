# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
TLS CERT GENERATOR
═══════════════════════════════════════════════════════════════════════════════
Gera certificados TLS auto-assinados para HTTPS
Autor: Elias Andrade - Arquiteto de Soluções
═══════════════════════════════════════════════════════════════════════════════
"""

import datetime
import os

from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.x509.oid import NameOID


class TlsCertGenerator:
    """Gera certificados TLS auto-assinados."""

    def generate(
        self,
        cert_path: str,
        key_path: str,
        certs_dir: str,
        common_name: str = "localhost",
        org_name: str = "SecureMessenger ZKS",
        country: str = "BR",
    ) -> None:
        """Gera e salva certificado e chave se não existirem."""
        os.makedirs(certs_dir, exist_ok=True)
        if os.path.exists(cert_path) and os.path.exists(key_path):
            return

        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096,
        )
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, country),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, org_name),
            x509.NameAttribute(NameOID.COMMON_NAME, common_name),
        ])
        cert = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(issuer)
            .public_key(private_key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(datetime.datetime.utcnow())
            .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
            .add_extension(
                x509.SubjectAlternativeName([x509.DNSName("localhost")]),
                critical=False,
            )
            .sign(private_key, hashes.SHA256())
        )
        with open(key_path, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            ))
        with open(cert_path, "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
