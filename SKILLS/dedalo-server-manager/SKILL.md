---
name: dedalo-server-manager
description: >
  Use when managing IDM/NAM servers — Tomcat, Identity Apps, eDirectory, health checks,
  log analysis, installation (IDM 4.10.1), driver troubleshooting, search params in logs,
  service management. Cross-platform (Linux + Windows).
---

# dedalo-server-manager

Contexto sobre **Servidores IDM/NAM** — instalación, configuración, logs y mantenimiento.

## Ubicación de la documentación en el vault

| Área | Linux | Windows |
|------|-------|---------|
| IDM Server | `/files/Personal-Vault/Manuales/04-SPECIALIZED-DOMAINS/01-IAM-IDENTITY/01-IDM/06-SERVER/` | `C:\Users\lcampassi\Proton Drive\D4rkDr4g0n19\My files\Personal-Vault\Manuales\04-SPECIALIZED-DOMAINS\01-IAM-IDENTITY\01-IDM\06-SERVER\` |

## Documentación disponible

- `Instalacion y configuracion IDM 4.10.1.md` — Instalación completa sobre SLES: firewall, SSH, FQDN, repositorios zypper, prerequisitos, instalación de Identity Manager
- `Comando para buscar un parametro en multiples logs.md` — Comandos útiles para búsqueda de parámetros en logs
- `Comando por si se traban los Drivers.md` — Procedimiento para drivers trabados

## Conceptos clave

### Servidores típicos del stack IDM
- **Identity Apps (idmapps)**: servidor Tomcat con las aplicaciones de identidad (User App, WF, etc.)
- **Identity Console**: consola de administración web
- **iManager**: consola de administración de eDirectory
- **Remote Loader**: proxy para drivers externos (Windows)
- **eDirectory**: directorio subyacente

### Comandos útiles para logs
```bash
# Buscar parámetros en logs
grep -r "parametro" /ruta/a/logs/

# Ver logs de Tomcat
tail -f /opt/netiq/idm/apps/tomcat/logs/catalina.out

# Ver health de drivers (desde iManager)
# o usando la consola de Identity Console
```

### Drivers trabados
- Posibles causas: bloqueos en base de datos, problemas de red con Remote Loader, errores de conexión LDAP
- Verificar estado desde iManager > Identity Manager > Driver Health
- Forzar reinicio desde Identity Console

### Instalación IDM 4.10.1
- Base: SUSE Linux Enterprise Server
- Requiere: FQDN configurado, firewall apagado/abierto, repositorios OpenSUSE
- Componentes: Identity Manager Engine, Identity Apps, Designer (cliente)
