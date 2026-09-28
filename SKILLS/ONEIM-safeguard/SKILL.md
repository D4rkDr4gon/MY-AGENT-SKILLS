---
name: ONEIM-safeguard
description: >
  Use when administering One Identity Safeguard (PAM) — Safeguard for Privileged
  Passwords (SPP), Safeguard for Privileged Sessions (SPS), Safeguard for Privileged
  Analytics (SPA). Assets, partitions, profiles, entitlements, access request policies,
  clustering, API REST. Genérico — aplica a cualquier instalación o cliente.
  También conduce el curso de Safeguard (syllabus del vault) como tutor.
---

# ONEIM-safeguard

## Propósito

Este skill se activa cuando el usuario necesita **administrar, operar o diagnosticar** una instalación de **One Identity Safeguard** (la suite PAM de One Identity). Cubre:

- Arquitectura de Safeguard: SPP, SPS, SPA
- Gestión de assets, cuentas, particiones, perfiles
- Entitlements y access request policies
- Sesiones privilegiadas (SPS)
- Clustering y alta disponibilidad
- Health checks y troubleshooting
- API REST

**No incluye** otros productos de la suite One Identity — usar los skills hermanos:
- `ONEIM-manager` (IGA), `ONEIM-active-roles`, `ONEIM-onelogin`, `ONEIM-password-manager`, `ONEIM-starling`.

> [!important] **Genérico por diseño**
> Este skill NO contiene información de clientes ni infraestructuras prearmadas. Siempre se trabaja en función de la instalación que el usuario describa en cada conversación.

---

## Al iniciar: ¿curso o resolución?

> [!important] **Primera pregunta obligatoria**
> Antes de cualquier otra cosa, preguntar: **"¿Es para el curso de Safeguard o para resolver algo puntual?"**. Sólo se omite si el mensaje del usuario ya lo deja claro (por ejemplo, "arranquemos el paso 03 del curso" o "tengo este error en…").

### Modo CURSO

El curso está definido en el syllabus del vault, que es la fuente de verdad:

`$BABILONIA/BIBLIOTECA-DE-BABEL/04-SPECIALIZED-DOMAINS/01-IAM-IDENTITY/03-ONEIDENTITY/02-SAFEGUARD-PAM/99-ENABLEMENTS/CURSO SAFEGUARD - SYLLABUS.md`

1. Leer el syllabus **completo** con `obsidian-manager` y seguir al pie de la letra su sección **INSTRUCCIONES PARA LA IA TUTORA**: rol de tutor socrático, ciclo de cada paso, reglas, adaptación.
2. Pedir los datos de **COMO ARRANCAR**: nombre del alumno, versión de Safeguard (o "última") y paso actual (o "retomar desde el seguimiento"). Si es "retomar", leer la sección **SEGUIMIENTO**.
3. En cada paso, el contenido sale **sólo** de las notas listadas en **Leer**. Las preguntas de repaso salen de `SAFEGUARD FOUNDATION (SG-FND) - GUIA DEL CURSO.md`, y para practicar la demo final se usa `DEMO SAFEGUARD.md`. Nunca inventar menús, opciones ni comportamientos.
4. Al cerrar la sesión, actualizar **SEGUIMIENTO** (checklist y bitácora) con `obsidian-manager`, siempre con la confirmación del alumno.
5. En este modo **no** se aplica el "Protocolo de actuación" de más abajo, salvo como consulta.

### Modo RESOLUCIÓN

Seguir el **Protocolo de actuación** de esta skill: pedir contexto de la instalación, buscar en el vault, buscar en la documentación oficial y resolver.

---

## ¿Qué es Safeguard? — Contexto general

**One Identity Safeguard** es la solución de **Privileged Access Management (PAM)** de One Identity. Se compone de tres productos que pueden usarse juntos o por separado:

| Producto | Sigla | Función |
|----------|-------|---------|
| **Safeguard for Privileged Passwords** | SPP | Vault de contraseñas, claves SSH y secretos. Rotación, check/change de credenciales, workflows de acceso |
| **Safeguard for Privileged Sessions** | SPS | Proxy de sesiones privilegiadas: intercepta, controla, graba y analiza sesiones (RDP, SSH, Telnet, etc.) |
| **Safeguard for Privileged Analytics** | SPA | Análisis de comportamiento de usuarios privilegiados con machine learning; detecta anomalías y las rankea por riesgo |

### Modelo de despliegue

- **SPP**: appliance hardened (4000/3000 Appliance) con software preinstalado. También disponible On Demand (hosted)
- **SPS**: appliance o virtual appliance; opera como proxy en la red (modo transparente o no transparente)
- **SPA**: integra datos de SPS para análisis de comportamiento

