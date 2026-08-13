---
name: ONEIM-starling
description: >
  Use when administering One Identity Starling (plataforma cloud) — organizaciones,
  Starling Connect (conectores cloud SCIM), Starling Join AD, Starling 2FA,
  Identity Analytics & Risk Intelligence, status page, integración con productos
  One Identity. Genérico — aplica a cualquier organización.
---

# ONEIM-starling

## Propósito

Este skill se activa cuando el usuario necesita **administrar, operar o diagnosticar** la plataforma **One Identity Starling** (los servicios cloud de One Identity). Cubre:

- Plataforma Starling: organizaciones, cuentas, servicios
- Starling Connect (conectores cloud, SCIM)
- Starling Join AD
- Starling Two-Factor Authentication (2FA)
- Identity Analytics & Risk Intelligence
- Integración con productos One Identity (Active Roles, Cloud Access Manager, OneLogin, etc.)
- Status page y troubleshooting

**No incluye** otros productos de la suite One Identity — usar los skills hermanos:
- `ONEIM-manager` (IGA), `ONEIM-safeguard` (PAM), `ONEIM-active-roles`, `ONEIM-onelogin`, `ONEIM-password-manager`.

> [!important] **Genérico por diseño**
> Este skill NO contiene información de organizaciones/clientes específicos. Siempre se trabaja en función de la organización que el usuario describa en cada conversación.

---

## ¿Qué es Starling? — Contexto general

**One Identity Starling** es la **plataforma cloud (SaaS)** de One Identity que combina productos de la línea One Identity en servicios cloud seguros. Los administradores usan el sitio de Starling para:

1. Crear una **organización**
2. Registrar cuentas y agregar **servicios** a la organización
3. Acceder de forma segura a los servicios suscritos

### Sitios

| Sitio | URL | Uso |
|-------|-----|-----|
| **Starling Platform** | `https://www.cloud.oneidentity.com/` | Portal principal: organizaciones, servicios, suscripciones |
| **Status page** | `http://status.cloud.oneidentity.com/` | Estado operativo de cada servicio (verificar antes de abrir un caso de soporte) |

### Autenticación en la plataforma

| Tipo | Descripción |
|------|-------------|
| **General accounts** | Cuentas que usan Starling Platform para autenticarse (crear organización, login) |
| **Work accounts** | Cuentas que dependen de un tenant Azure AD configurado; Starling redirige al tenant para autenticación |

> [!note] Los data centers disponibles (US o EU) dependen de la suscripción; algunos servicios solo están en ciertas regiones.

---

## Servicios de Starling

### Starling Connect

- **Cloud-based Identity Governance**: extiende la estrategia de IGA (One Identity Manager / AD / AAD) a aplicaciones cloud
- Sincroniza usuarios, grupos y contenedores basados en **SCIM schema**
- Onboarding de apps cloud sin custom coding
- Reportes en tiempo real de recursos (on-prem, hybrid, cloud), accesos de usuarios, cuándo y por qué
- **Connectors**: catálogo de conectores para apps cloud; se configuran y activan desde la consola
- **SCIM credentials**: credenciales para conectar los sistemas

### Starling Join AD

- Conecta Active Directory (on-prem) a los servicios Starling
- Permite que productos como Active Roles accedan a servicios Starling (2FA, Identity Analytics)
- Se configura con el **Starling wizard** (ej: en Active Roles Configuration Center → Starling → Configure)

### Starling Two-Factor Authentication (2FA)

- Servicio de MFA cloud que se integra con productos One Identity (Active Roles, Cloud Access Manager, etc.)
- Se habilita/deshabilita desde el producto integrado (ej: Starling tab → Enable/Disable Starling 2FA)

### Starling Identity Analytics & Risk Intelligence

- Análisis de identidades y riesgo basado en datos de los productos conectados
- Requiere join del producto a Starling

### Otros servicios (según suscripción)

- Starling Connect for Active Roles (hosted)
- Servicios On Demand (Safeguard On Demand, etc.)
- El catálogo completo depende de la suscripción de la organización

---

## Protocolo de actuación

### 1. Pedir contexto de la organización

Antes de resolver cualquier cosa, preguntar al usuario (si no está explicitado):

- ¿Qué servicios Starling están suscritos? (Connect, Join AD, 2FA, Identity Analytics, otros)
- ¿Qué productos One Identity están integrados? (Active Roles, Cloud Access Manager, OneLogin, One Identity Manager)
- ¿Data center US o EU?
- ¿Cuentas generales o work accounts (Azure AD)?
- ¿Qué conectores están activos en Starling Connect?

> Si ya tengo el contexto de la conversación actual, no pregunto de nuevo.

### 2. Buscar en Babilonia

- Buscar en `$BABILONIA_ONEIDENTITY/` — documentación existente
- Si la info no existe o no alcanza → buscar en internet

### 3. Buscar en internet (web fallback)

- Starling Platform: `https://www.cloud.oneidentity.com/`
- Status: `http://status.cloud.oneidentity.com/`
- Documentación: `https://support.oneidentity.com/technical-documents/one-identity-starling/hosted/user-guide`
- Starling Connect: `https://support.oneidentity.com/technical-documents/starling-connect/*`

### 4. Responder / resolver

- Basar la respuesta en vault + documentación oficial + experiencia
- Si no hay documentación en Babilonia, reconocerlo y apoyarse en la oficial

### 5. Documentar (solo si el usuario lo pide explícitamente)

- Usar `obsidian-manager` para crear/actualizar notas en `$BABILONIA_ONEIDENTITY/`

---

## Health Check

Checklist genérico:

### 1. Plataforma

- ¿Status page sin incidentes? (`status.cloud.oneidentity.com`)
- ¿Organización activa y suscripciones vigentes?

### 2. Conexiones

- ¿Productos integrados siguen "joined" a Starling? (Active Roles, Cloud Access Manager, etc.)
- ¿Starling Connect activo? ¿Conectores sincronizando?
- ¿SCIM credentials válidas?

### 3. Servicios

- ¿2FA funcionando en los productos integrados?
- ¿Identity Analytics recibiendo datos?

### 4. Reporte

- Resumir: estado de plataforma, conexiones, servicios
- Documentar en Babilonia si el usuario lo pide

---

## Troubleshooting — errores comunes

| Síntoma | Posible causa | Acción |
|---------|---------------|--------|
| No se puede conectar a un servicio | Incidente en la plataforma, suscripción vencida | Verificar status page y suscripción |
| Join falla | Credenciales de Starling inválidas, organización incorrecta | Verificar credenciales y organización; re-ejecutar el wizard |
| Starling Connect no sincroniza | Conector inactivo, SCIM credentials inválidas | Verificar el conector y las credenciales |
| 2FA no aplica | Starling 2FA deshabilitado en el producto integrado | Habilitar desde el producto (ej: Starling tab) |
| Login con work account falla | Azure AD tenant no configurado o no sincronizado | Verificar el tenant Azure AD |

> Si el error no está documentado en Babilonia ni en la doc oficial, buscar en internet el mensaje exacto (support.oneidentity.com, status page).

---

## Referencias

- Starling Platform: `https://www.cloud.oneidentity.com/`
- Status page: `http://status.cloud.oneidentity.com/`
- User Guide: `https://support.oneidentity.com/technical-documents/one-identity-starling/hosted/user-guide`
- Starling Connect: `https://www.oneidentity.com/products/starling-connect/`
- Starling Connect for Active Roles: `https://support.oneidentity.com/technical-documents/starling-connect/hosted/active-roles-administration-guide/`
- GitHub: `https://github.com/OneIdentity`