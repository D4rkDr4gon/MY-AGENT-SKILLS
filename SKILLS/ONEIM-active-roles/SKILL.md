---
name: ONEIM-active-roles
description: >
  Use when administering One Identity Active Roles — Administration Service,
  Managed Units, Access Templates, Policy Objects, workflows de aprobación,
  delegación de administración de Active Directory, reporting y troubleshooting.
  Genérico — aplica a cualquier instalación o cliente. Cross-platform (Linux + Windows).
---

# ONEIM-active-roles

## Propósito

Este skill se activa cuando el usuario necesita **administrar, operar o diagnosticar** una instalación de **One Identity Active Roles** (gestión y delegación de administración de Active Directory). Cubre:

- Arquitectura de Active Roles (presentation, service, data sources)
- Delegación de administración: Managed Units, Access Templates, Trustees
- Policy Objects y enforcement de políticas
- Workflows de aprobación y notificación
- Reporting y auditoría
- Health checks y troubleshooting

**No incluye** otros productos de la suite One Identity — usar los skills hermanos:
- `ONEIM-manager` (IGA), `ONEIM-safeguard` (PAM), `ONEIM-onelogin`, `ONEIM-password-manager`, `ONEIM-starling`.

> [!important] **Genérico por diseño**
> Este skill NO contiene información de clientes ni infraestructuras prearmadas. Siempre se trabaja en función de la instalación que el usuario describa en cada conversación.

---

## ¿Qué es Active Roles? — Contexto general

**One Identity Active Roles** es una solución de **gestión y administración delegada de Active Directory** (y otros data sources como Exchange). Permite:

1. **Delegación granular** — dar permisos administrativos limitados a usuarios/grupos sin otorgar derechos de dominio
2. **Enforcement de políticas** — reglas de negocio aplicadas consistentemente en todas las operaciones
3. **Workflows de aprobación** — operaciones que requieren aprobación antes de ejecutarse
4. **Automatización** — provisioning de home folders, membresías, sincronización con otros sistemas
5. **Auditoría** — audit trail de todas las operaciones intentadas o realizadas

### Arquitectura (3 capas funcionales)

| Capa | Componente | Rol |
|------|-----------|-----|
| **Presentación** | Active Roles Console (Windows) | Interfaz principal de administración |
| **Presentación** | Web Interface | Interfaz web para tareas administrativas delegadas |
| **Presentación** | Reporting | Generación automatizada de reportes de actividades de gestión |
| **Servicio** | Administration Service | Capa segura entre administradores y data sources. Enforcement de políticas, automatización, integración de procesos de negocio. Puede desplegarse en múltiples instancias (performance + fault tolerance) |
| **Servicio** | Administration Database | Almacena permisos, políticas y configuración de Active Roles |
| **Datos** | Active Directory / Exchange / otros | Data sources gestionados |

### Flujo de una operación

1. El administrador usa la Console o Web Interface para enviar una operación (query o cambio)
2. El **Administration Service** recibe la operación (Request object)
3. **Access check** — verifica si el usuario tiene permisos suficientes
4. **Pre-execution** — corre workflows (ej: aprobaciones) y políticas pre-ejecución (validación, generación de propiedades)
5. **Execution** — ejecuta la operación en el data source (ej: crear el usuario)
6. **Post-execution** — corre políticas post-ejecución (provisioning de home folder, membresías) y workflows post (notificaciones)

---

## Elementos de seguridad y administración

Los tres elementos clave se almacenan como objetos en la Administration Database:

| Elemento | Descripción |
|----------|-------------|
| **Access Template** | Especifica el nivel de acceso que un Trustee tiene sobre objetos/directorios. Mecanismo proxy para dar acceso a AD sin derechos especiales |
| **Policy Object** | Colección de políticas administrativas (procedimientos + eventos que los activan). Define reglas de negocio: validación, sincronización, tareas batch |
| **Managed Unit** | Unidad administrativa que agrupa objetos de AD bajo un scope de delegación |

### Trustees

- Usuarios o grupos de AD con permisos administrativos en Active Roles
- Se asignan a Managed Units, objetos o contenedores
- Al designar un Trustee se especifican los Access Templates que controlan lo que puede hacer
- **Best practice**: delegar a grupos, no a usuarios individuales

### Scope de políticas

Un Policy Object se vincula a:
- Managed Units (vistas administrativas)
- Contenedores de AD (OUs) — aplica a todos los objetos del contenedor y sub-contenedores
- Objetos individuales (leaf) — ej: un usuario específico

> [!warning] Las políticas se aplican **incluso a quienes tienen derechos de administrador** de Active Roles. Nadie las evade.

---

## Workflows

### Modelo de procesamiento

Cada operación (Request object) pasa por 4 fases:

