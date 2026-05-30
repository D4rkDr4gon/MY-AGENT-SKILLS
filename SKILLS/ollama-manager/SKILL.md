---
name: ollama-manager
description: Use when the user asks about managing their local AI models via Ollama, running models, configuring GPU acceleration, integrating with opencode, the Ollama REST API, or troubleshooting model performance.
---

# ollama-manager

## Contexto del Sistema

**Version**: 0.24.0
**Servicio**: `ollama.service` (systemd, sistema)
**GPU**: AMD Radeon Graphics (Barcelo) — sin ROCm (CPU-only por ahora)
**Storage**: `~/.ollama/models/` (blobs + manifests)
**Espacio usado**: ~8.9 GB
**REST API**: `http://localhost:11434`

### Modelos instalados

| Modelo | Parametros | Tamano | Uso |
|--------|-----------|--------|-----|
| `gemma3:270m` | 270M | 291 MB | Rapido, testing, launchgemma |
| `jimscard/whiterabbit-neo:13b` | 13B | 9.2 GB | Razonamiento, tareas complejas |

### Scripts del dotfiles

| Script | Ruta | Funcion |
|--------|------|---------|
| `install-ollama.sh` | `~/dotfiles/automat/install/install-ollama.sh` | Instalacion + servicio |
| `ollama-pull.sh` | `~/dotfiles/automat/install/ollama-pull.sh` | Descarga modelos (llama3.2, codellama, mistral, neural-chat, qwen:7b) |
| `launchgemma.sh` | `~/dotfiles/automat/launchgemma.sh` | Inicia ollama + gemma3 en Kitty |
| `ollama-status` | `~/.local/bin/ollama-status` | Estado del servicio + modelos |

---

## Comandos basicos

```bash
# Iniciar servidor
ollama serve

# Ver estado
systemctl status ollama
~/.local/bin/ollama-status

# Iniciar/detener servicio
sudo systemctl start ollama
sudo systemctl stop ollama
sudo systemctl enable ollama
sudo systemctl disable ollama

# Listar modelos descargados
ollama list

# Ver modelos en ejecucion
ollama ps

# Informacion de un modelo
ollama show <modelo>
```

---

## Gestion de modelos

### Descargar modelos

```bash
# Un modelo
ollama pull llama3.2

# Varios (script incluido)
bash ~/dotfiles/automat/install/ollama-pull.sh

# Modelos recomendados por categoria
```

### Eliminar modelos

```bash
ollama rm <modelo>
ollama rm gemma3:270m   # ej: borrar gemma chico
```

### Ejecutar modelos

```bash
# Interactivo (chat en terminal)
ollama run gemma3:270m

# Una sola consulta
ollama run gemma3:270m "Explica que es una API REST"

# Con template de sistema
ollama run gemma3:270m --system "Sos un experto en Linux. Respondé en español."
```

---

## REST API

Ollama expone una API HTTP en `http://localhost:11434`.

### Endpoints principales

#### `POST /api/generate` — Generar texto

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "gemma3:270m",
  "prompt": "Por que el cielo es azul?",
  "stream": false
}'
```

#### `POST /api/chat` — Chat con historial

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "gemma3:270m",
  "messages": [
    {"role": "system", "content": "Sos un asistente experto en Linux."},
    {"role": "user", "content": "Que es systemd?"}
  ],
  "stream": false
}'
```

#### `POST /api/embed` — Embeddings

```bash
curl http://localhost:11434/api/embed -d '{
  "model": "gemma3:270m",
  "input": "El cielo es azul por la dispersion de Rayleigh"
}'
```

#### `GET /api/tags` — Modelos disponibles

```bash
curl http://localhost:11434/api/tags | jq .
```

#### `POST /api/pull` — Descargar modelo

```bash
curl http://localhost:11434/api/pull -d '{"name": "llama3.2"}'
```

### Parametros comunes de generacion

| Parametro | Tipo | Defecto | Descripcion |
|-----------|------|---------|-------------|
| `temperature` | float | 0.8 | Creatividad (0 = deterministico, 2 = muy creativo) |
| `top_p` | float | 0.9 | Nucleus sampling |
| `top_k` | int | 40 | Top-K sampling |
| `num_predict` | int | 128 | Max tokens a generar |
| `stop` | string[] | [] | Secuencias para detener generacion |
| `repeat_penalty` | float | 1.1 | Penalizar repeticion |

