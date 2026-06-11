---
name: IDM-identity-servers
description: >
  Use when managing IDM servers — eDirectory, Identity Engine, Identity Apps (Tomcat),
  Remote Loader, OSP, SSPR, Identity Console, iManager. Health checks, log analysis,
  service management, troubleshooting de componentes.
  Cross-platform (Linux + Windows). NO incluye instalación.
---

# IDM-identity-servers

## Propósito

Este skill se activa cuando el usuario necesita **mantener, operar o diagnosticar** servidores del stack **OpenText Identity Manager (IDM)**. Cubre:

- Arquitectura general de IDM y sus componentes
- Ubicación de logs de cada servicio
- Búsqueda de errores de eDirectory en Babilonia y en internet
- Health checks y diagnóstico de componentes
- Preguntar por la arquitectura del cliente antes de trabajar

**No incluye** instalación (el usuario explicitó que solo quiere mantenimiento), ni drivers IDM (usar `IDM-identity-drivers`), ni workflows (`IDM-workflow-forms`), ni NAM (`NAM-access-manager`).

---

## ¿Qué es IDM? — Contexto general

**OpenText Identity Manager** (antes NetIQ IDM, Micro Focus IDM, Novell IDM) es una plataforma de **gestión de identidades (IAM)** que permite:

1. **Sincronización de identidades** — mantener identidades consistentes entre sistemas (AD, LDAP, RRHH, bases de datos, etc.)
2. **Aprovisionamiento automatizado** — crear/modificar/eliminar cuentas en sistemas conectados según reglas de negocio
3. **Workflows de aprobación** — solicitudes de recursos, roles, accesos con flujos de aprobación
4. **Roles y certificaciones** — gestión de roles empresariales y campañas de certificación
5. **Self-service** — autogestión de contraseñas (SSPR), datos de perfil, solicitudes
6. **Reporting** — auditoría e informes de identidades

### Componentes del stack IDM

| Componente | Rol | Base tecnológica |
|-----------|-----|-----------------|
| **eDirectory (Identity Vault)** | Directorio LDAP subyacente. Almacena identidades, configuraciones, drivers, roles | eDirectory (Novell/OpenText) |
| **Identity Manager Engine** | Motor de aprovisionamiento. Procesa eventos del vault y aplica policies vía drivers | Nativo Linux/Windows |
| **Identity Applications (Tomcat)** | User App, Dashboard, Workflows, Role Service. La interfaz web del producto | Apache Tomcat + PostgreSQL |
| **OSP (One SSO Provider)** | Proveedor SSO para Identity Apps. Manejo de sesiones y autenticación | Componente Java en Tomcat |
| **SSPR (Self Service Password Reset)** | Autogestión de contraseñas | Aplicación web standalone |
| **Remote Loader** | Proxy para drivers que corren fuera del servidor IDM (ej: AD en Windows) | .NET / Java |
| **Fan-Out Agent** | Distribución de eventos a múltiples Remote Loaders | Nativo Linux/Windows |
| **Identity Console** | Consola de administración web moderna (reemplazo de iManager) | Web (HTML5) |
| **iManager** | Consola de administración legacy para eDirectory e IDM | Web (Java) |
| **Designer** | IDE de diseño: drivers, workflows, forms, policies | Eclipse-based (cliente) |
| **Identity Reporting** | Reportes y auditoría | Apache Tomcat + PostgreSQL + Sentinel |
| **Sentinel Log Management for IGA** | Auditoría de eventos | Servidor standalone |
| **ActiveMQ** | Mensajería asíncrona entre componentes IDM | Apache ActiveMQ |
| **NGINX** | Reverse proxy para Identity Apps | NGINX |

### Ediciones

- **Standard Edition**: Engine + eDirectory + Identity Console + SSPR + Reporting
- **Advanced Edition**: Todo lo anterior + Identity Applications (User App, Dashboard, Workflows, Roles)

---

## Protocolo de actuación

### 1. Pedir contexto del cliente

Antes de resolver cualquier cosa, pregunto al usuario **de qué cliente se trata** (si no está explicitado). Necesito saber:

