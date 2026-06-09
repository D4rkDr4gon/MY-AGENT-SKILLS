---
name: dedalo-tools-errors
description: >
  Use when troubleshooting errors or using tools in IDM/NAM environments — error codes,
  log analysis, iManager, Identity Console, IDMApps, HiFlow, SSPR, Tomcat issues,
  database locks, memory errors, keystore errors, NAM errors. Cross-platform.
---

# dedalo-tools-errors

Contexto sobre **Herramientas y Errores** en entornos IDM y NAM.

## Ubicación de la documentación en el vault

| Área | Linux | Windows |
|------|-------|---------|
| IDM Errores | `/files/Personal-Vault/Manuales/04-SPECIALIZED-DOMAINS/01-IAM-IDENTITY/01-IDM/00-ERRORES/` | `C:\Users\lcampassi\Proton Drive\D4rkDr4g0n19\My files\Personal-Vault\Manuales\04-SPECIALIZED-DOMAINS\01-IAM-IDENTITY\01-IDM\00-ERRORES\` |
| IDM Tools | `/files/Personal-Vault/Manuales/04-SPECIALIZED-DOMAINS/01-IAM-IDENTITY/01-IDM/01-TOOLS/` | `C:\Users\lcampassi\Proton Drive\D4rkDr4g0n19\My files\Personal-Vault\Manuales\04-SPECIALIZED-DOMAINS\01-IAM-IDENTITY\01-IDM\01-TOOLS\` |
| NAM Errores | `/files/Personal-Vault/Manuales/03-ADVANCED-TECHNOLOGIES/04-NETWORKS/01-NAM/01-ERRORES/` | `C:\Users\lcampassi\Proton Drive\D4rkDr4g0n19\My files\Personal-Vault\Manuales\03-ADVANCED-TECHNOLOGIES\04-NETWORKS\01-NAM\01-ERRORES\` |

## Documentación disponible

### IDM — Errores documentados
- `Bloqueo de base de datos idmapps Could not acquire change log lock.md` — Lock en base de datos de IDMApps, solución vía SQL directo en DATABASECHANGELOGLOCK
- `java.lang.OutOfMemoryError GC overhead limit exceeded.md` — Error de memoria en Tomcat/IDMApps
- `Manejo del error "state file corruption".md` — Corrupción de archivos de estado
- `Manejo del error "value too large for column".md` — Error de tamaño de columna en base de datos
- `Manejo del error ENGINE STATE.md` — Error de estado del motor IDM
- `Manejo del error LDAP_INSUFFICIENT_RIGHTS.md` — Permisos insuficientes en LDAP
- `Resolución del error "ERR_MISSING_MANDATORY".md` — Campos obligatorios faltantes
- `TypeError fetch failed O ERROR Invalid Response Type.md` — Error de conexión/fetch

### IDM — Tools
- **HIFLOW**:
  - `ERROR en usuario HIFLOW.md`
  - `Update associations Hiflow.md`
- **IDCONSOLE**: `comandos para identity console.md`
- **IDMAPPS**:
  - `Comandos para reiniciar el idmapps.md`
  - `Manejo de delegaciones en IDM 4.8.6.md`
  - `Script de rotacion de logs para idmapps.md`
  - `Ubicacion de las asociaciones entre roles, recursos, grupos de AD, etc..md`
- **IMANAGER**:
  - `Comandos para iManager.md`
  - `Creacion de atributos.md`
- **SSPR**:
  - `Acceso a SSPR sin SSO.md`
  - `Como acceder a modo editable en SSPR.md`
  - `que es el SSPR.md`

### NAM — Errores documentados
- `ERROR "Unable To Read Keystore" en NAM.md` — Error de lectura de keystore en NAM
- `Error dualidad de usuario en NAM.md` — Conflicto de usuarios duplicados
- `Informe de Vulnerabilidad – ROBOT (Return Of Bleichenbacher's Oracle Threat).md` — Vulnerabilidad ROBOT
- `Sistema de analytics de NAM se queda sin espacio.md` — Espacio en analytics de NAM

## Conceptos clave

### Herramientas principales
- **iManager**: consola web para gestión de eDirectory, certificados, drivers
- **Identity Console**: reemplazo moderno de iManager, basado en web
- **IDMApps**: suite Tomcat de aplicaciones de identidad (User App, WF, Workflow Dashboard)
- **HiFlow**: herramienta para flujos de aprobación avanzados
- **SSPR**: autoservicio de restablecimiento de contraseñas
- **Designer**: cliente Eclipse para diseño de drivers y workflows

### Troubleshooting general
1. Revisar logs de Tomcat: `catalina.out`, `localhost.log`
2. Verificar estado de servicios: `systemctl status <servicio>` (Linux)
3. Revisar base de datos: bloqueos, conexiones, espacio
4. Verificar conectividad de red entre componentes
5. Consultar documentación en vault para errores específicos