---

## Integracion con Python

### Instalar libreria

```bash
pip install ollama
```

### Uso basico

```python
import ollama

# Chat simple
response = ollama.chat(model="gemma3:270m", messages=[
    {"role": "user", "content": "Hola! Que tal?"},
])
print(response["message"]["content"])

# Streaming
stream = ollama.chat(model="gemma3:270m", messages=[
    {"role": "user", "content": "Contame algo interesante"},
], stream=True)
for chunk in stream:
    print(chunk["message"]["content"], end="", flush=True)

# Con contexto / system prompt
response = ollama.chat(model="whiterabbit-neo:13b", messages=[
    {"role": "system", "content": "Sos un asistente util. Respondé en español."},
    {"role": "user", "content": "Explica la diferencia entre TCP y UDP"},
])
print(response["message"]["content"])

# Embeddings
response = ollama.embed(model="gemma3:270m", input="Texto a vectorizar")
print(response["embeddings"])
```

### Integracion con Skills / contexto

```python
import ollama

# Cargar contenido de una skill como contexto
with open("$HOME/MY-AGENT-SKILLS/obsidian-manager/SKILL.md") as f:
    skill_context = f.read()

response = ollama.chat(model="whiterabbit-neo:13b", messages=[
    {"role": "system", "content": f"Usa este contexto para responder:\n\n{skill_context}"},
    {"role": "user", "content": "Cuales son las templates disponibles?"},
])
```

---

## Integracion con opencode

### 1. Configurar proveedor Ollama en opencode

Editar `~/.config/opencode/opencode.jsonc`:

```jsonc
{
  "provider": "ollama",
  "model": "whiterabbit-neo:13b",
  "skills": {
    "paths": ["$HOME/MY-AGENT-SKILLS"]
  }
}
```

### 2. Usar skills locales como contexto

Para que opencode cargue una skill al interactuar con Ollama:

```jsonc
{
  "provider": "ollama",
  "model": "whiterabbit-neo:13b",
  "systemPrompt": "Sos un asistente experto en gestion de sistemas. Usa las skills disponibles para contexto adicional.",
  "skills": {
    "paths": ["$HOME/MY-AGENT-SKILLS"]
  }
}
```

### 3. Probar conexion

```bash
# Verificar que el API responde
curl http://localhost:11434/api/tags

# Probar modelo
curl http://localhost:11434/api/generate -d '{
  "model": "whiterabbit-neo:13b",
  "prompt": "Hola, decis hola?",
  "stream": false
}' | jq .response
```

---

## GPU Acceleration (ROCm para AMD)

### Instalar soporte ROCm

```bash
# Paquetes necesarios para AMD ROCm
sudo pacman -S rocm-hip-sdk rocm-opencl-sdk rocm-llvm

# Agregar usuario al grupo render
sudo usermod -aG render $USER

# Verificar GPU detectada
rocm-smi
```

### Configurar Ollama para GPU

```bash
# Forzar uso de ROCm
export HSA_OVERRIDE_GFX_VERSION=10.3.0
export HIP_VISIBLE_DEVICES=0

# O configurar en el servicio
sudo systemctl edit ollama
```

Agregar en `[Service]`:
```
Environment="HSA_OVERRIDE_GFX_VERSION=10.3.0"
Environment="HIP_VISIBLE_DEVICES=0"
```

> **Nota**: Barcelo (gfx1030) tiene soporte ROCm experimental. Sin ROCm, los modelos corren en CPU.

### Verificar aceleracion

```bash
# Ollama muestra GPU en los logs cuando usa ROCm
journalctl -u ollama --no-pager | grep -i "gpu\|rocm\|hip"

# O consultar la API
curl http://localhost:11434/api/generate -d '{
  "model": "gemma3:270m",
  "prompt": "test",
  "options": {"num_gpu": 1}
}'
```

---

## Flujos de trabajo comunes

### 1. Iniciar sesion interactiva

