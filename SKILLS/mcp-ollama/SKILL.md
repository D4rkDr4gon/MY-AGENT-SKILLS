---
name: mcp-ollama
description: Use when the user has the Ollama MCP server installed and wants to call local AI models from opencode agents. Covers tools: ollama_generate, ollama_chat, ollama_list_models, ollama_ps, ollama_embed, ollama_pull.
---

# mcp-ollama

Este skill documenta el servidor MCP que conecta opencode con modelos
locales de Ollama. Permite ejecutar inferencia **sin consumir tokens de
opencode Zen**, usando modelos que corren en tu propia máquina.

## Arquitectura

```
┌─────────────┐   MCP (stdio)    ┌──────────────────┐   HTTP REST   ┌─────────┐
│  opencode   │ ◄──────────────► │ ollama-mcp-server │ ◄───────────► │ Ollama  │
│  (agentes)  │   JSON-RPC +     │  server.py        │  localhost:   │  daemon │
│             │   Content-Length │                   │   11434       │         │
└─────────────┘                  └──────────────────┘               └─────────┘
```

## Herramientas disponibles

Todas las tools están disponibles para cualquier agente de opencode que
tenga permisos para usar MCP. No requieren configuración adicional.

### ollama_generate

Generación directa prompt → texto. Ideal para tareas que no necesitan
mantener historial de conversación.

**Parámetros clave:**
- `model` (string, default: `gemma3:270m`) — qué modelo usar
- `prompt` (string, **requerido**) — la instrucción
- `system` (string, opcional) — system prompt para contexto
- `temperature` (float, default: `0.7`) — creatividad
- `num_predict` (int, default: `1024`) — tokens máximos

**Cuándo usarla:**
- Resumir texto, logs, o documentos
- Clasificar o etiquetar contenido
- Traducir entre idiomas
- Preguntas/respuestas simples
- Extraer IOCs de texto

### ollama_chat

Chat multi-turno con historial completo de mensajes. Soportados roles:
`system`, `user`, `assistant`.

**Parámetros clave:**
- `model` (string, default: `gemma3:270m`)
- `messages` (array, **requerido**) — `[{"role": "user", "content": "..."}]`
- `temperature` (float, default: `0.7`)

**Cuándo usarla:**
- Conversaciones que requieren contexto de vueltas anteriores
- Refinamiento iterativo de respuestas
- Cuando necesitás que el modelo "recuerde" lo dicho antes

### ollama_list_models

Lista todos los modelos descargados localmente. Sin parámetros.

**Cuándo usarla:**
- Para verificar qué modelos están disponibles
- Para decidir qué modelo usar en una generación

### ollama_ps

Muestra qué modelos están actualmente cargados en memoria.

### ollama_embed

Genera embeddings (vectores) para un texto dado.

**Cuándo usarla:**
- Alimentar un pipeline RAG
- Búsqueda semántica
- Clustering de documentos

### ollama_pull

Descarga un modelo nuevo desde la librería de Ollama.

**Cuándo usarla:**
- Cuando necesitás un modelo que no está instalado todavía

## Modelos recomendados

| Modelo | Params | RAM | Uso recomendado |
|--------|--------|-----|-----------------|
| `gemma3:270m` | 270M | 2 GB+ | Rápido, testing, tareas triviales |
| `whiterabbit-neo:13b` | 13B | 16 GB+ | Razonamiento profundo, análisis complejo |

Para más modelos, ver el skill `ollama-manager`.

## Cómo usarlas desde un agente

Las tools MCP se invocan igual que cualquier otra herramienta de opencode.
Simplemente decile al agente qué tool usar:

> "Usá ollama_generate con whiterabbit-neo:13b para analizar este log"

O si estás escribiendo el prompt de un subagente:

```markdown
Tienes acceso a herramientas locales via MCP. Cuando recibas una consulta,
usá `ollama_generate` con el modelo apropiado según la complejidad:
- Tareas simples → gemma3:270m (rápido)
- Análisis profundos → whiterabbit-neo:13b
```

## Integración con subagentes

Los subagentes `local-quick` y `local-reason` son wrappers pre-configurados
que usan el MCP server automáticamente:

- `@local-quick` → gemma3:270m (tareas rápidas, temperatura baja)
- `@local-reason` → whiterabbit-neo:13b (razonamiento, temperatura media)

Invocarlos desde cualquier agente primario:

```
@local-quick Resumí este texto en 3 líneas
@local-reason Analizá este código en busca de vulnerabilidades
```

## Verificación de estado

```bash
# 1. Verificar que Ollama corre
curl http://localhost:11434/api/tags | python3 -m json.tool

# 2. Verificar que el MCP server responde
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' |
  python3 ~/MY-AGENT-SKILLS/MCP/ollama-server/server.py
```

## Notas importantes

- El servidor debe estar registrado en `opencode.jsonc` bajo `mcp.ollama`
- Ollama debe estar corriendo (`systemctl start ollama` o `ollama serve`)
- Los modelos locales son **más lentos** que opencode Zen en GPU
- No consumen tokens facturables
- gemma3:270m responde en milisegundos en CPU moderna
- whiterabbit-neo:13b puede tomar 30-60s por respuesta en CPU
