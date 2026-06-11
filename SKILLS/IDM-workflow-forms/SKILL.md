---
name: IDM-workflow-forms
description: >
  Use when working with Workflow JSON forms for IDM — Form Builder, fields,
  components, buttons (submit/approve/reject), eventos custom, JavaScript logic,
  data mapping, precarga de datos. Cross-platform (Linux + Windows).
---

# IDM-workflow-forms

## Propósito

Este skill se activa cuando el usuario plantea tareas relacionadas con **Workflow Forms JSON** de OpenText Identity Manager (IDM). Cubre el diseño, configuración, troubleshooting y mantenimiento de formularios creados con el **Form Builder** integrado en Designer.

**No incluye** drivers IDM (usar `IDM-identity-drivers`), servidores (usar `IDM-identity-servers`), certificados (`enterprise-certificates`), ni NAM (`NAM-access-manager`).

---

## Contexto técnico del Form Builder

### ¿Qué es el Form Builder?

El **Form Builder** es una herramienta visual de **drag & drop** integrada en Designer (IDM 4.8+) para crear formularios modernos en formato **JSON**. Reemplaza al método legacy (XML/Dojo) y está basado en la tecnología de **Form.IO** (https://form.io).

Los formularios creados con Form Builder:
- Se almacenan como **JSON Schema** en el contenedor `Workflow Forms` del driver de **User Application** en eDirectory.
- Se renderizan en el navegador a través del **Form Renderer** de Identity Apps.
- Son **responsivos** y con **apariencia moderna** (vs. los legacy que usan Dojo).
- Soportan **JavaScript nativo** para lógica custom, llamadas REST y eventos.

### Tipos de formularios

| Tipo | Propósito |
|------|-----------|
| **Approval Forms** | Pantallas de aprobación/rechazo en actividades de Approval |
| **Request Forms** | Formularios de solicitud inicial (request) |
| **Template Forms** | Plantillas para el asistente "Create Workflow Form" |

### Arquitectura

```
Designer (Form Builder)
  └── JSON Schema (formulario)
       └── Se almacena en eDirectory: system\driverset\UserAppDriver\Workflow Forms\
            └── Se asocia a un Provisioning Request Definition (PRD)
                 └── Se despliega al Identity Vault
                      └── Workflow Engine lo lee durante ejecución
                           └── Form Renderer lo muestra en Identity Apps (navegador)
                                └── Usuario interactúa → datos viajan como JSON
                                     └── Workflow Engine persiste en BD de workflow
```

### Form.IO heritage

- El Form Builder de IDM hereda la arquitectura de **Form.IO**: JSON schema, componentes drag & drop, renderizado.
- Cada componente arrastrado al formulario genera su schema JSON internamente.
- El schema define la estructura, validaciones, eventos y lógica del formulario.
- El editor JSON permite modificar ese schema directamente.

### Componentes principales

**Básicos:**
- `Text Field` — texto corto
- `Text Area` — texto multilínea
- `Number` — numérico con validación
- `Checkbox` — booleano (true/false)
- `Select Boxes` — selección múltiple
- `Radio` — selección única

**Avanzados:**
- `Select` — desplegable. Soporta listas estáticas o dinámicas vía REST (RoleVault, Identity Vault)
- `Data Grid` — tabla dinámica con filas agregables
- `Dynamic Entity Component` — entidades dinámicas del vault

### Eventos y JavaScript

Cada componente soporta eventos:
- `onLoad` — al cargar el formulario
- `onChange` — al cambiar el valor
- `onSubmit` — al enviar

El **JS Editor** global permite agregar/modificar métodos JavaScript para todos los campos en un solo lugar. Soporta:
- Llamadas REST a APIs internas (RoleVault, Identity Vault) o externas
- Lógica condicional
- Manipulación de datos del formulario

### Botones de acción

Los botones Request/Approve/Reject usan **eventos custom** con JavaScript:

```javascript
// Botón Request (submit)
if(checkValidateOnSubmit(instance, data)) {
    requestAlert(util, requestPayload);
} else {
    console.warn("Invalid form");
}

// Botón Approval
if(checkValidateOnSubmit(instance, data)) {
    approvalAlert(util, decisionPayload);
}

// Botón Reject
if(checkValidateOnSubmit(instance, data)) {
    rejectAlert(util, decisionPayload);
}
```

### Data Item Mapping

Cada campo del formulario se mapea al `flowdata` del workflow mediante:
- **Pre-activity mapping**: precarga datos antes de mostrar el formulario
- **Post-activity mapping**: guarda datos modificados al `flowdata` después del submit

El **API Key** de cada campo (property crucial en JSON) debe coincidir exactamente con el nombre del nodo en `flowdata`, o los datos se pierden.

### Migración Legacy → JSON

**No existe herramienta de migración automática.** El proceso es:
1. Hacer backup del PRD legacy
2. Crear nuevo formulario JSON en Form Builder
3. Crear nuevo PRD o asociar el formulario JSON al PRD existente (seleccionando JSON Forms)
4. Mapear campos manualmente en Data Item Mapping
5. Desplegar desde Designer
6. **Importante**: al seleccionar JSON Forms, Designer borra todos los forms legacy asociados anteriormente

---

## Protocolo de actuación

Siempre que se invoque este skill, seguir estos pasos:

### 1. Pedir contexto del cliente

Antes de resolver cualquier cosa, pregunto al usuario **de qué cliente se trata** (si no está explicitado). Necesito saber:

- ¿Es un formulario nuevo o existente?
- ¿Qué versión de IDM? (4.8, 4.10, CE 24.4)
- ¿El formulario es tipo Request, Approval o Template?
- ¿Está asociado a un PRD existente?
- ¿Usa Form Builder (JSON) o es legacy (XML)?
- ¿El formulario se despliega desde Designer?
- ¿Hay problemas específicos? (validación, datos que no fluyen, botones, etc.)

> Si ya tengo el contexto de la conversación actual, no pregunto de nuevo.

### 2. Revisar Babilonia

Buscar en `$BABILONIA_IDM/04-WF JSON/` si existe documentación relevante al tema. Leer los documentos aplicables y citarlos como fuente.

### 3. Responder / resolver

- Si hay documentación en el vault, basar la respuesta en ella + documentación oficial de OpenText + experiencia técnica.
- Si no hay documentación, reconocerlo y resolver con fuente oficial o conocimiento propio.

### 4. Documentar (solo si el usuario lo pide explícitamente)

Si el usuario dice "documentalo" o "guardalo en el vault", usar `obsidian-manager` para crear el documento en la carpeta correspondiente de `$BABILONIA_IDM/04-WF JSON/`.

---

## Vault — Ubicación de documentación

| Área | Ruta (via env var) |
|------|-------------------|
| IDM — WF JSON (teoría) | `$BABILONIA_IDM/04-WF JSON/` |
| IDM — WF JSON (campos) | `$BABILONIA_IDM/04-WF JSON/campos/` |
| IDM — WF JSON (Form.IO) | `$BABILONIA_IDM/04-WF JSON/FORM.IO/` |

> **Nota:** La documentación en Babilonia cubre casos puntuales de campos y configuraciones comunes, pero NO es exhaustiva. El Form Builder es una herramienta amplia y muchas configuraciones avanzadas (componentes custom, APIs complejas, integraciones) no están documentadas allí.

---

## Buenas prácticas y tips clave

### API Key
- Es el identificador **crítico** del campo. Si cambia el Label, verificar que el API Key no cambie automáticamente.
- Debe coincidir exactamente con el nombre del nodo en `flowdata` para que los datos fluyan correctamente.

### Data Item Mapping
- Siempre verificar que los campos JSON estén mapeados correctamente en el PRD.
- Usar pre-activity mapping para valores por defecto o datos calculados.
- Usar post-activity mapping para persistir datos modificados.

### Botones
- Todo botón Request/Approve/Reject debe tener un **evento custom**.
- Usar `checkValidateOnSubmit()` para validar antes de ejecutar la acción.
- Si no se ejecuta la acción, revisar la consola del navegador (F12).

### Select con datos dinámicos
- Usar el JS Editor para configurar llamadas REST.
- Funciones útiles: `RoleVault.getUsers()`, `RoleVault.getRolesUserIn()`, etc.
- Configurar `"refreshOn"` para que el Select se actualice cuando cambie otro campo.

### Debugging
- Consola del navegador (F12) para ver errores JavaScript.
- Revisar que el formulario esté desplegado en eDirectory.
- Verificar que el PRD tenga JSON Forms seleccionado.
- Logs del workflow engine para ver si los datos llegan.

### Migración
- **Siempre hacer backup** del PRD legacy antes de migrar.
- No hay vuelta atrás automática: una vez seleccionado JSON Forms, los forms legacy se borran.
- Migrar de a un formulario por vez.

### Buenas prácticas generales
- No editar los forms default que vienen con el producto (Approval Form, Request Form, etc.).
- Hacer copias de los default y modificar las copias.
- Documentar cada formulario: qué PRD usa, qué campos tiene, qué APIs consume.
- Versionar los JSON exports en el vault (Babilonia).

---

## Cross-platform

| Aspecto | Linux | Windows |
|---------|-------|---------|
| Designer | Sí (Eclipse-based) | Sí (Eclipse-based) |
| Form Builder | Integrado en Designer | Integrado en Designer |
| Form Renderer | Identity Apps (browser) | Identity Apps (browser) |
| Consola debug | Navegador (F12) | Navegador (F12) |
| Despliegue | Desde Designer a eDirectory | Desde Designer a eDirectory |
| Ruta vault | `$BABILONIA_IDM/04-WF JSON/` | `$env:BABILONIA_IDM/04-WF JSON/` |

> El Form Builder es multiplataforma en tanto Designer corre en cualquier SO con Eclipse. El renderizado final es siempre vía navegador web.

---

## Referencias oficiales

- [OpenText IDM CE 24.4 (v4.10) — Administrator's Guide to Form Builder](https://www.netiq.com/documentation/identity-manager-4.10/form_builder/data/form_builder.html)
- [OpenText IDM CE 24.4 (v4.10) — Guide to Designing Identity Apps (About Forms)](https://www.netiq.com/documentation/identity-manager-4.10/identity_apps_design/data/about-prd-forms.html)
- [Form.IO Documentation](https://help.form.io/developers/form-development/form-builder)
- [NetIQ IDM 4.8 — Admin Guide to Form Builder](https://www.netiq.com/documentation/identity-manager-48/form_builder/data/form_builder.html)

---

## Librerías JavaScript internas (workflow)

En el vault existen librerías JavaScript utilitarias usadas en los workflows JSON de los clientes. Están en una ubicación separada del resto de la documentación de IDM.

### Ubicación

| Librería | Ruta (via env var) | Propósito |
|----------|-------------------|-----------|
| Utilidades generales | `$BABILONIA/Manuales/05-PRACTICAL-RESOURCES/01-SCRIPTS/JAVASCRIPT/WorkFlowUtils-General.js` | Validaciones, checks de ambiente, funciones transversales |
| Manejo de listas | `$BABILONIA/Manuales/05-PRACTICAL-RESOURCES/01-SCRIPTS/JAVASCRIPT/WorkFlowUtils-Lists.js` | Manipulación de componentes Select (listas desplegables) en formularios JSON |
| Alertas visuales | `$BABILONIA/Manuales/05-PRACTICAL-RESOURCES/01-SCRIPTS/JAVASCRIPT/WorkFlowUtils-sweetalert2.js` | Librería SweetAlert2 para modales y notificaciones en formularios |

### Cuándo usarlas

- Cuando el usuario pida resolver un problema que involucre lógica JavaScript en un formulario JSON
- Cuando se requiera validación de datos, limpieza de listas, o mensajes visuales al usuario
- Cuando se esté armando un formulario nuevo y se necesiten las utilidades base

### Cómo referenciarlas

Cuando corresponda, usar **`obsidian-manager`** para leer la librería relevante y extraer la función/funcionalidad que resuelva el problema puntual del usuario, sin exponer el código completo ni nombres de funciones internas salvo que el usuario los pida explícitamente.

> ⚠️ **No documentar ni replicar** el contenido de estas librerías en Babilonia sin autorización expresa del usuario. Son de uso interno del equipo.
