---
name: dedalo-wf-json
description: >
  Use when working with Workflow JSON forms for IDM — Form Builder, fields,
  components, buttons (submit/approve/reject), eventos custom, JavaScript logic,
  data mapping, precarga de datos. Cross-platform (Linux + Windows).
---

# dedalo-wf-json

Contexto sobre **Workflow JSON (Form Builder)** de NetIQ Identity Manager.

> **Base tecnológica:** El Form Builder de IDM está construido sobre **Form.IO** (https://form.io) — una plataforma open-source de construcción de formularios JSON. Los componentes, el schema JSON y el motor de renderizado de IDM heredan directamente de Form.IO. La documentación oficial de Form.IO se ha descargado al vault como recurso complementario.

## Ubicación de la documentación en el vault

| Área | Linux | Windows |
|------|-------|---------|
| IDM WF JSON | `/files/Personal-Vault/Manuales/04-SPECIALIZED-DOMAINS/01-IAM-IDENTITY/01-IDM/04-WF JSON/` | `C:\Users\lcampassi\Proton Drive\D4rkDr4g0n19\My files\Personal-Vault\Manuales\04-SPECIALIZED-DOMAINS\01-IAM-IDENTITY\01-IDM\04-WF JSON\` |
| WORK — Clientes | `/files/Personal-Vault/WORK/` | `C:\Users\lcampassi\Proton Drive\D4rkDr4g0n19\My files\Personal-Vault\WORK\` |

Los canvases (`.canvas`) de workflows por cliente están en `WORK/<CLIENTE>/`.

## Documentación disponible

### Teoría
- `Modulo Teorico - Forms JSON.md` — Conceptos fundamentales de Form Builder IDM 4.8: componentes, propiedades, migración de Legacy a JSON
- `Form Builder.md` — Guía del Form Builder
- `Botones aprobacion, submit, reject.md` — Eventos custom para botones con JavaScript

### Campos
- `Campo WF Json componente lista multiple data con buscador.md`
- `Campo WF Json multi asignacion de lista estatica.md`
- `Campo WF Json multi asignacion de objeto custom.md`
- `Campo WF json picklist con event handler para OnClick.md`
- `Campo WF Json Select simple selection.md`
- `Como definir un campo oculto en WF json.md`
- `Precarga de datos HTML visuales a partir de un campo de seleccion de usuarios.md`
- `Precarga de datos HTML visuales a partir de una precarga de usuario.md`

## Conceptos clave

### Arquitectura
- Form Builder genera esquemas JSON (reemplaza XML Legacy)
- Independiente del motor de Eclipse Designer
- Renderizado vía Form Renderer en Dashboard de Identity Apps
- Editable tanto gráficamente como en editor JSON/JS directo

### Componentes principales
- **Básicos**: Text Field, Text Area, Number, Checkbox, Select Boxes, Radio
- **Avanzados**: Select (listas estáticas o dinámicas vía REST), Data Grid, Dynamic Entity Component

### Propiedades
- **Property/Display**: label, tooltip, disabled, hidden
- **Validation**: required, max/min length, regex
- **Calculated Value/API**: valores calculados, llamadas REST

### Botones y eventos
- **Request** (submit): `checkValidateOnSubmit()` + `requestAlert()`
- **Approval** (aprobar): `checkValidateOnSubmit()` + `approvalAlert()`
- **Reject** (rechazar): similar con `rejectAlert()`
- Eventos custom JavaScript para lógica de aprobación

### Data mapping
- Los campos deben mapearse a nodos de `flowdata`
- Migración Legacy → JSON requiere rediseño manual desde cero

## Documentación de Form.IO (descargada)

La documentación oficial de **Form.IO** se descargó desde `https://help.form.io/llms-full.txt` (export completo GitBook en markdown).

### Ubicación en el vault

| Archivo | Ruta (cross-platform) |
|---------|-----------------------|
| Export completo | `Manuales/04-SPECIALIZED-DOMAINS/01-IAM-IDENTITY/01-IDM/04-WF JSON/FORM.IO/llms-full.txt` |

### Qué contiene
- **~1.2MB** de documentación completa en texto plano
- Creada con GitBook — misma plataforma que el vault de Babilonia
- Incluye: Form Builder, componentes (Basic, Advanced, Data, Layout, Premium), Form JSON schema, Actions (Email, Webhook, OAuth, LDAP), Roles & Permissions, Embedding, API docs, Deployment guides
- Páginas individuales disponibles como `.md` en `https://help.form.io/<path>.md`

### Consulta dinámica
La documentación online soporta consultas vía API:
```
GET https://help.form.io/<path>.md?ask=<pregunta>
```
Útil si la copia local se desactualiza o se necesita contexto adicional.