- ¿Qué versión de IDM? (4.8, 4.10, CE 24.4)
- ¿Qué versión de eDirectory? (9.2, 9.3, 24.4)
- ¿Es Advanced o Standard Edition?
- ¿Qué componentes están instalados? (Engine, Identity Apps, SSPR, Reporting, etc.)
- ¿Los componentes están en un solo servidor o distribuidos?
- ¿Es clúster (HA) o single server?
- ¿Qué sistema operativo? (SLES, RHEL, Windows)
- ¿Hay Remote Loaders en Windows?
- URLs / FQDN / puertos si aplica

> Si ya tengo el contexto de la conversación actual, no pregunto de nuevo.

### 2. Buscar errores de eDirectory

Cuando el usuario reporte un error de eDirectory:

1. **Buscar en Babilonia**: `$BABILONIA_IDM/00-ERRORES/` — leer documentación existente sobre el error
2. **Buscar en internet**: usar `webfetch` o `websearch` para buscar:
   - El código o mensaje de error exacto
   - TIDs (Technical Information Documents) de OpenText/Micro Focus
   - Community de OpenText (https://community.opentext.com)

### 3. Revisar logs

Identificar qué componente está fallando y acceder a los logs correspondientes (ver tabla de logs abajo).

### 4. Responder / resolver

- Basar la respuesta en vault + documentación oficial + experiencia.
- Si no hay documentación en Babilonia, reconocerlo.

### 5. Documentar (solo si el usuario lo pide explícitamente)

Usar `obsidian-manager` para crear documento en `$BABILONIA_IDM/00-ERRORES/` o `$BABILONIA_IDM/06-SERVER/`.

---

## Logs de servicios IDM

### Identity Engine + eDirectory

| Log | Ruta | Propósito |
|-----|------|-----------|
| ndsd.log | `/var/opt/novell/eDirectory/log/ndsd.log` | Log principal del servicio eDirectory |
| ndstrace.log | `/var/opt/novell/eDirectory/log/ndstrace.log` | Trace de eDirectory (debug) |
| DHost errors | `/var/opt/novell/eDirectory/log/DHostError.log` | Errores del DHost |
| Driver traces | `/var/log/idm/<driver>.log` | Traces de drivers individuales |

### Identity Applications (Tomcat)

| Log | Ruta | Propósito |
|-----|------|-----------|
| catalina.out | `/opt/netiq/idm/apps/tomcat/logs/catalina.out` | Log principal de Tomcat |
| localhost.log | `/opt/netiq/idm/apps/tomcat/logs/localhost.*.log` | Interacciones Tomcat-cliente |
| idapps.out | `/opt/netiq/idm/apps/tomcat/logs/idapps.out` | Log de Identity Applications (User App) |
| osp-idm-*.log | `/opt/netiq/idm/apps/tomcat/logs/osp-idm-*.log` | Log de OSP (SSO) |
| localhost_access_log | `/opt/netiq/idm/apps/tomcat/logs/localhost_access_log.*.txt` | Access log HTTP |
| workflow.log | `/opt/netiq/idm/apps/tomcat/logs/workflow.log` | Log del Workflow Engine |

### SSPR

| Log | Ruta |
|-----|------|
| SSPR.log | `/opt/netiq/idm/apps/sspr/sspr_data/logs/SSPR.log` |

### Identity Reporting

| Log | Ruta |
|-----|------|
| Reporting logs | `/var/opt/netiq/idm/log/` |

### Remote Loader

| Log | Ruta (Linux) | Ruta (Windows) |
|-----|-------------|----------------|
| Remote Loader log | `/opt/novell/eDirectory/lib/nds-modules/dirxml/RemoteLoader/logs/` | `C:\Program Files\Novell\RemoteLoader\logs\` |

### ActiveMQ

| Log | Ruta |
|-----|------|
| activemq.log | `/opt/netiq/idm/apps/activemq/data/activemq.log` |

### NGINX

| Log | Ruta |
|-----|------|
| access.log | `/opt/netiq/idm/apps/sites/logs/access.log` |
| error.log | `/opt/netiq/idm/apps/sites/logs/error.log` |

### Identity Console

| Log | Ruta |
|-----|------|
| idconsole.log | `/opt/netiq/idconsole/logs/idconsole.log` |

### iManager

| Log | Ruta |
|-----|------|
| catalina.out | `/opt/novell/iManager/tomcat/logs/catalina.out` |
| iManager logs | `/var/opt/novell/iManager/log/` |

---

## Servicios systemd (Linux)

| Servicio | Componente | Comando |
|----------|-----------|---------|
| `netiq-tomcat.service` | Identity Apps (Tomcat) | `systemctl start/stop/restart/status netiq-tomcat` |
| `netiq-activemq.service` | ActiveMQ | `systemctl start/stop/restart/status netiq-activemq` |
| `netiq-nginx.service` | NGINX | `systemctl start/stop/restart/status netiq-nginx` |
| `netiq-golang.service` | Golang (componente auxiliar) | `systemctl start/stop/restart/status netiq-golang` |
| `ndsd.service` | eDirectory | `systemctl start/stop/restart/status ndsd` |
| `novell-idp.service` | NAM Identity Server | `systemctl start/stop/restart/status novell-idp` |
| `novell-mag.service` | NAM Access Gateway | `systemctl start/stop/restart/status novell-mag` |

---

## Vault — Ubicación de documentación

| Área | Ruta (via env var) |
|------|-------------------|
| IDM — Errores | `$BABILONIA_IDM/00-ERRORES/` |
| IDM — Tools | `$BABILONIA_IDM/01-TOOLS/` |
| IDM — Server | `$BABILONIA_IDM/06-SERVER/` |

> **Nota:** La documentación en Babilonia cubre casos puntuales. Para errores no documentados, buscar en internet (OpenText TIDs, Community).

---

## Buenas prácticas

### Para troubleshooting
- **Siempre empezar por logs** — identificar qué componente falla y revisar su log correspondiente.
- **Buscar errores en Babilonia primero** — muchos errores comunes ya están documentados.
- **Usar grep recursivo** para buscar un parámetro en múltiples logs:
  ```bash
  grep -ril "parametro" /ruta/a/logs/*
  grep -rl "parametro" /ruta/a/logs/*
  ```
- **Driver trabado** — intentar reinicio desde consola, reinicio del eDir y Como último recurso, usar `dxcmd` desde línea de comandos.

### Para drivers trabados (último recurso)
```bash
cd /opt/novell/eDirectory/bin
./dxcmd -host <IP-eDir> -user <admin> -password <pass> -s
```

### Documentación
- **No borrar nunca** documentos existentes en el vault.
- **Solo crear** documentación nueva si el usuario lo pide explícitamente.
- Versionar configuraciones y cambios en Babilonia.

---

## Cross-platform

| Aspecto | Linux (SLES/RHEL) | Windows |
|---------|-------------------|---------|
| Engine | `/opt/novell/eDirectory/` | `C:\Program Files\Novell\` |
| Identity Apps | `/opt/netiq/idm/apps/tomcat/` | N/A (solo Linux) |
| Remote Loader | `/opt/novell/eDirectory/lib/nds-modules/dirxml/RemoteLoader/` | `C:\Program Files\Novell\RemoteLoader\` |
| iManager | Web via browser | Web via browser |
| Identity Console | Web via browser | Web via browser |
| Logs eDirectory | `/var/opt/novell/eDirectory/log/` | `C:\Novell\eDirectory\log\` |
| Servicios | systemd | Services.msc |

> Los componentes core de IDM (Engine, Identity Apps, SSPR) son nativos de Linux. Remote Loader puede correr en Windows para drivers de AD.

---

## Referencias oficiales

- [OpenText IDM CE 24.4 (v4.10) — Overview and Planning Guide](https://www.netiq.com/documentation/identity-manager-4.10/idm_overview_planning/data/)
- [OpenText IDM CE 24.4 (v4.10) — Install and Upgrade Guide for Linux](https://www.netiq.com/documentation/identity-manager-4.10/setup_linux/data/)
- [OpenText IDM — Administrator's Guide to Identity Applications](https://www.netiq.com/documentation/identity-manager-4.10/identity_apps_admin/data/)
- [OpenText Community — IDM](https://community.opentext.com/cybersec/identity/)
- [eDirectory Administration Guide](https://www.netiq.com/documentation/edirectory-9/)
