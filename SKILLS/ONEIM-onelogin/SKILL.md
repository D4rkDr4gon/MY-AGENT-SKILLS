---
name: ONEIM-onelogin
description: >
  Use when administering OneLogin (IAM cloud) — SSO, MFA, cloud directory,
  apps y conectores (AD, LDAP, Workday), roles, reglas, provisioning,
  Smart Hooks, API REST OAuth2. Genérico — aplica a cualquier organización.
---

# ONEIM-onelogin

## Propósito

Este skill se activa cuando el usuario necesita **administrar, operar o diagnosticar** una organización de **OneLogin** (la plataforma de Identity and Access Management cloud de One Identity). Cubre:

- Arquitectura de OneLogin (Unified Access Management)
- Single Sign-On (SSO) y catálogo de aplicaciones
- Multi-Factor Authentication (MFA)
- Cloud directory y conectores (AD, LDAP, Workday)
- Roles, reglas y provisioning
- Smart Hooks
- API REST (OAuth2)
- Health checks y troubleshooting

**No incluye** otros productos de la suite One Identity — usar los skills hermanos:
- `ONEIM-manager` (IGA), `ONEIM-safeguard` (PAM), `ONEIM-active-roles`, `ONEIM-password-manager`, `ONEIM-starling`.

> [!important] **Genérico por diseño**
> Este skill NO contiene información de organizaciones/clientes específicos. Siempre se trabaja en función de la organización que el usuario describa en cada conversación.

---

## ¿Qué es OneLogin? — Contexto general

**OneLogin** es una plataforma cloud de **Unified Access Management (UAM)** que combina:

1. **Single Sign-On (SSO)** — un solo login para acceder a todas las aplicaciones (catálogo de 5000+ apps)
2. **Multi-Factor Authentication (MFA)** — OneLogin Protect (push), SMS, TOTP, WebAuthn/FIDO2
3. **Cloud Directory** — directorio cloud como fuente de verdad para gestionar accesos
4. **Directories y conectores** — sincronización con AD, LDAP, Workday y otros
5. **Lifecycle management** — provisioning de usuarios, onboarding/offboarding automatizado
6. **Adaptive authentication** — machine learning que detecta logins anómalos y desafía con MFA
7. **OneLogin Desktop** — extiende SSO al login del sistema operativo (macOS/Windows)

### Arquitectura

| Componente | Rol |
|------------|-----|
| **OneLogin cloud directory** | Fuente de verdad central para identidades y accesos |
| **SSO portal** | Punto único de acceso a todas las apps |
| **Connectors** | Sincronización en tiempo real con directorios on-prem y cloud (AD, LDAP, Workday) |
| **Apps** | Integraciones pre-armadas (SAML, OIDC, WS-Fed, form-based) |
| **Policies** | Reglas de acceso (MFA, restricciones por ubicación/rol/privilegio) |
| **Rules** | Automatización de asignaciones de apps/roles según atributos de usuario |
| **Smart Hooks** | Funciones serverless que interceptan eventos de autenticación/provisioning |
| **API** | REST API completa (OAuth2) para administración e integración |

### Regiones

- OneLogin opera en múltiples regiones: **us**, **eu**, **de** (afecta las URLs de la API y el tenant)

---

## Conceptos clave

### SSO y aplicaciones

- **App catalog**: 5000+ integraciones pre-armadas (SAML 2.0, OIDC, WS-Fed, form-based)
- **SSO portal**: el usuario ve sus apps asignadas y accede con un click
- **OneLogin Desktop**: SSO a nivel de sistema operativo

### MFA

| Factor | Descripción |
|--------|-------------|
| **OneLogin Protect** | App móvil con push notifications y OTP |
| **SMS** | Códigos OTP por SMS |
| **TOTP** | Códigos basados en tiempo (Google Authenticator compatible) |
| **WebAuthn / FIDO2** | Llaveros de seguridad y biometría |
| **Adaptive MFA** | Desafíos condicionales según riesgo (ubicación, dispositivo, comportamiento) |

### Directories y conectores

- **Cloud Directory**: directorio nativo de OneLogin
- **Active Directory / LDAP**: sincronización con directorios on-prem (agente OneLogin Directory Sync)
- **Workday**: sincronización de identidades desde HR
- **Provisioning**: aprovisionamiento/desaprovisionamiento de cuentas en apps conectadas

### Roles y reglas

- **Roles**: agrupan usuarios para asignar apps y políticas
- **Rules**: automatizan la asignación de roles/apps según atributos (departamento, ubicación, etc.)
- **Policies**: controlan la autenticación (MFA requerido, sesiones, restricciones)

### Smart Hooks

