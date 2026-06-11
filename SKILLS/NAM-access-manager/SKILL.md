---
name: NAM-access-manager
description: >
  Use when configuring NetIQ Access Manager (NAM) — Identity Server, Access Gateway,
  contracts, user stores, methods, form fills, role policies, Advanced Options (Apache),
  cookies de sesión, troubleshooting de autenticación y SSO.
  Cross-platform (Linux + Windows).
---

# NAM-access-manager

## Propósito

Este skill se activa cuando el usuario plantea tareas relacionadas con **NetIQ Access Manager (NAM)** de OpenText (antes Micro Focus / NetIQ / Novell). Cubre configuración, operación y troubleshooting de los componentes del producto.

**No incluye** gestión de certificados (usar `enterprise-certificates`), ni drivers IDM (usar `IDM-identity-drivers`), ni troubleshooting de servidores (`IDM-identity-servers`), ni workflows (`IDM-workflow-forms`).

---

## Contexto técnico de NAM

### ¿Qué es NAM?

NetIQ Access Manager es una solución de **gestión de accesos y SSO** empresarial. Consta de 4 componentes principales:

| Componente | Rol | Base tecnológica |
|-----------|-----|-----------------|
| **Identity Server (IdP)** | Proveedor de identidad SAML 2.0 / OAuth / OIDC. Autenticación, emisión de tokens, políticas | Apache Tomcat + Jetty |
| **Access Gateway (AG)** | Reverse proxy que protege recursos web. SSO, form fill, inyección de headers | **Apache HTTPD 2.4** + Tomcat (comunicación vía AJP) |
| **Administration Console** | Consola web centralizada de configuración | Apache Tomcat |
| **Analytics Server** | Dashboard, reportes, auditoría | Kibana (ELK stack) |

### Modelos de despliegue

1. **Access Manager (componentes individuales)** — Cada componente en servidores separados. Soporta Docker, AWS EC2, Azure.
2. **Access Manager Appliance** — Todo-en-uno basado en SUSE Linux Enterprise Server. Identity Server + Access Gateway + Admin Console empaquetados.

### Relación con Apache (importante)

- El **Access Gateway** corre sobre **Apache HTTPD 2.4**. Las `Advanced Options` (globales y por proxy service) aceptan **directivas Apache nativas** además de las opciones `NAG-prefix` documentadas.
- La comunicación entre Apache HTTPD y Tomcat se hace mediante el **protocolo AJP** (`mod_proxy_ajp`).
- Esto permite usar directivas como `Header always set`, `RequestHeader set/unset`, `SSLProtocol`, `SSLCipherSuite`, `LogLevel`, etc. directamente desde la UI de NAM.
- NO experimentar con directivas Apache sin conocer el impacto — una directiva incorrecta puede dejar el AG caído.

### Jerarquía de configuración

```
Administration Console
  └── Identity Server (IdP)
        ├── User Stores (eDirectory, AD, LDAP, local)
        ├── Methods (Name/Password, X.509, Kerberos, OAuth, etc.)
        ├── Contracts (method + user store + políticas)
        ├── Shared Settings (secret stores, atributos custom)
        └── Defaults (contrato por defecto, user store default)
  └── Access Gateway (AG)
        ├── Reverse Proxy / Proxy Service
        ├── Protected Resources (URLs a proteger)
        ├── Form Fill Policies (SSO vía relleno automático)
        ├── Role Policies (validación de roles)
        ├── Advanced Options (global y por proxy service)
        └── Certificados SSL
  └── Analytics Server (dashboard)
```

---

## Protocolo de actuación

Siempre que se invoque este skill, seguir estos pasos:

### 1. Pedir contexto del cliente

Antes de resolver cualquier cosa, pregunto al usuario **de qué cliente se trata** (si no está explicitado en la conversación). Necesito saber:

- ¿Es un ambiente nuevo o existente?
- ¿Qué versión de NAM? (4.5, 5.0, 5.1 Appliance, CE 24.2)
- ¿Modelo de despliegue? (componentes separados vs Appliance)
- ¿Qué componentes están involucrados? (IdP, AG, Analytics)
- ¿El user store es eDirectory, AD u otro LDAP?
- ¿Hay clúster / alta disponibilidad?
- URLs / FQDN / puertos involucrados (si aplica)

> Si ya tengo el contexto del cliente de la conversación actual, no pregunto de nuevo.

### 2. Revisar Babilonia

Buscar en `$BABILONIA_NAM` si existe documentación relevante al tema. Leer los documentos aplicables y citarlos como fuente.

### 3. Responder / resolver

- Si hay documentación aplicable en el vault, basar la respuesta en ella + documentación oficial de OpenText + experiencia.
- Si no hay documentación en Babilonia, reconocerlo y resolver con fuente oficial de OpenText o conocimiento propio.

### 4. Documentar (solo si el usuario lo pide explícitamente)

Si el usuario dice "documentalo" o "guardalo en el vault", usar `obsidian-manager` para crear el documento en la carpeta correspondiente de `$BABILONIA_NAM`.