```
Access check → Pre-execution → Execution → Post-execution
```

| Fase | Workflows | Políticas |
|------|-----------|-----------|
| **Pre-execution** | Actividades de la parte superior del diagrama (ej: **Approval**) | Pre-execution policies (validación, generación de propiedades, pre-event handlers) |
| **Post-execution** | Actividades de la parte inferior (ej: **Notification**) | Post-execution policies (provisioning, membresías, post-event handlers) |

### Reglas de matching y prioridad

- Un workflow se inicia si la operación satisface sus **start conditions**
- Pueden matchear **múltiples workflows** a una sola operación
- Orden de ejecución: atributo `edsaWorkflowPriority` (default 500; menor valor = mayor prioridad; a igualdad, orden alfabético por nombre)
- **If-Else activities** permiten branching condicional según los datos de la operación

### Actividades típicas

- **Approval** — aprobadores permiten o rechazan la operación
- **Notification** — mails informando la finalización
- **Script** — lógica custom
- **If-Else** — branching condicional

---

## Protocolo de actuación

### 1. Pedir contexto de la instalación

Antes de resolver cualquier cosa, preguntar al usuario (si no está explicitado):

- ¿Qué versión de Active Roles? (7.x, 8.0.x, 8.1.x)
- ¿Cuántas instancias del Administration Service? ¿HA?
- ¿Qué data sources gestiona? (AD, Exchange, otros)
- ¿Qué elementos están en uso? (Managed Units, Policy Objects, workflows)
- ¿Integrado con Starling? (Starling Join, 2FA)

> Si ya tengo el contexto de la conversación actual, no pregunto de nuevo.

### 2. Buscar en Babilonia

- Buscar en `$BABILONIA_ONEIDENTITY/` — documentación existente
- Si la info no existe o no alcanza → buscar en internet

### 3. Buscar en internet (web fallback)

- Documentación: `https://docs.oneidentity.com/bundle/active-roles_*`
- Soporte: `https://support.oneidentity.com/technical-documents/active-roles/*`
- GitHub: `https://github.com/OneIdentity`

### 4. Responder / resolver

- Basar la respuesta en vault + documentación oficial + experiencia
- Si no hay documentación en Babilonia, reconocerlo y apoyarse en la oficial

### 5. Documentar (solo si el usuario lo pide explícitamente)

- Usar `obsidian-manager` para crear/actualizar notas en `$BABILONIA_ONEIDENTITY/`

---

## Health Check

Checklist genérico:

### 1. Servicios

- ¿Administration Service corriendo? ¿Todas las instancias responden?
- ¿Administration Database accesible?
- ¿Web Interface responde?

### 2. Operaciones

- ¿Hay operaciones fallidas o atascadas en workflows de aprobación?
- ¿Aprobaciones pendientes acumuladas?
- ¿Errores recurrentes en el audit trail?

### 3. Sincronización / integraciones

- ¿Integraciones con otros sistemas (scripts en Policy Objects) funcionando?
- ¿Integración con Starling (si aplica) activa?

### 4. Reporte

- Resumir: servicios, operaciones, aprobaciones pendientes
- Documentar en Babilonia si el usuario lo pide

---

## Troubleshooting — errores comunes

| Síntoma | Posible causa | Acción |
|---------|---------------|--------|
| Operación denegada | Access check falla (Trustee sin Access Template suficiente) | Verificar asignaciones de Trustee y Access Templates |
| Workflow no se dispara | Start conditions no satisfechas | Revisar las condiciones del workflow |
| Aprobación nunca llega | Aprobadores sin cuenta válida, mail no configurado | Verificar destinatarios y configuración de notificaciones |
| Política no aplica | Policy Object no vinculado al scope correcto | Verificar el vínculo (Managed Unit, OU, objeto) |
| Administration Service lento | Múltiples instancias desbalanceadas, DB lenta | Revisar instancias y performance de la Administration Database |

> Si el error no está documentado en Babilonia ni en la doc oficial, buscar en internet el mensaje exacto (support.oneidentity.com, community).

---

## Referencias

- Technical overview: `https://docs.oneidentity.com/bundle/active-roles_administration-guide_8.0.1/page/guides/administrationguide/technical-overview.htm`
- Workflow processing: `https://docs.oneidentity.com/bundle/active-roles_administration-guide_8.0.1/page/guides/administrationguide/workflow-processing-overview.htm`
- Policy Objects: `https://docs.oneidentity.com/bundle/active-roles_administration-guide_8.1.3/page/guides/administrationguide/how-policy-objects-work.htm`
- Service components: `https://docs.oneidentity.com/bundle/active-roles_feature-guide_8.1.3/page/guides/featureguide/service-components.htm`
- GitHub: `https://github.com/OneIdentity`