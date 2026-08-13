---
name: ONEIM-password-manager
description: >
  Use when administering One Identity Password Manager — Password Manager Service,
  Administration/Self-Service/Helpdesk Sites, Management Policies, Q&A profiles,
  Password Policy Manager, Secure Password Extension, realms, FIDO2, troubleshooting.
  Genérico — aplica a cualquier instalación o cliente. Windows (producto on-prem).
---

# ONEIM-password-manager

## Propósito

Este skill se activa cuando el usuario necesita **administrar, operar o diagnosticar** una instalación de **One Identity Password Manager** (autoservicio de contraseñas para Active Directory y sistemas conectados). Cubre:

- Arquitectura de Password Manager y sus componentes
- Management Policies y políticas de contraseñas
- Sites: Administration, Self-Service, Helpdesk
- Workflows de autoservicio (registro, reset, unlock, Q&A)
- Password Policy Manager y Secure Password Extension
- Realms y despliegues múltiples
- Health checks y troubleshooting

**No incluye** otros productos de la suite One Identity — usar los skills hermanos:
- `ONEIM-manager` (IGA), `ONEIM-safeguard` (PAM), `ONEIM-active-roles`, `ONEIM-onelogin`, `ONEIM-starling`.

> [!important] **Genérico por diseño**
> Este skill NO contiene información de clientes ni infraestructuras prearmadas. Siempre se trabaja en función de la instalación que el usuario describa en cada conversación.

---

## ¿Qué es Password Manager? — Contexto general

**One Identity Password Manager** es una solución web de **gestión de contraseñas de autoservicio** para Active Directory y sistemas conectados. Permite:

1. **Self-service** — los usuarios registran, cambian y resetean sus contraseñas sin intervención del helpdesk
2. **Helpdesk delegado** — operadores resetean contraseñas, desbloquean cuentas, asignan passcodes temporales
3. **Políticas de contraseñas** — enforcement de políticas robustas en el dominio
4. **Autenticación Q&A** — preguntas y respuestas secretas para verificar identidad
5. **Sincronización cross-platform** — cambio de contraseñas en múltiples sistemas conectados (via Quick Connect Sync Engine / Redistributable Secret Management Service)
6. **FIDO2** — gestión de llaves de seguridad

### Arquitectura y componentes

| Componente | Rol |
|------------|-----|
| **Password Manager Service** | Servicio central que procesa las operaciones de contraseñas |
| **Workflow Service** | Ejecuta los workflows de los sites |
| **Administration Site** | Configuración: site settings, políticas, workflows |
| **Self-Service Site** | Portal de autoservicio para usuarios finales |
| **Helpdesk Site** | Portal para operadores de helpdesk (reset, unlock, passcodes, Q&A) |
| **Password Policy Manager** | Enforcement de políticas de contraseñas del dominio (instalar en todos los DCs x64) |
| **Secure Password Extension** | Acceso al Self-Service Site desde la pantalla de login de Windows + notificaciones de registro |
| **Offline Password Reset** | Reset de contraseñas sin conectividad al intranet (AD no disponible) |
| **SQL Server Database + SSRS** | Base de datos y reporting |
| **Secure Token Server** | Emisión de tokens seguros |
| **Redistributable Secret Management Service** | Sincronización de contraseñas entre sistemas conectados |
| **Quick Connect Sync Engine** | Motor de sincronización para cambio de contraseñas cross-platform |
| **Migration Wizard** | Actualización de perfiles al re-inicializar la instancia |

### Sites (templates de configuración)

| Site | Audiencia | Funciones |
|------|-----------|-----------|
| **Administration Site** | Administradores | Configuración de site settings, políticas, workflows |
| **Self-Service Site** | Usuarios finales | Register, Manage My Profile, Edit Q&A, Reset/Change password, Unlock account, Enable account, Force change at next logon, Subscribe to notifications, Issue BitLocker Recovery Key |
| **Helpdesk Site** | Operadores helpdesk | Reset password, Unlock account, Assign passcode, Unlock Q&A profile, Enforce Q&A update, Restart workflow on error |

> [!note] El **legacy Self-Service site** está deprecado desde Password Manager 5.14.0 — usar el nuevo Self-Service Site.

---

## Management Policies

- Las **Management Policies** definen qué usuarios pueden hacer qué (scope de usuarios, workflows habilitados)
- Se pueden agregar o clonar políticas existentes
- Configuran: acceso a los sites, workflows de autoservicio, políticas de contraseñas
- Cada política tiene un **scope de usuarios** (user scope) y de helpdesk (helpdesk scope)

### Cuentas usadas por Password Manager

| Cuenta | Uso |
|--------|-----|
| **Password Manager Service account** | Cuenta del servicio principal |
| **Application pool identity** | Identidad del pool de aplicaciones de IIS |
| **Domain management account** | Cuenta con permisos de gestión en el dominio |
| **Password policy account** | Cuenta para aplicar políticas de contraseñas |
| **Quick Connect account** | Cuenta para sincronización cross-platform |