---

## Vault — Ubicación de documentación

| Área | Ruta (via env var) |
|------|-------------------|
| NAM — Configuraciones básicas | `$BABILONIA_NAM/00-CONFIGURACIONES-BASICAS/` |
| NAM — Errores documentados | `$BABILONIA_NAM/01-ERRORES/` |
| NAM — Certificados | `$BABILONIA_NAM/02-CERTIFICADOS/` |
| NAM — General | `$BABILONIA_NAM/03-GENERAL/` |
| NAM — Advanced Options (Apache) | `$BABILONIA_NAM/04-ADVANCE-OPTIONS/` |

> **Nota:** La documentación en Babilonia cubre casos puntuales, pero NO es exhaustiva. NAM es un producto muy amplio y muchas configuraciones posibles no están documentadas allí. En esos casos, se resuelve con documentación oficial de OpenText y experiencia técnica.

---

## Buenas prácticas y tips clave

### Configuración general
- **Siempre usar HTTPS** — los métodos Secure Name/Password requieren SSL.
- **Contracts inseguros por defecto** — NAM viene con `Name/Password - Basic` y `Name/Password - Form` habilitados. En producción, eliminarlos o reemplazarlos por `Secure Name/Password`.
- **MFA** — se logra asociando múltiples Methods a un mismo Contract.
- **User Store order matters** — el orden de user stores en un Method define el orden de búsqueda. Primero donde esté la mayoría de usuarios.
- **OU restriction** — se configura en el User Store, no en el Contract. Limita qué OUs pueden autenticarse.

### Cookies de sesión
- `JSESSIONID` → Identity Server (path `/nidp`)
- `IPC` (Identity Proxy Cookie) → Access Gateway
- `SPC` (Session Proxy Cookie) → Access Gateway
- Atributos de seguridad recomendados: `HttpOnly`, `Secure`, `SameSite=Lax|Strict`

### Advanced Options
- Preferir opciones `NAG-prefix` documentadas (soportadas oficialmente).
- Para casos no cubiertos (ej: inyección de headers CUSTOM), las directivas Apache nativas funcionan pero **no tienen soporte oficial**.
- Probar siempre en ambiente de desarrollo antes de pasar a producción.
- `DumpResponseHeaders on` es útil para debug pero **no usarlo en producción** (genera mucho log).
- Documentar TODAS las Advanced Options aplicadas (en Babilonia o en un changelog).

### Form Fill
- Solo soporta `content-type: text/html`.
- Para forms con JavaScript complejo, usar `InPlaceSilent=on` + `InPlaceSilentPolicyDoesSubmit=on`.
- Los Shared Secrets se gestionan desde Identity Server > Shared Settings > Custom Attributes.


## Troubleshooting de NAM

### Logs de componentes

#### Identity Server (IdP)

| Log | Ruta | Propósito |
|-----|------|-----------|
| catalina.out (IdP) | `/var/opt/novell/nam/logs/idp/tomcat/catalina.out` | Log principal del Identity Server. Policy evaluation, autenticación, SAML, OAuth |
| IdP access log | `/var/opt/novell/nam/logs/idp/tomcat/localhost_access_log.*.txt` | HTTP access log del IdP |
| IdP localhost log | `/var/opt/novell/nam/logs/idp/tomcat/localhost.*.log` | Interacciones Tomcat-cliente en IdP |
| NIDP logs (XML) | `/var/opt/novell/tomcat/webapps/nesp/WEB-INF/logs/nidp.*.xml` | Logs detallados del ESP (Embedded Service Provider) — policy evaluation |
| Request dumper | Configurable vía `RequestDumperFilter` en `web.xml` | Debug de requests HTTP completos |

#### Access Gateway (AG)

| Log | Ruta | Propósito |
|-----|------|-----------|
| Apache error_log | `/var/opt/novell/nam/logs/mag/apache2/error_log` | Log de errores de Apache HTTPD (AG) |
| catalina.out (AG) | `/var/opt/novell/nam/logs/mag/tomcat/catalina.out` | Log de Tomcat del AG (ESP, form fill, policies) |
| Reverse proxy logs | `/var/log/novell/reverse/` | HTTP transaction logging por proxy service (si está habilitado) |
| JCC log | `/var/opt/novell/nam/logs/jcc/jcc-0.log.0` | Comunicación AG ↔ Admin Console (imports, certs, health) |
| AGS error log | `/var/opt/novell/nam/logs/mag/amlogging/ags_error.log` | Errores de Gateway Service Manager |
| Verbose log | `/var/opt/novell/nam/logs/mag/amlogging/verbose_log` | Log verbose (debug) |
| HTTP headers debug | Activable con `DumpResponseHeaders on` (global) | Debug de headers HTTP request/response |

#### Administration Console

| Log | Ruta |
|-----|------|
| catalina.out (AC) | `/var/opt/novell/nam/logs/ac/tomcat/catalina.out` |

#### Analytics Server