- Funciones serverless (Node.js) que se ejecutan en eventos de autenticación, user provisioning, etc.
- Permiten lógica custom sin modificar la plataforma

---

## Protocolo de actuación

### 1. Pedir contexto de la organización

Antes de resolver cualquier cosa, preguntar al usuario (si no está explicitado):

- ¿Qué región? (us, eu, de)
- ¿Qué plan/edición? (OneLogin SSO, OneLogin Advanced, Identity Governance)
- ¿Qué directorios están conectados? (Cloud Directory, AD, LDAP, Workday)
- ¿Qué apps están en uso? (SAML, OIDC, form-based)
- ¿MFA configurado? ¿Qué factores?
- ¿Integrado con Starling u otros productos One Identity?

> Si ya tengo el contexto de la conversación actual, no pregunto de nuevo.

### 2. Buscar en Babilonia

- Buscar en `$BABILONIA_ONEIDENTITY/01-ONE LOGIN/` — documentación existente
- Si la info no existe o no alcanza → buscar en internet

### 3. Buscar en internet (web fallback)

- Documentación: `https://developers.onelogin.com/` (API, SDKs, tutorials)
- Knowledge Base: `https://onelogin.service-now.com/support`
- Soporte: `https://support.oneidentity.com/technical-documents/onelogin/*`

### 4. Responder / resolver

- Basar la respuesta en vault + documentación oficial + experiencia
- Si no hay documentación en Babilonia, reconocerlo y apoyarse en la oficial

### 5. Documentar (solo si el usuario lo pide explícitamente)

- Usar `obsidian-manager` para crear/actualizar notas en `$BABILONIA_ONEIDENTITY/01-ONE LOGIN/`

---

## API REST

### Autenticación

- Todas las requests requieren **OAuth2 Bearer token**
- Se genera con un par **client_id + client_secret** (API credentials)
- Endpoint: `POST /api/2/oauth2/token` (o v1 según recurso)
- Scopes: mínimo necesario (ej: `manage:users`, `manage:apps`, `manage:all`)

### Endpoints principales

| Recurso | Endpoints |
|---------|-----------|
| **Users** | List, create, update, delete, bulk operations, reset password |
| **Apps** | List, create, update, get (backup/restore de configuración de apps) |
| **Roles** | List, create, assign users |
| **MFA** | Available factors, enroll, activate, verify |
| **Login** | Create session login token, verify factor, create session |
| **Connectors** | List connectors |
| **Reports** | Extracción de datos para reporting |

### SDKs

- Ruby, Python, Node.js, Java, .NET, Go, PHP, PowerShell
- Postman Collections disponibles

---

## Health Check

Checklist genérico:

### 1. Plataforma

- ¿Estado del servicio? (status page de OneLogin)
- ¿Región correcta para el tenant?

### 2. Directorios y sincronización

- ¿El agente de sincronización (AD/LDAP) está corriendo y sincronizando?
- ¿Errores de sincronización recientes?
- ¿Provisioning a apps funcionando?

### 3. Autenticación

- ¿Logins exitosos? ¿Aumento de fallos de autenticación?
- ¿MFA funcionando? ¿Usuarios sin factor registrado?
- ¿Alertas de adaptive authentication?

### 4. Apps

- ¿Apps con errores de configuración SAML/OIDC?
- ¿Certificados de apps próximos a expirar?

### 5. Reporte

- Resumir: estado de plataforma, sincronización, autenticación, apps
- Documentar en Babilonia si el usuario lo pide

---

## Troubleshooting — errores comunes

| Síntoma | Posible causa | Acción |
|---------|---------------|--------|
| SSO falla en una app | Configuración SAML incorrecta (ACS, entity ID, certificado) | Verificar metadata de la app y el certificado |
| Usuarios no sincronizan | Agente de directorio caído, credenciales inválidas | Verificar el agente y las credenciales de conexión |
| MFA no disponible | Usuario sin factor registrado, política restrictiva | Verificar políticas y registro de factores |
| API 401 | Token expirado, scopes insuficientes | Regenerar token, verificar scopes de las API credentials |
| Login bloqueado | Adaptive authentication, políticas de ubicación | Revisar eventos de riesgo y políticas |

> Si el error no está documentado en Babilonia ni en la doc oficial, buscar en internet el mensaje exacto (developers.onelogin.com, KB de OneLogin).

---

## Referencias

- Developers: `https://developers.onelogin.com/`
- API Reference: `https://developers.onelogin.com/api-docs`
- MFA API: `https://developers.onelogin.com/api-docs/1/multi-factor-authentication/overview`
- Apps API: `https://developers.onelogin.com/api-docs/2/apps/overview`
- Knowledge Base: `https://onelogin.service-now.com/support`
- GitHub: `https://github.com/OneIdentity`