```bash
# Iniciar servidor si no corre
ollama serve > /dev/null 2>&1 &
sleep 2

# Chat interactivo
ollama run whiterabbit-neo:13b
```

### 2. Usar launchgemma (acceso rapido)

```bash
# Abre Kitty con Gemma 3 directamente
bash ~/dotfiles/automat/launchgemma.sh
```

### 3. Script para query rapida

```python
#!/usr/bin/env python3
"""query.py: Consulta rapida a Ollama desde terminal."""
import sys, ollama

model = sys.argv[1] if len(sys.argv) > 1 else "gemma3:270m"
prompt = sys.argv[2] if len(sys.argv) > 2 else sys.stdin.read().strip()

response = ollama.chat(model=model, messages=[
    {"role": "user", "content": prompt}
], stream=True)

for chunk in response:
    print(chunk["message"]["content"], end="", flush=True)
print()
```

Uso:
```bash
python3 query.py gemma3:270m "Explica que es un firewall"
echo "Que es Docker?" | python3 query.py whiterabbit-neo:13b
```

### 4. Pasar contexto desde archivo

```bash
cat contexto.md | python3 -c "
import sys, ollama
context = sys.stdin.read()
prompt = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else 'Resumi este texto'
response = ollama.chat(model='whiterabbit-neo:13b', messages=[
    {'role': 'system', 'content': f'Contexto:\n{context}'},
    {'role': 'user', 'content': prompt}
], stream=True)
for chunk in response:
    print(chunk['message']['content'], end='', flush=True)
print()
" "Hace un resumen de este documento"
```

### 5. Evaluar modelos: comparar respuestas

```bash
for model in gemma3:270m whiterabbit-neo:13b; do
    echo "=== $model ==="
    curl -s http://localhost:11434/api/generate -d "{
        \"model\": \"$model\",
        \"prompt\": \"Explica que es la memoria virtual en 3 parrafos\",
        \"stream\": false
    }" | jq -r '.response'
    echo
done
```

---

## Troubleshooting

| Problema | Solucion |
|----------|----------|
| `could not connect to ollama server` | `ollama serve` o `sudo systemctl start ollama` |
| Modelo lento en CPU | Usar modelos < 3B (gemma3:270m, phi3:mini, qwen:0.5b) |
| `out of memory` | Usar modelo mas chico o cerrar apps pesadas |
| GPU no detectada | Verificar ROCm + grupo `render` |
| `context deadline exceeded` | Modelo muy grande para el hardware |
| Puerto 11434 ocupado | `ollama serve --port 11435` |

### Logs

```bash
# Servicio systemd
journalctl -u ollama -f

# Servicio manual (verbose)
ollama serve 2>&1
```

---

## Modelos recomendados por uso

| Categoria | Modelo | Tamano | RAM recomendada |
|-----------|--------|--------|-----------------|
| Rapido / testing | `gemma3:270m` | 291 MB | 2 GB+ |
| Rapido / general | `llama3.2:1b` | ~1 GB | 4 GB+ |
| General / coding | `llama3.2:3b` | ~2 GB | 4 GB+ |
| Coding | `codellama:7b` | ~4 GB | 8 GB+ |
| General / chat | `mistral:7b` | ~4 GB | 8 GB+ |
| Chat en espanol | `qwen:7b` | ~4 GB | 8 GB+ |
| Razonamiento | `whiterabbit-neo:13b` | 9.2 GB | 16 GB+ |
| Instrucciones | `neural-chat:7b` | ~4 GB | 8 GB+ |

---

## Notas importantes

- `~/.ollama/history` guarda el historial de conversaciones de `ollama run`
- El servidor debe estar **corriendo** para cualquier operacion excepto `ollama serve` y `ollama pull`
- Los modelos se almacenan en `~/.ollama/models/blobs/` como archivos sha256
- Para liberar espacio: `ollama rm <modelo>` y limpiar blobs huerfanos con `ollama prune`
- `ollama run` sin `--system` no tiene system prompt por defecto
- La API streaming (`stream: true`) es mas rapida para respuestas largas
- Se puede usar `num_ctx: 4096` o `num_ctx: 8192` para contexto mas largo (consume mas RAM)
