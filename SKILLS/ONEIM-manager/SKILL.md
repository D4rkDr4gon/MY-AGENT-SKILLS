---
name: ONEIM-manager
description: >
  Use when administering One Identity Manager (IGA) — architecture, IT Shop &
  workflows, connectors (AD, CSV, custom), Manager/Web Portal/Web Designer,
  Job Queue/DBQueue, health checks, logs, troubleshooting, API REST y PowerShell.
  Genérico — aplica a cualquier instalación o cliente. Cross-platform (Linux + Windows).
---

# ONEIM-manager

## Propósito

Este skill se activa cuando el usuario necesita **administrar, operar o diagnosticar** una instalación de **One Identity Manager** (la plataforma IGA de One Identity, antes Quest). Cubre:

- Arquitectura genérica de One Identity Manager y sus componentes
- IT Shop: solicitudes, aprobaciones, roles, recursos y workflows
- Configuración de conectores (Active Directory, CSV, custom)
- Health checks y diagnóstico de componentes
- Logs y troubleshooting
- API REST y PowerShell

**No incluye** otros productos de la suite One Identity — usar los skills hermanos:
- `ONEIM-safeguard` (PAM), `ONEIM-active-roles`, `ONEIM-onelogin`, `ONEIM-password-manager`, `ONEIM-starling`.

> [!important] **Genérico por diseño**
> Este skill NO contiene información de clientes ni infraestructuras prearmadas. Siempre se trabaja en función de la instalación que el usuario describa en cada conversación.

---

## ¿Qué es One Identity Manager? — Contexto general

**One Identity Manager** es una plataforma de **Identity Governance & Administration (IGA)** que cubre:

1. **Identity Lifecycle** — gestión del ciclo de vida de identidades (altas, bajas, modificaciones)
2. **Governance** — roles, políticas, SoD (Separation of Duties), risk assessment
3. **Application Governance** — aprovisionamiento y gobierno de accesos a aplicaciones
4. **Compliance Audit** — auditoría y evidencia de todos los eventos
5. **Self-Service Access** — portal de autoservicio para usuarios finales
6. **Attestation / Recertification** — campañas de certificación de accesos
7. **Privileged Access Governance** — gobierno de accesos privilegiados (integra con Safeguard)

### Arquitectura (3-tier clásica)

| Capa | Componente | Rol |
|------|-----------|-----|
| **Datos** | SQL Server / Azure SQL / Amazon RDS | Base de datos central. Dos partes lógicas: **payload** (identidades, cuentas, grupos, aprobaciones, attestation, compliance) y **metadata** (modelo de datos, scripts, configuración del sistema, colas asíncronas) |
| **Lógica** | Object Layer (VI.DB) | Acceso orientado a objetos a la base. Entidades, UnitOfWork, eventos Insert/Update/Delete |
| **Lógica** | One Identity Manager Service (Job Server) | Único componente autorizado a hacer cambios en sistemas destino. Procesa pasos del Job Queue, sincroniza con target systems, ejecuta procesos |
| **Lógica** | Application Server | Pool de conexiones a la DB, lógica de negocio para clientes. Conexión segura a la base |
| **Presentación** | Manager (cliente .NET) | Front-end principal de administración |
| **Presentación** | Web Portal | Portal de autoservicio para usuarios finales |
| **Presentación** | Web Designer | Diseño de formularios y procesos web |
| **Presentación** | Administration Portal | Administración vía web |
| **Presentación** | Operations Support Web Portal | Operaciones |
| **Presentación** | Password Reset Portal | Autoservicio de contraseñas |
| **Presentación** | API Server | Despliega los portales web + expone la API REST |

### Mecanismos internos clave

| Mecanismo | Descripción |
|-----------|-------------|
| **DBQueue** | Lista de tareas de recálculo de herencia. Los triggers de la DB encolan tareas; el DBQueue Processor las procesa |
| **JobQueue** | Órdenes de procesamiento que ejecuta el object layer (procesos, pasos) |
| **Jobgenerator** | Convierte plantillas de scripts en procesos concretos en el Job Queue |
| **Procesos** | Mapean procesos de negocio: pasos con relaciones predecesor/sucesor, modelados con process templates |
| **Herencia** | Propiedades heredadas a lo largo de estructuras jerárquicas (departamentos, centros de costo, ubicación, roles de negocio) |

### Herramientas del producto

| Herramienta | Uso |
|-------------|-----|
| **Manager** | Administración principal (cliente .NET) |
| **Designer** | Diseño de esquema, procesos, formularios (equivalente al Designer de NetIQ IDM) |
| **Configuration Wizard** | Configuración inicial de la instalación |
| **Database Compiler** | Compilación de la base (schema, procesos) |
| **Database Transporter** | Transporte de cambios entre entornos (dev → test → prod) |
| **Job Service Configuration** | Configuración del One Identity Manager Service (archivo de configuración, Windows y Linux daemon) |
| **Schema Extension** | Extensión del esquema |
| **License Meter** | Medición de licencias |
| **Software Loader** | Carga de software/actualizaciones |
| **Server Installer** | Instalación de componentes en servidores |
| **API Server** | Despliegue de portales web + API REST |
| **Data Import** | Importación de datos |
| **Report Editor** | Edición de reportes |
| **Crypto Configuration** | Configuración criptográfica |
| **System Debugger** | Debug del sistema |