### Modos de operación SPP + SPS

| Modo | Flujo |
|------|-------|
| **SPP-initiated** | El usuario solicita acceso en el portal de SPP; al ser aprobado, se conecta al target a través de SPS |
| **SPS-initiated** | El usuario se conecta directo al servidor target; SPS intercepta el tráfico y obtiene las credenciales de SPP |

---

## Conceptos de Safeguard for Privileged Passwords (SPP)

### Entidades principales

| Entidad | Descripción |
|---------|-------------|
| **Asset** | Computadora, servidor, dispositivo de red, directorio o aplicación gestionada. Un asset solo puede estar en una partición a la vez |
| **Account** | Cuenta de usuario o servicio asociada a un asset. Una cuenta solo puede asociarse a un asset |
| **Asset Group** | Conjunto de assets que puede agregarse al scope de un entitlement |
| **Partition** | Contenedor de delegación de gestión de contraseñas y claves SSH (check/change). Permite segregar assets por dueños (SoD). Al crear una partición se crea un perfil default |
| **Profile** | Reglas y schedules que gobiernan los assets/accounts de una partición (frecuencia de check, política de cambio). Un account se gobierna por un solo perfil (explícito > implícito) |
| **Entitlement** | Conjunto de access request policies que restringen recursos, típicamente por rol de trabajo |
| **Access Request Policy** | Define el tipo de acceso (password, SSH key, sesión), condiciones (cantidad de aprobadores, horario, ticketing, reason codes) y scope (accounts, account groups, assets, asset groups) |
| **User / User Group** | Personas que acceden a Safeguard. Pueden tener permisos administrativos (Asset Admin, Security Policy Admin, User Admin, Auditor) o ser usuarios estándar (solicitar/aprobar) |
| **Discovery Job** | Descubre assets y cuentas no gestionadas para ponerlas bajo gestión |

### Jerarquía de administradores (setup inicial)

1. **Authorizer Administrator** — primer admin, crea los demás administradores
2. **Appliance Administrator** — configura el appliance (red, backups, clustering)
3. **User Administrator** — agrega usuarios y grupos
4. **Asset Administrator** — agrega sistemas gestionados (assets)
5. **Security Policy Administrator** — crea access request policies y entitlements

> [!tip] **Best practice**: seguir SoD — Asset Administrator, Security Policy Administrator, User Administrator y Auditor deben ser usuarios distintos.

### Flujo de acceso típico

1. El usuario (o una integración vía API) solicita una credencial o una sesión
2. La solicitud pasa por la access request policy (aprobaciones, condiciones)
3. Aprobada → checkout de la credencial o conexión de sesión (proxied por SPS y grabada)
4. Check-in al terminar; la política puede requerir revisión o cambio de credencial

---

## Conceptos de Safeguard for Privileged Sessions (SPS)

- **Proxy de protocolos**: SSH, Telnet, RDP, HTTP(s), ICA, VNC
- **Control de tráfico**: inspecciona el tráfico a nivel de aplicación; puede rechazar tráfico que viole el protocolo
- **Grabación**: captura keystrokes, mouse, ventanas; audit trails cifrados, timestamped y firmados criptográficamente
- **Búsqueda**: eventos indexados; playback tipo video
- **Políticas de sesión**: patrones predefinidos (comandos riesgosos, títulos de ventana sospechosos) → log, alerta o terminación de sesión
- **Modo transparente**: opera como router invisible; los usuarios no cambian su flujo de trabajo

---

## Clustering y Alta Disponibilidad

### SPP

- Clúster de **3 o 5 appliances** (join)
- Configuración compartida, replicación de toda la información
- Escalabilidad, HA y disaster recovery en una sola arquitectura
- El clúster sigue funcionando si algunos appliances fallan

### SPS

- **HA pair**: par primario + secundario (hot-spare) que replica todo y toma el control si el primario falla
- **Scalability cluster**: múltiples nodos con roles variados, controlados desde un solo pane of glass
- HA y escalabilidad se configuran independientemente

### Interoperación

- Un clúster SPP puede conectarse a uno o más clústeres SPS (SPP-SPS join)
- Combinan rotación de contraseñas + grabación de sesiones para las mismas cuentas

---

## Protocolo de actuación

### 1. Pedir contexto de la instalación

Antes de resolver cualquier cosa, preguntar al usuario (si no está explicitado):

