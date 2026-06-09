---
name: dedalo-cert-manager
description: >
  Use when handling certificates for IDM and NAM — keystores (JKS/PKCS12), keytool,
  OpenSSL, iManager certificate management, LDAP certificates, wildcard certs,
  renewal procedures, SAN configuration, trust chains. Cross-platform (Linux + Windows).
---

# dedalo-cert-manager

Contexto sobre gestión de certificados para entornos **NetIQ Identity Manager (IDM)** y **NetIQ Access Manager (NAM)**.

## Ubicación de la documentación en el vault

| Área | Linux | Windows |
|------|-------|---------|
| IDM Certificados | `/files/Personal-Vault/Manuales/04-SPECIALIZED-DOMAINS/01-IAM-IDENTITY/01-IDM/03-CERTIFICADOS/` | `C:\Users\lcampassi\Proton Drive\D4rkDr4g0n19\My files\Personal-Vault\Manuales\04-SPECIALIZED-DOMAINS\01-IAM-IDENTITY\01-IDM\03-CERTIFICADOS\` |
| NAM Certificados | `/files/Personal-Vault/Manuales/03-ADVANCED-TECHNOLOGIES/04-NETWORKS/01-NAM/02-CERTIFICADOS/` | `C:\Users\lcampassi\Proton Drive\D4rkDr4g0n19\My files\Personal-Vault\Manuales\03-ADVANCED-TECHNOLOGIES\04-NETWORKS\01-NAM\02-CERTIFICADOS\` |

## Documentación disponible

### IDM — Certificados
- `Cambio de certificados iManager.md` — Procedimiento de generación de CSR con keytool, SAN, y reemplazo en iManager
- `Cambio de certificados LDAP.md` — Generación de server certificate desde Roles and Tasks > NetIQ Certificate Server, importación en LDAP server objects
- `Cambio de certificados para Userapp.md` — Certificados para User Application
- `Cambio Certificado nginx - wf json.md` — Certificados para nginx en entorno WF JSON
- `Procedimiento cambio de certificados PZRThiflow.md` — Certificados específicos para HiFlow

### NAM — Certificados
- `Cambio certificado wilcard NAM.md` — Procedimiento de cambio de wildcard en NAM
- `Instructivo renovación certificados NAM Admin Console.md` — Renovación desde Admin Console

## Herramientas comunes
- **keytool**: generación de keystores, CSR, importación de certificados firmados (ruta típica: `/opt/netiq/common/jre/bin/keytool`)
- **OpenSSL**: verificación, conversión de formatos (PEM, DER, PKCS12)
- **iManager**: para emitir server certificates contra CA interna de eDirectory
- **NAM Admin Console**: para renovación de certificados en el cluster
- **nginx**: certificados SSL para WF JSON

## Conceptos clave
- Algoritmo: RSA 2048, firma SHA256withRSA
- SAN (Subject Alternative Names): IPs, DNS names necesarios para conectividad
- Formato: JKS (Java KeyStore), PKCS12, PEM
- Storepass / keypass: contraseñas de keystore
- Validez típica: 1 año (365 días) o 10 años (3650 días)
- CA: interna de eDirectory o externa (según el entorno)