### Ediciones

- **Standard Edition**: módulos base de gestión de identidades
- **Full Edition**: incluye todos los módulos de gestión (IT Shop & workflow, delegación, system roles y business roles, role mining, risk assessment, attestation, compliance, company policies, report subscriptions), Unified Namespace y conectores para Active Directory

---

## Protocolo de actuación

### 1. Pedir contexto de la instalación

Antes de resolver cualquier cosa, preguntar al usuario (si no está explicitado en la conversación):

- ¿Qué versión de One Identity Manager? (9.x, 10.0, etc.)
- ¿Qué edición? (Standard / Full)
- ¿Base de datos? (SQL Server on-prem, Azure SQL, Amazon RDS)
- ¿Topología? (Job Server, Application Server, API Server — ¿en un solo servidor o distribuidos?)
- ¿Qué front-ends están en uso? (Manager, Web Portal, Web Designer, Administration Portal)
- ¿Qué conectores están configurados? (AD, CSV, SAP, custom)
- ¿Sistema operativo de los servidores? (Windows Server / Linux con Docker)
- ¿Hay clúster / HA?

> Si ya tengo el contexto de la conversación actual, no pregunto de nuevo.

### 2. Buscar en Babilonia

- Buscar en `$BABILONIA_ONEIDENTITY/` — documentación existente (instalación Docker, conectores AD/CSV, presales IGA)
- Si la info no existe o no alcanza → buscar en internet

### 3. Buscar en internet (web fallback)

- Documentación oficial: `https://docs.oneidentity.com/bundle/one-identity-manager_*`
- Soporte: `https://support.oneidentity.com/technical-documents/identity-manager/*`
- GitHub: `https://github.com/OneIdentity` (scripts, ejemplos, SDK)
- Community: foros de One Identity

### 4. Responder / resolver

- Basar la respuesta en vault + documentación oficial + experiencia
- Si no hay documentación en Babilonia, reconocerlo y apoyarse en la oficial

### 5. Documentar (solo si el usuario lo pide explícitamente)

- Usar `obsidian-manager` para crear/actualizar notas en `$BABILONIA_ONEIDENTITY/`
- Estructura sugerida: `00-IDENTITY GOVERNANCE & ADMINISTRATION/` (instalación, conectores), `99-OTHER/` (investigación, errores)

---

## IT Shop & Workflows

### Conceptos del IT Shop

| Concepto | Descripción |
|----------|-------------|
| **IT Shop** | Catálogo de servicios de TI donde los usuarios solicitan recursos (roles, grupos, aplicaciones) |
| **Shopping Cart** | Carrito de solicitudes del usuario en el Web Portal |
| **Solicitud (Request)** | Pedido de un recurso del catálogo; dispara un proceso de aprobación |
| **Aprobación** | Pasos de aprobación configurados en el proceso (uno o varios aprobadores, escalamiento) |
| **Recurso (Resource)** | Entidad solicitable: rol, grupo, aplicación, cuenta |
| **Rol** | Agrupación de recursos con asignación a identidades (system roles, business roles) |
| **Asignación (Assignment)** | Vínculo entre identidad y recurso/rol; puede ser directa o por herencia |
| **Proceso (Process)** | Flujo de pasos que ejecuta la asignación/desasignación (creación de cuenta, membresía, etc.) |

### Flujo típico de solicitud

1. Usuario solicita un recurso desde el Web Portal (IT Shop)
2. Se genera una solicitud con estado (pendiente, en aprobación, aprobada, rechazada)
3. El proceso de aprobación corre (aprobadores según política)
4. Aprobada → el proceso de asignación se encola en el Job Queue
5. El One Identity Manager Service ejecuta los pasos (crear cuenta en AD, agregar a grupo, etc.)
6. El usuario ve el resultado en el portal; todo queda auditado

### Configuración de workflows

- Los procesos se modelan con **process templates** en el Designer
- Cada proceso tiene pasos con relaciones predecesor/sucesor
- Los pasos pueden incluir: aprobaciones, tareas manuales, acciones automáticas (scripts), notificaciones por mail
- El **Jobgenerator** convierte las plantillas en procesos concretos en el Job Queue
- Verificación: `Job Queue Info` (herramienta) para monitorear procesos en cola

---

## Conectores

### Conector Active Directory

Pasos genéricos de configuración:

