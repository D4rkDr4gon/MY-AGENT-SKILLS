---
name: health-check-manager
description: >
  Skill para gestionar Health Checks de infraestructura IDM/NAM.
  Proporciona catálogo de servicios, flujo interactivo y generación de template HTML
  para ticketera. El agente dedalo la carga para guiar al usuario.
---

# health-check-manager ⚕️

Skill de apoyo para el agente **dedalo**. Define el catálogo de servicios, el flujo de preguntas y el formato de salida HTML para armar Health Checks de IDM/NAM.

---

## 🎯 Propósito

Permitir a `dedalo` construir templates de Health Check de forma interactiva:
- Preguntar estado de cada servicio (uno a uno, sin asumir)
- Generar HTML listo para copiar a la ticketera
- Buscar procedimientos en `$BABILONIA`/`internet` ante errores

---

## 📋 Catálogo de Servicios (Referencia Interna)

### IDM_BASE (siempre, orden fijo)
| # | Servicio | Referencia de verificación |
|---|----------|---------------------------|
| 1 | Sincronización horaria de eDirectory | `ndsrepair -T` |
| 2 | Sincronización de réplicas de eDirectory | `ndsrepair -E` |
| 3 | Funcionamiento de Conectores | iManager > Identity Manager Overview > Dashboard (eventos encolados) |
| 4 | Funcionamiento de iManager | Login en todas las instancias |
| 5 | Funcionamiento de SSPR | URL + login + certificado web |
| 6 | Funcionamiento de Identity Application | Portal IDM + formularios + certificado |
| 7 | Workflows finalizados con error | iManager > Workflow > Filtro días > View Comments |

### NAM_OPCIONAL (si usuario confirma)
| # | Servicio | Verificación |
|---|----------|-------------|
| 8 | Access Manager – Administration Console | Levantada y responde |
| 9 | Access Manager – Identity Server | Responde |
| 10 | Access Manager – Access Gateway | Responde + proxies sin errores |
| 11 | Access Manager – Analytics | Funcionando |

### HIFLOW_OPCIONAL (si usuario confirma)
| # | Servicio | Verificación |
|---|----------|-------------|
| 12 | Sincronización HiFlow (HFi) | Jobs corriendo + sin errores de sincronización |

### PERSONALIZADOS
- Definidos por el usuario al inicio, se agregan al final.

---

## 🔄 Flujo de Trabajo (para que dedalo ejecute)

### 1. CONFIGURACIÓN INICIAL
Preguntar secuencialmente:
- "Cliente / Identificador para el título:"
- "Ticket ID (opcional):"
- "Fecha (DD/MM/YYYY) [hoy]:"
- "¿Incluye componentes NAM? (sí/no):"
- "¿Incluye HiFlow (HFi)? (sí/no):"
- "¿Servicios extra personalizados? (uno por línea, vacío para terminar)"

Construir título: `HC - <Cliente> <DD/MM/YYYY>`

### 2. RECORRIDO DE SERVICIOS
Para cada servicio del catálogo correspondiente (IDM_BASE + NAM_OPCIONAL + HIFLOW_OPCIONAL + PERSONALIZADOS):

```
MOSTRAR: "🔍 [Servicio] — Verificación: [Referencia]"
PREGUNTAR: "¿Estado? [OK / ERROR / NO APLICA / SALTAR]"

SI "ERROR":
  PREGUNTAR: "Detalle breve del error:"
  PREGUNTAR: "¿Buscar procedimiento en $BABILONIA/internet? (sí/no):"
  SI SÍ:
    USAR skill obsidian-manager → buscar en $BABILONIA/WORK/** y $BABILONIA/Manuales/**
    Términos: [servicio] + "health check" + "procedimiento" + "resolución"
    SI SIN RESULTADOS: webfetch "NetIQ IDM health check [servicio] procedimiento resolución"
    MOSTRAR resumen + link
```

Registrar: servicio, estado, detalle (si ERROR), link (si buscó).

### 3. GENERAR HTML
Formato exacto (una línea por servicio, línea en blanco entre cada uno):

```
LÍNEA 1: HC - <Cliente> <DD/MM/YYYY>
LÍNEA 2: (vacía)
PARA CADA SERVICIO REGISTRADO:
  OK:      <span style="color: green; font-weight: bold;">[OK]</span> <Servicio>
  ERROR:   <span style="color: red; font-weight: bold;">[ERROR]</span> <Servicio> - <Detalle>
  N/A:     <span style="color: gray; font-style: italic;">[N/A]</span> <Servicio>
  SALTAR:  (omitir)
  LÍNEA VACÍA tras cada servicio
NOTAS EXTRA: <em><Texto></em> + línea vacía
```

### 4. SALIDA
- Mostrar HTML en consola (bloque de código para copiar)
- Preguntar: "¿Regenerar? / ¿Agregar nota? / ¿Salir?"

---

## 🎨 Ejemplo de Salida HTML (Referencia)

```
HC - CLIENTE 29/06/2026

<span style="color: green; font-weight: bold;">[OK]</span> Sincronización horaria de eDirectory

<span style="color: green; font-weight: bold;">[OK]</span> Sincronización de réplicas de eDirectory

<span style="color: red; font-weight: bold;">[ERROR]</span> Funcionamiento de Conectores - Driver con eventos encolados

<span style="color: green; font-weight: bold;">[OK]</span> Funcionamiento de iManager

<em><Foto de Jobs de HiFlow></em>
```

---

## 🔍 Búsqueda de Conocimiento (Ante ERROR)

**Orden de prioridad:**
1. **$BABILONIA** vía `obsidian-manager` (skill)
   - Zonas: `$BABILONIA/WORK/**`, `$BABILONIA/Manuales/**`
   - Estrategia: `rg` o REST API search
2. **Internet** vía `webfetch`
   - Query: `"NetIQ IDM" "health check" "<servicio>" procedimiento resolución`
   - Sitios: microfocus.com, netiq.com, documentación oficial

---

## ⚙️ Variables de Entorno (Sin Hardcodeo)

| Variable | Uso |
|----------|-----|
| `$BABILONIA` | Raíz del vault (para `obsidian-manager`) |

---

## 📌 Reglas Clave para dedalo

1. **NUNCA ASUMIR ESTADOS** — Preguntar uno a uno, esperar respuesta explícita
2. **GENÉRICO TOTAL** — Cero referencias a clientes reales, tickets, rutas absolutas
3. **SOLO SALIDA CONSOLA** — No escribir archivos salvo que usuario pida guardar (entonces usar `obsidian-manager`)
4. **ORDEN FIJO** — IDM_BASE → NAM_OPCIONAL → HIFLOW_OPCIONAL → PERSONALIZADOS
5. **HTML EXACTO** — Una línea/servicio, línea en blanco entre servicios, colores en tags, `<em>` para notas
6. **CARGA BAJO DEMANDA** — `obsidian-manager` solo si usuario pide buscar en vault; `webfetch` solo si no hay resultados en vault

---