---

## Realms y despliegues

- **Realm**: una o más instancias de Password Manager que comparten configuración (mismos scopes, Management Policies, workflows, settings)
- Se agrega un miembro al realm instalando una instancia nueva y seleccionando **"A replica of an existing instance"** durante la inicialización
- **Realm affinity**: fuerza a Secure Password Extension a usar solo instancias de un realm específico
- **FailSafe**: soporte para continuidad ante fallos

### Despliegues típicos

| Tipo | Descripción |
|------|-------------|
| **Simple** | Una instancia con todos los componentes |
| **Standalone sites** | Self-Service y Helpdesk Sites en servidores separados |
| **Realm** | Múltiples instancias compartiendo configuración |
| **Multiple realms** | Varios realms para entornos/segmentos distintos |

---

## Protocolo de actuación

### 1. Pedir contexto de la instalación

Antes de resolver cualquier cosa, preguntar al usuario (si no está explicitado):

- ¿Qué versión de Password Manager? (5.14.x, 5.15, etc.)
- ¿Qué componentes están instalados? (Service, sites, Password Policy Manager, Secure Password Extension, Offline Password Reset)
- ¿Despliegue simple, standalone sites o realm?
- ¿Qué Management Policies existen?
- ¿Integrado con Quick Connect / Redistributable Secret Management Service?
- ¿FIDO2 en uso?

> Si ya tengo el contexto de la conversación actual, no pregunto de nuevo.

### 2. Buscar en Babilonia

- Buscar en `$BABILONIA_ONEIDENTITY/` — documentación existente
- Si la info no existe o no alcanza → buscar en internet

### 3. Buscar en internet (web fallback)

- Documentación: `https://docs.oneidentity.com/bundle/password-manager_admin-guide_*`
- Soporte: `https://support.oneidentity.com/technical-documents/password-manager/*`

### 4. Responder / resolver

- Basar la respuesta en vault + documentación oficial + experiencia
- Si no hay documentación en Babilonia, reconocerlo y apoyarse en la oficial

### 5. Documentar (solo si el usuario lo pide explícitamente)

- Usar `obsidian-manager` para crear/actualizar notas en `$BABILONIA_ONEIDENTITY/`

---

## Health Check

Checklist genérico:

### 1. Servicios

- ¿Password Manager Service corriendo?
- ¿Workflow Service OK?
- ¿SQL Server accesible? ¿SSRS responde?
- ¿Sites responden (Administration, Self-Service, Helpdesk)?

### 2. Workflows

- ¿Hay workflows fallidos o atascados?
- ¿Resets de contraseña exitosos en el último período?
- ¿Errores de autenticación Q&A?

### 3. Dominio / AD

- ¿Password Policy Manager activo en los DCs?
- ¿Secure Password Extension desplegado y encontrando el Self-Service Site (service connection points)?
- ¿Cuenta de servicio con permisos válidos?

### 4. Sincronización

- ¿Cambios de contraseña replicados a sistemas conectados (Quick Connect / Secret Management)?
- ¿Errores de sincronización?

### 5. Reporte

- Resumir: servicios, workflows, dominio, sincronización
- Documentar en Babilonia si el usuario lo pide

---

## Troubleshooting — errores comunes

| Síntoma | Posible causa | Acción |
|---------|---------------|--------|
| Self-Service Site no encontrado desde login | Service connection points ausentes o mal publicados | Verificar SCPs en AD; override manual de URL si aplica |
| Reset de contraseña falla | Cuenta de servicio sin permisos, política de dominio | Verificar credenciales y Management Policy |
| Workflow atascado | Workflow Service detenido, error en paso | Revisar logs del workflow, restart si corresponde |
| Q&A no disponible | Usuario sin perfil Q&A registrado | Verificar registro; helpdesk puede unlock Q&A profile |
| Password Policy Manager no aplica | No instalado en todos los DCs x64 | Instalar en todos los DCs |
| Sincronización cross-platform falla | Quick Connect / Secret Management Service caído | Verificar el servicio y las cuentas conectadas |

> Si el error no está documentado en Babilonia ni en la doc oficial, buscar en internet el mensaje exacto (support.oneidentity.com, community).

---

## Referencias

- Architecture: `https://docs.oneidentity.com/bundle/password-manager_admin-guide_5.15/page/guides/adminguide/pm-architecture-cover.htm`
- Components: `https://docs.oneidentity.com/bundle/password-manager_admin-guide_5.14.4/page/guides/adminguide/pm-components.htm`
- Administration Guide: `https://support.oneidentity.com/technical-documents/password-manager/5.14/administration-guide`
- GitHub: `https://github.com/OneIdentity`