1. **Prerrequisitos**: cuenta de servicio con permisos de lectura/escritura en el dominio, conectividad de red, DNS resoluble
2. **Instalación**: el conector se instala como machine role en el Job Server (o Remote Loader si aplica)
3. **Configuración en Manager**: crear el sistema destino (target system) con los datos del dominio (FQDN, cuenta de servicio)
4. **Sincronización inicial**: correr el proceso de carga inicial (importación de usuarios, grupos, OUs)
5. **Mapeo de esquema**: verificar que los atributos de AD mapean correctamente al esquema de One Identity Manager
6. **Procesos de aprovisionamiento**: verificar que los procesos de creación/modificación/eliminación de cuentas están activos
7. **Prueba**: crear una identidad de prueba y verificar la provisión en AD

### Conector CSV

1. Definir la **estructura del CSV** (columnas, delimitador, encoding)
2. Configurar el conector con la ruta del archivo y el mapeo de columnas → atributos
3. Programar la importación (job recurrente) o importación manual
4. Verificar el procesamiento en el Job Queue

### Conectores custom (Custom Connect)

- Se pueden desarrollar conectores custom para aplicaciones sin conector oficial
- Usar la API REST o scripts en los procesos de aprovisionamiento
- Referencia: integraciones en `https://www.oneidentity.com/mx-es/one-identity-manager-integration/`

---

## Health Check diario

Checklist genérico para verificar el estado de una instalación:

### 1. Servicios del sistema

| Servicio | Verificación |
|----------|--------------|
| One Identity Manager Service (Job Server) | ¿Está corriendo? ¿Configuración válida? |
| Application Server | ¿Responde? ¿Pool de conexiones OK? |
| API Server / IIS / web server | ¿Portales responden? |
| SQL Server | ¿Base accesible? ¿Espacio en disco? |

### 2. Colas de procesamiento

- **Job Queue**: ¿hay procesos atascados o en error? (Job Queue Info)
- **DBQueue**: ¿hay tareas de recálculo pendientes acumuladas?
- Procesos fallidos: revisar el error y re-ejecutar si corresponde

### 3. Sincronización con target systems

- ¿Los conectores (AD, CSV, etc.) sincronizaron en el último ciclo?
- ¿Hay errores de conexión con los sistemas destino?

### 4. Logs

- Revisar logs del One Identity Manager Service y del Application Server
- Buscar errores recurrentes (autenticación, conexión a DB, permisos)

### 5. Reporte

- Resumir: servicios OK/FAIL, colas, errores encontrados
- Documentar en Babilonia si el usuario lo pide

---

## Logs

| Componente | Dónde mirar |
|------------|-------------|
| One Identity Manager Service | Logs del servicio en el Job Server (Windows: Event Viewer / archivos del servicio; Linux: syslog / archivos del daemon) |
| Application Server | Logs de la aplicación en el servidor de aplicaciones |
| API Server / Web | Logs del web server (IIS / nginx) y de la aplicación |
| SQL Server | SQL Server error log, deadlocks, bloqueos |
| Procesos | Job Queue Info — estado de cada proceso/paso |

---

## API REST y PowerShell

### API REST

- El **API Server** expone la API REST de One Identity Manager
- Referencia: `https://support.oneidentity.com/technical-documents/identity-manager/9.1.1/rest-api-reference-guide/`
- Uso típico: integraciones, automatización, consulta de identidades/roles

### PowerShell

- Módulo `OneIdentity.PowerShell` (cmdlets para One Identity Manager)
- Operaciones típicas: consultar identidades, roles, solicitudes; disparar procesos
- Verificar disponibilidad según versión instalada

---

## Troubleshooting — errores comunes

| Síntoma | Posible causa | Acción |
|---------|---------------|--------|
| Procesos atascados en Job Queue | Servicio detenido, permisos, error en paso | Revisar log del paso, re-ejecutar, verificar servicio |
| Sincronización AD falla | Cuenta de servicio sin permisos, conectividad, DNS | Verificar credenciales y conectividad |
| Web Portal no responde | API Server / web server caído, DB inaccesible | Verificar servicios y conexión a DB |
| Recálculo de herencia lento | DBQueue acumulada, índices | Monitorear DBQueue, revisar performance de DB |
| Error de permisos en Manager | Usuario sin roles de administración | Verificar asignaciones de administrador en Manager |

> Si el error no está documentado en Babilonia ni en la doc oficial, buscar en internet el mensaje exacto (support.oneidentity.com, community).

---

## Referencias

- Instalación: `https://support.oneidentity.com/es-es/technical-documents/identity-manager/8.2/installation-guide` (y versiones nuevas)
- Arquitectura: `https://docs.oneidentity.com/bundle/one-identity-manager_configuration_10.0/page/sources/config/architecture/oneimarchitectureoverview.html`
- Web Portal: `https://docs.oneidentity.com/bundle/one-identity-manager_web-portal_10.0/`
- API REST: `https://support.oneidentity.com/technical-documents/identity-manager/9.1.1/rest-api-reference-guide/`
- GitHub: `https://github.com/OneIdentity`
- Integraciones: `https://www.oneidentity.com/mx-es/one-identity-manager-integration/`