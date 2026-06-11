---
name: enterprise-certificates
description: >
  Use when handling certificates for IDM and NAM — keystores (JKS/PKCS12), keytool,
  OpenSSL, iManager certificate management, LDAP certificates, wildcard certs,
  renewal procedures, SAN configuration, trust chains. Cross-platform (Linux + Windows).
---

# enterprise-certificates

Contexto sobre gestión de certificados para entornos **Identity Manager (IDM)** y **Access Manager (NAM)**.

## Ubicación de la documentación en el vault

| Área | Ruta (via env var) |
|------|-------------------|
| IDM Certificados | `$BABILONIA_IDM/03-CERTIFICADOS/` |
| NAM Certificados | `$BABILONIA_NAM/02-CERTIFICADOS/` |

## Documentación disponible

### IDM — Certificados
- `Cambio de certificados iManager.md` — CSR con keytool, SAN, reemplazo en iManager
- `Cambio de certificados LDAP.md` — Server certificate desde Roles and Tasks > Certificate Server
- `Cambio de certificados para Userapp.md` — Certificados para User Application
- `Cambio Certificado nginx - wf json.md` — Certificados para nginx en entorno WF JSON
- `Procedimiento cambio de certificados PZRThiflow.md` — Certificados para HiFlow

### NAM — Certificados
- `Cambio certificado wilcard NAM.md` — Cambio de wildcard en NAM
- `Instructivo renovación certificados NAM Admin Console.md` — Renovación desde Admin Console

## Herramientas comunes
- **keytool**: generación de keystores, CSR, importación (ruta: `/opt/netiq/common/jre/bin/keytool`)
- **OpenSSL**: verificación, conversión (PEM, DER, PKCS12)
- **iManager**: server certificates contra CA interna de eDirectory
- **NAM Admin Console**: renovación de certificados en cluster
- **nginx**: certificados SSL para WF JSON

## Conceptos clave
- Algoritmo: RSA 2048, firma SHA256withRSA
- SAN (Subject Alternative Names): IPs, DNS names necesarios
- Formato: JKS (Java KeyStore), PKCS12, PEM
- Validez típica: 1 año (365 días) o 10 años (3650 días)
- CA: interna de eDirectory o externa según entorno
