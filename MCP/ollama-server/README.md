# ollama-mcp-server

MCP (Model Context Protocol) server que expone modelos locales de
[Ollama](https://ollama.ai) como herramientas para agentes de opencode.

## Herramientas expuestas

| Tool | Descripción | Modelo por defecto |
|------|-------------|-------------------|
| `ollama_generate` | Generación simple prompt→texto | gemma3:270m |
| `ollama_chat` | Chat multi-turno con historial | gemma3:270m |
| `ollama_list_models` | Lista modelos descargados | — |
| `ollama_ps` | Muestra modelos en memoria | — |
| `ollama_embed` | Genera embeddings de texto | gemma3:270m |
| `ollama_pull` | Descarga un modelo nuevo | — |

## Requisitos

- Python 3.10+
- `requests` (instalado en el sistema)
- Ollama corriendo (`ollama serve` o `systemctl start ollama`)

## Instalación

1. Clonar/actualizar `MY-AGENT-SKILLS`:

   ```bash
   cd ~/MY-AGENT-SKILLS && git pull
   ```

2. (Opcional) Instalar dependencias si faltan:

   ```bash
   pip install -r MCP/ollama-server/requirements.txt
   ```

3. Agregar a `~/.config/opencode/opencode.jsonc`:

   ```jsonc
   "mcp": {
     "ollama": {
       "type": "local",
       "command": [
         "python3",
         "/home/lcampassi/MY-AGENT-SKILLS/MCP/ollama-server/server.py"
       ],
       "enabled": true
     }
   }
   ```

4. **Reiniciar opencode**.

## Uso desde opencode

Una vez registrado, cualquier agente puede invocar las herramientas
directamente. Por ejemplo:

> Usá `ollama_generate` con el modelo `whiterabbit-neo:13b` para analizar
> este log en profundidad.

O desde un subagente configurado para usar el MCP server automáticamente
(ver skill `mcp-ollama` y agentes `local-quick` / `local-reason`).

## Solución de problemas

| Síntoma | Causa | Solución |
|---------|-------|----------|
| `Cannot connect to Ollama` | Ollama no está corriendo | `ollama serve` |
| Tool timeout | Modelo muy pesado para CPU | Usar gemma3:270m o esperar |
| MCP no aparece | Error en opencode.jsonc | Revisar sintaxis, reiniciar |

## Mantenimiento

El server se inicia y detiene automáticamente con opencode.
No requiere supervisión.
