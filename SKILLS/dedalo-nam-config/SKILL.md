---
name: dedalo-nam-config
description: >
  Use when configuring NetIQ Access Manager (NAM) — contracts, user stores, methods,
  form fills, role validation policies, OU configuration for authentication, session
  cookies, general NAM settings. Cross-platform (Linux + Windows).
---

# dedalo-nam-config

Contexto sobre **Configuraciones de NetIQ Access Manager (NAM)**.

## Ubicación de la documentación en el vault

| Área | Linux | Windows |
|------|-------|---------|
| NAM Procedimientos | `/files/Personal-Vault/Manuales/03-ADVANCED-TECHNOLOGIES/04-NETWORKS/01-NAM/00-PROCEDIMIENTOS/` | `C:\Users\lcampassi\Proton Drive\D4rkDr4g0n19\My files\Personal-Vault\Manuales\03-ADVANCED-TECHNOLOGIES\04-NETWORKS\01-NAM\00-PROCEDIMIENTOS\` |
| NAM General | `/files/Personal-Vault/Manuales/03-ADVANCED-TECHNOLOGIES\04-NETWORKS\01-NAM\03-GENERAL/` | `C:\Users\lcampassi\Proton Drive\D4rkDr4g0n19\My files\Personal-Vault\Manuales\03-ADVANCED-TECHNOLOGIES\04-NETWORKS\01-NAM\03-GENERAL\` |

## Documentación disponible

### Procedimientos
- `Armado de un contrato en NAM para eDir.md` — Configuración de contrato NAM contra eDirectory: User Stores, Methods, Contracts
- `Como añadir Roles de Usuario a NAM.md` — Integración de roles de usuario en NAM
- `Como armar un Form Fill.md` — Configuración de Form Fill para autenticación basada en formularios
- `Como crear una politica de validacion de roles en NAM.md` — Políticas de validación de roles
- `Creacion de contratos en NAM.md` — Guía general de creación de contratos
- `Definicion de OUs que puede revisar para autenticar usuarios el user store de NAM.md` — Restricción de OUs para autenticación

### General
- `COOKIE De Session de NAM5.md` — Configuración de cookies de sesión en NAM 5

## Conceptos clave

### Arquitectura NAM
- **Identity Server (IDP)**: proveedor de identidad, autenticación, SSO
- **Access Gateway (AG)**: proxy reverso, protección de recursos web
- **Admin Console**: consola de administración centralizada
- **User Stores**: fuentes de usuarios (eDirectory, LDAP, Active Directory)
- **Contracts**: definiciones de métodos de autenticación y políticas de acceso
- **Methods**: métodos de autenticación (Name/Password, X.509, etc.)
- **Form Fill**: relleno automático de formularios para SSO a aplicaciones web

### Componentes de un contrato
1. **User Store**: fuente de usuarios para autenticar
2. **Methods**: cómo se autentican (contraseña, certificado, etc.)
3. **Roles**: qué roles pueden acceder
4. **OUs**: qué unidades organizativas pueden autenticarse

### Configuraciones típicas
- Restricción de OUs para autenticación: definir qué OUs del user store pueden autenticar
- Roles de usuario: mapeo de roles de eDirectory/IDM a NAM
- Form Fill: configuración de política de relleno automático de credenciales
- Cookies de sesión: configuración de timeout, dominio, seguridad