| Log | Ruta |
|-----|------|
| Analytics logs | `/var/opt/novell/nam/logs/dashboard/` |

### Servicios systemd

| Servicio | Componente | Comandos |
|----------|-----------|----------|
| `novell-idp.service` | Identity Server (IdP) | `systemctl start/stop/restart/status novell-idp` |
| `novell-mag.service` | Access Gateway (AG) | `systemctl start/stop/restart/status novell-mag` |
| `novell-ac.service` | Administration Console | `systemctl start/stop/restart/status novell-ac` |
| `novell-apache2.service` | Apache HTTPD (AG) | `systemctl start/stop/restart/status novell-apache2` |
| `novell-jcc.service` | JCC (comunicación AG-AC) | `systemctl start/stop/restart/status novell-jcc` |
| `novell-activemq.service` | ActiveMQ (mensajería) | `systemctl start/stop/restart/status novell-activemq` |
| `novell-tomcat8.service` | Tomcat (Admin Console) | `systemctl start/stop/restart/status novell-tomcat8` |

### Health checks

#### Identity Server
```
https://<idp-fqdn>:<port>/nidp/heartbeat
```
Responde HTTP 200 si está saludable.

#### Access Gateway
```
https://<ag-fqdn>:<port>/nesp/app/heartbeat
```
Responde HTTP 200 si está saludable. Usado por L4 switches para health checks en clúster.

#### Administration Console
```
https://<ac-fqdn>:8443/admin-console
```

### Tools de troubleshooting

| Herramienta | Uso |
|------------|-----|
| **Re-push Configuration** | Admin Console > Troubleshooting > Re-push Current Configuration. Fuerza a AG a usar la config actual |
| **Health icon** | Admin Console > Devices > Access Gateways > [Server] > Health. Estado en tiempo real |
| **curl** | Probar conectividad, ver metadatos IdP, verificar health endpoints |
| **tail -f** | Monitoreo en tiempo real de logs (`tail -f /var/opt/novell/nam/logs/mag/apache2/error_log`) |
| **tcpdump** | Captura de tráfico en interfaces (útil para debug de AJP, SSO, redirecciones) |
| **DumpResponseHeaders** | Advanced Option global: `DumpResponseHeaders on`. Vuelca headers HTTP a `/var/opt/novell/nam/logs/mag/apache2/httpheaders` |
| **RequestDumperFilter** | Filtro Tomcat en `web.xml` del IdP para loguear requests HTTP completos |

### Errores comunes documentados en Babilonia

Los siguientes errores ya están documentados en `$BABILONIA_NAM/01-ERRORES/`:

- `ERROR "Unable To Read Keystore" en NAM`
- `Error dualidad de usuario en NAM`
- `Informe de Vulnerabilidad – ROBOT (Return Of Bleichenbacher's Oracle Threat)`
- `Sistema de analytics de NAM se queda sin espacio`

> Para errores no documentados, buscar en internet (OpenText TIDs, Community) y en `$BABILONIA_NAM/01-ERRORES/`.

### Buenas prácticas de troubleshooting

1. **Siempre empezar por el log del componente que falla** — si es autenticación, revisar IdP. Si es proxy, AG.
2. **Verificar health endpoints** antes de sumergirse en logs.
3. **Para debug de políticas**: habilitar `Echo to Console` en Identity Server > Auditing and Logging, nivel `info` o `config` para ver traces de policy evaluation en catalina.out.
4. **No usar DumpResponseHeaders en producción** — genera volumen masivo de logs.
5. **Re-push configuration** después de cambios si el AG no refleja la config nueva.
6. **Verificar conectividad de red** entre componentes (IdP ↔ AG ↔ Admin Console ↔ LDAP).

---

## Cross-platform

| Aspecto | Linux (SLES) | Windows |
|---------|-------------|---------|
| Admin Console | https://<FQDN>:8443/admin-console | Idem (vía browser) |
| Logs AG Apache | `/var/opt/novell/nam/logs/mag/apache2/` | N/A (AG no corre en Windows) |
| Logs IdP Tomcat | `/var/opt/novell/nam/logs/idp/tomcat/` | N/A |
| Servicios AG | `systemctl novell-mag` | N/A |
| Servicios IdP | `systemctl novell-idp` | N/A |
| Servicios Admin Console | `systemctl novell-tomcat8` | N/A |
| Config files | `/opt/novell/nam/` | N/A |

> NAM es un producto nativo de Linux (SLES). En Windows solo se accede vía browser a la Admin Console. No hay componentes de NAM instalables en Windows.

---

## Referencias oficiales

- [NAM 5.0 Administration Guide](https://www.microfocus.com/documentation/access-manager/5.0/admin/)
- [NAM Appliance CE 24.2 (v5.1) Administration Guide](https://www.microfocus.com/documentation/access-manager/appliance-5.1/admin/)
- [NAM 5.0 Security Guide](https://www.microfocus.com/documentation/access-manager/5.0/security-guide/)
- [OpenText NAM Community](https://community.opentext.com/cybersec/nam/)
