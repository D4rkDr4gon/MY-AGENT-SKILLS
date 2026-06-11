---
name: orchestrator-manager
description: >
  Use when you need to orchestrate multiple subagent instances working in parallel
  on a large task while maintaining coherence. Covers the full protocol: planning,
  manifest creation, worker dispatch, staging, reconciliation, and failure handling.
  Generic — works with any subagent type and any task type (docs, code, analysis, search, refactor).
---

# orchestrator-manager

Protocolo genérico de orquestación paralela para subagentes opencode.

> **Filosofía**: Un agente orquestador planifica la tarea, la divide en work items,
> lanza N workers paralelos que trabajan en aislamiento (staging), y finalmente
> reconcilia y mergea los resultados en un output coherente.

---

## Índice

1. [¿Cuándo usarlo?](#cuándo-usarlo)
2. [El Protocolo en 4 Fases](#el-protocolo-en-4-fases)
3. [Fase 1 — PLAN](#fase-1--plan)
4. [Fase 2 — LAUNCH](#fase-2--launch)
5. [Fase 3 — RECONCILE](#fase-3--reconcile)
6. [Fase 4 — MERGE](#fase-4--merge)
7. [Formato del Manifest](#formato-del-manifest)
8. [Estrategias de Distribución](#estrategias-de-distribución)
9. [Manejo de Fallos](#manejo-de-fallos)
10. [Validación y Coherencia](#validación-y-coherencia)
11. [Ejemplos de Uso](#ejemplos-de-uso)
12. [Integración con Agentes Existentes](#integración-con-agentes-existentes)
13. [Templates](#templates)

---

## ¿Cuándo usarlo?

Usá `orchestrator-manager` cuando:
- Tenés una tarea que se puede dividir en **múltiples work items independientes**
- Querés **paralelizar** invocando N workers simultáneos
- Necesitás que los resultados sean **coherentes entre sí** (IDs únicos, estilo consistente, sin colisiones)
- El trabajo involucra **escritura a disco** (archivos, docs, código, etc.) y necesitás evitar que se pisen

| Tipo de tarea | `output.type` | Ejemplo concreto |
|---------------|---------------|------------------|
| Documentación | `file` | Crear 20 notas de criptografía con proteo |
| Análisis | `data` | Analizar 100 muestras de malware con hecate |
| Búsqueda | `data` | Escanear 50 hosts con argos |
| Código | `file` | Generar 10 scripts de automatización con prometeo |
| Refactor | `file` | Renombrar 30 archivos siguiendo una convención |
| Reporte | `data` | Correlacionar logs de 5 fuentes con apolo |

**No** usarlo para:
- Tareas estrictamente secuenciales (item B depende de item A)
- Tareas que un solo worker puede resolver en una llamada
- Operaciones que requieren estado compartido en tiempo real

---

## El Protocolo en 4 Fases

```
┌─────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR                              │
│  (hefesto, atlas, o cualquier agente primario) │
└──────────┬──────────┬──────────┬──────────┬─────────────────┘
           │          │          │          │
           ▼          ▼          ▼          ▼
      ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
      │ worker │ │ worker │ │ worker │ │ worker │  ← Mismo subagente,
      │  #1    │ │  #2    │ │  #3    │ │  #N    │    múltiples instancias
      └───┬────┘ └───┬────┘ └───┬────┘ └───┬────┘
          │          │          │          │
          ▼          ▼          ▼          ▼
      ┌─────────────────────────────────────────┐
      │           STAGING AREA                    │
      │  /tmp/opencode/orch/<task_id>/            │
      │  ├── w-1/  ├── w-2/  ├── w-3/  ├── w-N/  │
      └─────────────────────────────────────────┘
                         │
                         ▼
               ┌─────────────────┐
               │  RECONCILIATION  │  ← Orchestrator junta, valida, mergea
               └────────┬────────┘
                        │
                        ▼
               ┌─────────────────┐
               │   FINAL OUTPUT   │
               └─────────────────┘
```

---

## Fase 1 — PLAN

El orquestador analiza la tarea y produce un **manifest**.

### Pasos

1. **Analizar la tarea grande** y descomponerla en items atómicos
2. **Identificar dependencias** entre items (si B necesita el output de A)
3. **Asignar rangos de IDs** o recursos únicos para evitar colisiones
4. **Determinar estrategia** de distribución (paralelo total, batches, pipeline)
5. **Escribir el manifest** en `/tmp/opencode/orch/<task_id>/manifest.json`
6. **Decidir `max_concurrency`** — cuántos workers lanzar simultáneamente

### Reglas de descomposición

- Cada item debe poder procesarse **sin comunicarse con otros workers**
- Items con `deps: []` → pueden ir en paralelo
- Items con `deps: ["A01"]` → deben esperar a que A01 termine
- Si hay dependencias, se dividen en **batches secuenciales**: batch 1 (paralelo), batch 2 (paralelo), etc.

---

## Fase 2 — LAUNCH

El orquestador lanza N workers con `task` tool, todos del mismo `subagent_type`.

### Contrato de entrada para cada worker

Cada worker recibe en su prompt:

```
MANIFEST_PATH=/tmp/opencode/orch/<task_id>/manifest.json
WORKER_ID=w-1
ASSIGNED_ITEMS=["A01","A02","A03"]
STAGING_DIR=/tmp/opencode/orch/<task_id>/staging
SHARED_DIR=/tmp/opencode/orch/<task_id>/shared
```

El worker **debe**:

1. Leer `MANIFEST_PATH` para obtener contexto global (style_rules, tags, etc.)
2. Procesar cada item en `ASSIGNED_ITEMS` en orden
3. Para cada item:
   - Leer `item.prompt` y `item.output.path`
   - Producir el output
   - Escribir en `STAGING_DIR/<WORKER_ID>/<item_id>/output.<ext>`
   - Escribir metadata en `STAGING_DIR/<WORKER_ID>/<item_id>/meta.json`
4. NO escribir fuera de `STAGING_DIR/<WORKER_ID>/`
5. NO modificar el manifest
6. Devolver resumen al orquestador vía el mensaje de retorno del task

### Contrato de salida de cada worker

```json
{
  "worker_id": "w-1",
  "status": "ok" | "partial" | "failed",
  "items_total": 3,
  "items_ok": 3,
  "items_failed": 0,
  "items": [
    {
      "id": "A01",
      "status": "done",
      "output": "staging/w-1/A01/output.md",
      "meta": "staging/w-1/A01/meta.json"
    }
  ],
  "errors": []
}
```

### Código de lanzamiento (ejemplo)

```
# El orquestador hace:
1. task(subagent_type="proteo", prompt="...", con MANIFEST_PATH, WORKER_ID="w-1", ASSIGNED_ITEMS=[...])
2. task(subagent_type="proteo", prompt="...", con MANIFEST_PATH, WORKER_ID="w-2", ASSIGNED_ITEMS=[...])
3. task(subagent_type="proteo", prompt="...", con MANIFEST_PATH, WORKER_ID="w-3", ASSIGNED_ITEMS=[...])
```

---

## Fase 3 — RECONCILE

Cuando todos los workers responden, el orquestador ejecuta la reconciliación.

### Pasos

1. **Recolectar resultados** de todos los workers
2. Para cada item en el manifest:
   - Verificar que existe `staging/<worker>/<item_id>/output`
   - Validar **unicidad de IDs** (no hay MAN-XXXXX duplicados entre workers)
   - Validar **cross-references** (si aplica: wikilinks, imports, etc.)
   - Validar **consistencia de estilo** contra `shared_context.style_rules`
3. Si hay conflictos:
   - Resolver automático según `reconciliation.conflict` strategy
   - O reportar para decisión manual
4. Actualizar `manifest.state = "reconciling"`
5. Registrar resultados de validación

### Reglas de resolución de conflictos

| `conflict` strategy | Comportamiento |
|---------------------|----------------|
| `orchestrator_decides` | El orquestador elige la versión ganadora basado en reglas predefinidas |
| `report` | Marca el conflicto, lo incluye en el resumen final, no lo resuelve |
| `newer_wins` | El worker que terminó último tiene prioridad |
| `merge` | Intenta mergear contenido (solo aplicable a ciertos `output.type`) |

---

## Fase 4 — MERGE

El orquestador mueve los outputs validados a su destino final.

### Pasos

1. Para cada item reconciliado:
   - Copiar `staging/<worker>/<item_id>/output` → `item.output.path` (destino final)
   - Si `output.type` es `file` → mover el archivo
   - Si `output.type` es `data` → consolidar en un JSON único
   - Si `output.type` es `code` → mergear según estructura de proyecto
2. Actualizar manifest:
   - `items[].status = "done"`
   - `state = "completed"` (o `"completed_with_errors"`)
3. Limpiar staging area (opcional, mantener para debug)
4. Devolver resumen final estructurado

---

## Formato del Manifest

```json
{
  "task_id": "orch-unique-name-YYYYMMDD",
  "created_at": "2026-06-05T20:00:00Z",

  "orchestrator": {
    "agent": "hefesto",
    "strategy": "parallel",
    "max_concurrency": 4
  },

  "worker": {
    "type": "proteo",
    "prompt_prefix": "Eres proteo. Trabajás dentro de un plan orquestado. Lee el manifest en MANIFEST_PATH.",
    "config": {
      "model": null,
      "temperature": 0.2
    }
  },

  "items": [
    {
      "id": "A01",
      "name": "RSA documentation",
      "prompt": "Crear documentación completa de RSA...",
      "deps": [],
      "output": {
        "type": "file",
        "path": "/destino/final/01-RSA.md",
        "ext": ".md"
      },
      "status": "pending",
      "worker": null
    }
  ],

  "stage": {
    "dir": "/tmp/opencode/orch/orch-unique-name-YYYYMMDD",
    "worker_prefix": "w"
  },

  "shared_context": {
    "style_rules": "Usar frontmatter YAML con id, nombre, tags. Incluir código Python.",
    "global_tags": ["criptografia"],
    "id_range": {"start": "MAN-001601", "end": "MAN-001642"},
    "id_counter": "MAN-001601",
    "extra": {}
  },

  "reconciliation": {
    "validate_ids": true,
    "validate_refs": true,
    "conflict": "orchestrator_decides",
    "on_failure": "report_and_continue"
  },

  "state": "planning"
}
```

### Campos del Manifest

| Campo | Descripción |
|-------|-------------|
| `task_id` | Identificador único de la tarea orquestada |
| `orchestrator.agent` | Nombre del agente que orquesta |
| `orchestrator.strategy` | `parallel`, `batch`, `pipeline` |
| `orchestrator.max_concurrency` | Máximo de workers simultáneos |
| `worker.type` | `subagent_type` a invocar |
| `worker.prompt_prefix` | Texto que se antepone al prompt de cada worker para contextualizar |
| `items[].id` | Identificador único del item dentro del task |
| `items[].deps` | Array de IDs de los que depende (vacíos = paralelizables) |
| `items[].output.type` | `file`, `data`, `code`, `refactor`, `search`, `analysis` |
| `items[].output.path` | Ruta final donde va el output |
| `stage.dir` | Directorio staging (todos los workers escriben acá) |
| `shared_context` | Datos que todos los workers necesitan (style rules, tags, IDs) |
| `reconciliation` | Reglas de validación y resolución de conflictos |
| `state` | `planning`, `launched`, `reconciling`, `completed`, `failed` |

---

## Estrategias de Distribución

### `parallel` — Todos los items independientes

```
Items: A01, A02, A03, A04 (no tienen deps entre sí)
Distribución: w1=[A01,A02], w2=[A03,A04]
Lanzamiento: 2 workers simultáneos
```

### `batch` — Grupos con dependencias internas

```
Items: A01(deps:[]), A02(deps:[]), B01(deps:[A01]), B02(deps:[A02])
Batch 1: w1=[A01,A02] (paralelo)
Batch 2: w1=[B01], w2=[B02] (paralelo, después del batch 1)
```

### `pipeline` — Items estrictamente secuenciales

```
Items: A → B → C (cada uno depende del anterior)
Distribución: Un solo worker procesa en serie
O: Worker 1 hace A, Worker 2 lee output de A y hace B, etc.
```

---

## Manejo de Fallos

| Situación | Respuesta |
|-----------|-----------|
| Worker timeout (no responde) | Registrar como `failed`. Si `on_failure: retry`, re-lanzar. |
| Worker reporta error parcial | Aceptar items que sí funcionaron, reportar fallas. |
| Worker escribe en ubicación incorrecta | Rechazar output, marcar item como `failed`. |
| ID duplicado entre workers | Reasignar IDs según `reconciliation.conflict` strategy. |
| Cross-reference rota (wikilink a inexistente) | Registrar advertencia, no bloquear (depende del contexto). |
| Style guide no seguida | Registrar como advertencia, no bloquear. |
| Todos los workers fallan | `state = "failed"`, reportar diagnóstico completo. |

### Campos de `reconciliation.on_failure`

| Valor | Comportamiento |
|-------|----------------|
| `report_and_continue` | Reporta el error pero continúa con el resto |
| `abort_on_any` | Cancela toda la orquestación si un item falla |
| `retry_once` | Re-lanza el worker fallido una vez más |
| `retry_reassign` | Re-asigna items fallidos a otro worker |

---

## Validación y Coherencia

### Validación automática post-recolección

```python
# Pseudo-código del orquestador en la fase de reconciliación
def validate(manifest, staging_dir):
    errors = []
    warnings = []

    # 1. IDs: secuenciales, sin duplicados, dentro del rango
    all_ids = [item.id for item in manifest.items]
    if len(all_ids) != len(set(all_ids)):
        errors.append("Duplicate IDs found")
    # validar rango...

    # 2. Archivos: todos los outputs existen
    for item in manifest.items:
        worker_dir = f"{staging_dir}/{item.worker}/{item.id}"
        if not exists(f"{worker_dir}/output.{item.output.ext}"):
            errors.append(f"Missing output for {item.id}")

    # 3. Cross-references (si aplica)
    if manifest.reconciliation.validate_refs:
        for output in outputs:
            refs = extract_references(output)
            for ref in refs:
                if not resolve(ref, all_known_paths):
                    warnings.append(f"Broken ref: {ref} in {item.id}")

    # 4. Estilo (si hay style_rules)
    if manifest.shared_context.style_rules:
        for output in outputs:
            if not matches_style(output, manifest.shared_context.style_rules):
                warnings.append(f"Style mismatch in {item.id}")

    return errors, warnings
```

---

## Ejemplos de Uso

### Ejemplo 1: Documentación paralela con proteo

```json
// manifest.json
{
  "task_id": "orch-crypto-20260605",
  "orchestrator": { "agent": "hefesto", "strategy": "parallel", "max_concurrency": 3 },
  "worker": { "type": "proteo" },
  "items": [
    { "id": "A01", "name": "RSA", "prompt": "Crear nota RSA...", "deps": [], "output": {"type":"file","path":"02-CRIPTOGRAFIA/03-ASIMETRICA/01-RSA.md"} },
    { "id": "A02", "name": "ECC", "prompt": "Crear nota ECC...", "deps": [], "output": {"type":"file","path":"02-CRIPTOGRAFIA/03-ASIMETRICA/02-ECC.md"} },
    { "id": "A03", "name": "TLS", "prompt": "Crear nota TLS...", "deps": [], "output": {"type":"file","path":"02-CRIPTOGRAFIA/05-PROTOCOLOS/01-TLS.md"} }
  ],
  "stage": { "dir": "/tmp/opencode/orch/orch-crypto-20260605" },
  "shared_context": { "style_rules": "Incluir frontmatter, ejemplos Python, y wikilinks.", "id_range": {"start":"MAN-001601","end":"MAN-001642"} },
  "reconciliation": { "validate_ids": true, "validate_refs": true, "conflict": "orchestrator_decides", "on_failure": "report_and_continue" },
  "state": "planning"
}
```

### Ejemplo 2: Análisis de logs con apolo

```json
{
  "task_id": "orch-loganalysis-20260605",
  "worker": { "type": "apolo" },
  "items": [
    { "id": "L01", "name": "auth.log", "prompt": "Analizar /var/log/auth.log en busca de bruteforce...", "deps": [], "output": {"type":"data","path":"/tmp/analysis/auth_results.json"} },
    { "id": "L02", "name": "syslog", "prompt": "Analizar /var/log/syslog en busca de anomalías...", "deps": [], "output": {"type":"data","path":"/tmp/analysis/syslog_results.json"} }
  ],
  "reconciliation": {
    "validate_ids": false,
    "conflict": "orchestrator_decides",
    "on_failure": "report_and_continue"
  },
  "shared_context": {
    "extra": { "time_window": "2026-06-01 to 2026-06-05", "min_severity": "WARN" }
  }
}
```

### Ejemplo 3: Análisis de malware con hecate

```json
{
  "task_id": "orch-malware-20260605",
  "worker": { "type": "hecate" },
  "items": [
    { "id": "M01", "name": "sample1.exe", "prompt": "Analizar sample1.exe...", "deps": [], "output": {"type":"data","path":"/tmp/analysis/sample1.json"} },
    { "id": "M02", "name": "sample2.exe", "prompt": "Analizar sample2.exe...", "deps": [], "output": {"type":"data","path":"/tmp/analysis/sample2.json"} }
  ],
  "shared_context": {
    "extra": { "yara_rules_path": "$HOME/yara/rules/", "sandbox": "docker" }
  }
}
```

---

## Integración con Agentes Existentes

Cualquier agente primario puede cargar este skill y actuar como orquestador.

### Carga del skill

```
skill(name="orchestrator-manager")
```

### Lo que cada agente obtiene al cargarlo

| Agente | ¿Puede ser orquestador? | ¿Puede ser worker? | ¿Qué tipo de tareas puede orquestar? |
|--------|------------------------|---------------------|--------------------------------------|
| `hefesto` | ✅ | ❌ | Creación de agentes, skills, documentación |
| `atlas` | ✅ | ❌ | Mantenimiento del sistema en múltiples equipos |
| `hestia` | ✅ | ❌ | Mantenimiento de Windows en varios equipos |
| `atenea` | ✅ | ❌ | Análisis forense, CSIRT, threat hunting |
| `ares` | ✅ | ❌ | Pentesting en múltiples targets |
| `prometeo` | ✅ | ❌ | Generación de código, refactors |
| `proteo` | ❌ | ✅ | Creación de documentación criptográfica |
| `hecate` | ❌ | ✅ | Análisis de muestras de malware |
| `apolo` | ❌ | ✅ | Análisis de logs |
| `hermes` | ❌ | ✅ | Análisis de PCAPs |
| `argos` | ❌ | ✅ | OSINT |
| `temis` | ❌ | ✅ | Auditoría y compliance |

### Flujo de integración

```
1. Agente primario detecta tarea grande → carga orchestrator-manager
2. Sigue el protocolo: PLAN → LAUNCH → RECONCILE → MERGE
3. Invoca workers del tipo adecuado
4. Los workers no necesitan saber del orchestrator-manager
   — solo reciben un prompt con los parámetros de entrada
```

---

## Templates

Los templates están en el directorio `templates/` junto a este SKILL.md.

| Template | Archivo | Uso |
|----------|---------|-----|
| Manifest | `templates/manifest.json` | Template base del manifest |
| Worker prompt | `templates/worker-prompt.md` | Template de prompt para workers |

### Template Manifest

```json
{
  "task_id": "orch-<task-name>-<YYYYMMDD>",
  "created_at": "<ISO_TIMESTAMP>",
  "orchestrator": {
    "agent": "<agent-name>",
    "strategy": "parallel",
    "max_concurrency": 3
  },
  "worker": {
    "type": "<subagent-type>",
    "prompt_prefix": "Eres <worker-type>. Trabajás dentro de un plan orquestado.",
    "config": {}
  },
  "items": [
    {
      "id": "<ITEM_ID>",
      "name": "<Human-readable name>",
      "prompt": "<Detailed instructions for this specific item>",
      "deps": [],
      "output": {
        "type": "file|data|code|analysis|search",
        "path": "<final/output/path>",
        "ext": "<extension>"
      },
      "status": "pending",
      "worker": null
    }
  ],
  "stage": {
    "dir": "/tmp/opencode/orch/<task_id>",
    "worker_prefix": "w"
  },
  "shared_context": {
    "style_rules": "<Style guide for consistency>",
    "global_tags": [],
    "id_range": null,
    "id_counter": null,
    "extra": {}
  },
  "reconciliation": {
    "validate_ids": true,
    "validate_refs": false,
    "conflict": "orchestrator_decides",
    "on_failure": "report_and_continue"
  },
  "state": "planning"
}
```

### Template Worker Prompt

```
# Worker Orquestado

Sos {worker_type}. Trabajás dentro de un plan de orquestación.

## Contexto Global
- Manifest: {MANIFEST_PATH}
- Worker ID: {WORKER_ID}
- Staging: {STAGING_DIR}/{WORKER_ID}/

## Instrucciones
1. Leé el manifest en {MANIFEST_PATH} para contexto global
2. Procesá CADA UNO de estos items (son tuyos, nadie más los toca):
   {ASSIGNED_ITEMS}

## Reglas
- NO escribas fuera de {STAGING_DIR}/{WORKER_ID}/
- NO modifiques el manifest
- Para cada item, escribí:
  - {STAGING_DIR}/{WORKER_ID}/<item_id>/output.<ext>
  - {STAGING_DIR}/{WORKER_ID}/<item_id>/meta.json
- Devolvé un resumen JSON al final con: items procesados, errores, archivos creados

## Items Asignados
(por cada item: su prompt específico, su output path, etc.)
```

---

## Notas Importantes

- **El manifest es el contrato**: todos los workers lo leen, solo el orquestador lo escribe
- **Staging por worker**: cada worker tiene su propio subdirectorio, no hay colisiones
- **Validación post-hoc**: la coherencia se verifica después, no durante la ejecución
- **Workers no necesitan el skill**: solo reciben un prompt bien estructurado
- **El orquestador puede ser cualquier agente primario** que cargue este skill
- **Siempre limpiar staging** después del merge exitoso (o al menos documentar dónde queda)