- ¿Qué productos Safeguard están en uso? (SPP, SPS, SPA)
- ¿Versión? (8.0 LTS, 8.2, etc.)
- ¿Appliance físico, virtual u On Demand?
- ¿Clúster? (3/5 nodos SPP, HA pair SPS)
- ¿Integrado con SPP-SPS? ¿Con One Identity Manager (PAG)?
- ¿Autenticación: local, AD, SAML 2.0, RADIUS 2FA?

> Si ya tengo el contexto de la conversación actual, no pregunto de nuevo.

### 2. Buscar en Babilonia

- Buscar en `$BABILONIA/BIBLIOTECA-DE-BABEL/04-SPECIALIZED-DOMAINS/01-IAM-IDENTITY/03-ONEIDENTITY/02-SAFEGUARD-PAM/` — manual completo de SPP, SPS y SPA, organizado por secciones (`00-ARQUITECTURA` a `11-SAFEGUARD-REMOTE-ACCESS` y `99-ENABLEMENTS`)
- Si la info no existe o no alcanza → buscar en internet

### 3. Buscar en internet (web fallback)

- Documentación: `https://docs.oneidentity.com/bundle/safeguard-for-privileged-passwords_*` y `safeguard-for-privileged-sessions_*`
- Soporte: `https://support.oneidentity.com/technical-documents/safeguard-*`
- GitHub: `https://github.com/OneIdentity` (SDK, scripts de integración)

### 4. Responder / resolver

- Basar la respuesta en vault + documentación oficial + experiencia
- Si no hay documentación en Babilonia, reconocerlo y apoyarse en la oficial

### 5. Documentar (solo si el usuario lo pide explícitamente)

- Usar `obsidian-manager` para crear/actualizar notas en `$BABILONIA/BIBLIOTECA-DE-BABEL/04-SPECIALIZED-DOMAINS/01-IAM-IDENTITY/03-ONEIDENTITY/02-SAFEGUARD-PAM/`

---

## Health Check

Checklist genérico:

### 1. Appliance / servicios

- ¿Appliances accesibles? (SPP, SPS)
- ¿Estado del clúster? (todos los nodos activos, replicación OK)
- ¿Backups configurados y recientes?

### 2. Gestión de credenciales

- ¿Los últimos check/change de contraseñas fueron exitosos?
- ¿Hay accounts con check fallido? (posible causa: UAC en Windows — "Run all administrators in Admin Approval Mode" debe estar deshabilitado para reset local)
- ¿Discovery jobs corrieron correctamente?

### 3. Sesiones (SPS)

- ¿Los proxies de protocolo están operativos?
- ¿Hay sesiones grabadas correctamente?
- ¿Alertas de patrones riesgosos?

### 4. Accesos

- ¿Solicitudes de acceso procesándose normalmente?
- ¿Aprobaciones pendientes acumuladas?

### 5. Reporte

- Resumir: estado de appliances, clúster, checks de contraseñas, sesiones
- Documentar en Babilonia si el usuario lo pide

---

## API REST

- **API moderna basada en REST**: cada función está expuesta vía API
- Uso típico: integraciones, automatización de solicitudes, reportes
- Referencia: documentación de API en `https://support.oneidentity.com/technical-documents/safeguard-for-privileged-passwords/*/api-reference`
- Autenticación: tokens (login con usuario/contraseña o certificado)

---

## Troubleshooting — errores comunes

| Síntoma | Posible causa | Acción |
|---------|---------------|--------|
| Password check/change falla en Windows | UAC "Admin Approval Mode" habilitado | Deshabilitar la política local de seguridad |
| No se puede conectar a SPP | Appliance caído, red, certificados | Verificar conectividad y estado del appliance |
| Sesiones no se graban | SPS sin tráfico redirigido, política de grabación | Verificar ruteo del tráfico y configuración de SPS |
| Clúster degradado | Nodo caído, replicación fallida | Verificar estado de nodos y red entre appliances |
| Acceso denegado en solicitud | Policy sin aprobadores, condiciones no cumplidas | Revisar la access request policy y sus condiciones |

> Si el error no está documentado en Babilonia ni en la doc oficial, buscar en internet el mensaje exacto (support.oneidentity.com, community).

---

## Referencias

- SPP Administration Guide: `https://support.oneidentity.com/technical-documents/one-identity-safeguard-for-privileged-passwords/8.0%20lts/administration-guide`
- SPS: `https://support.oneidentity.com/technical-documents/safeguard-for-privileged-sessions/*`
- Escalabilidad/HA: `https://support.oneidentity.com/technical-documents/safeguard-for-privileged-sessions-on-demand/hosted/scalability-and-high-availability-in-safeguard`
- GitHub: `https://github.com/OneIdentity`