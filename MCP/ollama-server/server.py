#!/usr/bin/env python3
"""
ollama-mcp-server — MCP (Model Context Protocol) server that exposes local
Ollama models as tools for opencode agents.

Architecture
────────────
- Communicates via stdio using MCP's JSON-RPC + Content-Length framing.
- Forwards tool invocations to Ollama's REST API (http://localhost:11434).
- No external dependencies beyond `requests` (already installed system-wide).

Tools exposed
─────────────
  ollama_generate   — Simple prompt → text  (gemma3:270m by default)
  ollama_chat       — Multi-turn chat with message history
  ollama_list_models— List downloaded models
  ollama_ps         — Show currently loaded models
  ollama_embed      — Generate text embeddings
  ollama_pull       — Download a model from the library

Usage
─────
  Register in opencode.jsonc:

    "mcp": {
      "ollama": {
        "type": "local",
        "command": ["python3", "/path/to/MCP/ollama-server/server.py"],
        "enabled": true
      }
    }

  The server starts when opencode launches and is ready to serve tool calls.
"""

from __future__ import annotations

import json
import sys
import traceback
from typing import Any

import requests

# ── Constants ────────────────────────────────────────────────────────────────
OLLAMA_BASE = "http://localhost:11434"
PROTOCOL_VERSION = "2024-11-05"
SERVER_NAME = "ollama-mcp-server"
SERVER_VERSION = "1.1.0"

TIMEOUT_GENERATE = 120  # seconds — model inference can be slow on CPU
TIMEOUT_PULL = 300      # model download
TIMEOUT_DEFAULT = 30

# ── MCP Transport (Content-Length framing over stdio) ────────────────────────


def read_message() -> dict[str, Any] | None:
    """Read one JSON-RPC message from stdin (Content-Length framing).

    Returns the parsed JSON object, or *None* on EOF.
    """
    raw_headers: list[bytes] = []
    while True:
        line = sys.stdin.buffer.readline()
        if not line:  # EOF
            return None
        if line in (b"\r\n", b"\n", b"\r"):
            break
        raw_headers.append(line)

    headers: dict[str, str] = {}
    for raw in raw_headers:
        decoded = raw.decode("utf-8", errors="replace").strip()
        if ":" in decoded:
            key, value = decoded.split(":", 1)
            headers[key.strip().lower()] = value.strip()

    content_length = int(headers.get("content-length", "0"))
    if content_length == 0:
        return None

    body_bytes = sys.stdin.buffer.read(content_length)
    body = body_bytes.decode("utf-8")
    return json.loads(body)


def write_message(msg: dict[str, Any]) -> None:
    """Write a JSON-RPC message to stdout with Content-Length framing."""
    body = json.dumps(msg, ensure_ascii=False, default=str)
    data = body.encode("utf-8")
    sys.stdout.buffer.write(f"Content-Length: {len(data)}\r\n\r\n".encode())
    sys.stdout.buffer.write(data)
    sys.stdout.buffer.flush()


# ── Tool definitions (JSON Schema for each tool's input) ─────────────────────

TOOLS: list[dict[str, Any]] = [
    {
        "name": "ollama_generate",
        "description": (
            "Generate text from a local Ollama model. "
            "Best for: summarization, translation, classification, Q&A, "
            "or any single-turn prompt task. "
            "Use gemma3:270m for speed, whiterabbit-neo:13b for reasoning."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "model": {
                    "type": "string",
                    "description": (
                        "Model tag, e.g. gemma3:270m, whiterabbit-neo:13b"
                    ),
                    "default": "gemma3:270m",
                },
                "prompt": {
                    "type": "string",
                    "description": "The user prompt / instruction",
                },
                "system": {
                    "type": "string",
                    "description": "Optional system prompt for context",
                },
                "temperature": {
                    "type": "number",
                    "description": "0.0 = deterministic, 1.0 = creative",
                    "default": 0.7,
                },
                "num_predict": {
                    "type": "integer",
                    "description": "Max tokens in the response",
                    "default": 1024,
                },
            },
            "required": ["prompt"],
        },
    },
    {
        "name": "ollama_chat",
        "description": (
            "Multi-turn chat with a local Ollama model. "
            "Supports system / user / assistant roles. "
            "Best for: interactive conversations, iterative refinement, "
            "or when you need to maintain conversation state."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "model": {
                    "type": "string",
                    "description": "Model tag (default: gemma3:270m)",
                    "default": "gemma3:270m",
                },
                "messages": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "role": {
                                "type": "string",
                                "enum": ["system", "user", "assistant"],
                            },
                            "content": {"type": "string"},
                        },
                        "required": ["role", "content"],
                    },
                    "description": "Chat history array",
                },
                "temperature": {
                    "type": "number",
                    "description": "0.0–2.0",
                    "default": 0.7,
                },
            },
            "required": ["messages"],
        },
    },
    {
        "name": "ollama_list_models",
        "description": (
            "List every Ollama model currently downloaded on this machine. "
            "Returns name, size, and modification date for each."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "ollama_ps",
        "description": (
            "Show models that are currently loaded into memory on the "
            "Ollama server."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "ollama_embed",
        "description": (
            "Generate a vector embedding for the given text using a local "
            "Ollama model. Useful for semantic search, clustering, or "
            "feeding into a RAG pipeline."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "model": {
                    "type": "string",
                    "description": "Model tag (default: gemma3:270m)",
                    "default": "gemma3:270m",
                },
                "input": {
                    "type": "string",
                    "description": "Text to embed",
                },
            },
            "required": ["input"],
        },
    },
    {
        "name": "ollama_pull",
        "description": (
            "Download a model from the Ollama library. "
            "E.g. llama3.2:3b, nomic-embed-text, mistral:7b. "
            "Blocks until download completes."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Model name:tag to pull",
                },
            },
            "required": ["name"],
        },
    },
]


# ── Tool implementations ─────────────────────────────────────────────────────


def _ollama_post(endpoint: str, payload: dict, timeout: int) -> dict:
    """POST to Ollama and return parsed JSON."""
    resp = requests.post(f"{OLLAMA_BASE}{endpoint}", json=payload, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def _ollama_get(endpoint: str, timeout: int = TIMEOUT_DEFAULT) -> dict:
    """GET from Ollama and return parsed JSON."""
    resp = requests.get(f"{OLLAMA_BASE}{endpoint}", timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def handle_tool_call(name: str, args: dict) -> dict:
    """Route a tool invocation to the right handler and return MCP content."""
    try:
        # ── ollama_generate ──────────────────────────────────────────
        if name == "ollama_generate":
            model = args.get("model", "gemma3:270m")
            prompt = args["prompt"]
            system = args.get("system")
            temperature = args.get("temperature", 0.7)
            num_predict = args.get("num_predict", 1024)

            payload: dict = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": temperature, "num_predict": num_predict},
            }
            if system:
                payload["system"] = system

            result = _ollama_post("/api/generate", payload, TIMEOUT_GENERATE)
            return {"content": [{"type": "text", "text": result.get("response", "")}]}

        # ── ollama_chat ──────────────────────────────────────────────
        elif name == "ollama_chat":
            model = args.get("model", "gemma3:270m")
            messages = args["messages"]
            temperature = args.get("temperature", 0.7)

            result = _ollama_post(
                "/api/chat",
                {
                    "model": model,
                    "messages": messages,
                    "stream": False,
                    "options": {"temperature": temperature},
                },
                TIMEOUT_GENERATE,
            )
            return {
                "content": [
                    {"type": "text", "text": result["message"]["content"]}
                ]
            }

        # ── ollama_list_models ───────────────────────────────────────
        elif name == "ollama_list_models":
            data = _ollama_get("/api/tags")
            models = data.get("models", [])
            lines = []
            for m in models:
                size_gb = m["size"] / (1024 ** 3)
                lines.append(
                    f"  {m['name']:<35s} {size_gb:>6.2f} GB"
                )
            text = (
                f"Models available ({len(models)}):\n" + "\n".join(lines)
                if models
                else "No models downloaded yet. Use ollama_pull to get one."
            )
            return {"content": [{"type": "text", "text": text}]}

        # ── ollama_ps ────────────────────────────────────────────────
        elif name == "ollama_ps":
            data = _ollama_get("/api/ps")
            models = data.get("models", [])
            text = (
                json.dumps(models, indent=2, ensure_ascii=False)
                if models
                else "No models currently loaded."
            )
            return {"content": [{"type": "text", "text": text}]}

        # ── ollama_embed ─────────────────────────────────────────────
        elif name == "ollama_embed":
            model = args.get("model", "gemma3:270m")
            input_text = args["input"]
            result = _ollama_post(
                "/api/embed",
                {"model": model, "input": input_text},
                TIMEOUT_DEFAULT,
            )
            emb = result.get("embeddings", [])
            dims = len(emb[0]) if emb else 0
            text = (
                f"Embedding generated — dimensions: {dims}, "
                f"vector preview (first 5): {emb[0][:5] if emb else 'N/A'}"
            )
            return {"content": [{"type": "text", "text": text}]}

        # ── ollama_pull ──────────────────────────────────────────────
        elif name == "ollama_pull":
            model_name = args["name"]
            result = _ollama_post(
                "/api/pull",
                {"name": model_name, "stream": False},
                TIMEOUT_PULL,
            )
            status = result.get("status", "done")
            return {
                "content": [
                    {"type": "text", "text": f"Model {model_name}: {status}"}
                ]
            }

        # ── Unknown tool ─────────────────────────────────────────────
        else:
            return {
                "content": [{"type": "text", "text": f"Unknown tool: {name}"}],
                "isError": True,
            }

    except requests.exceptions.ConnectionError:
        return {
            "content": [
                {
                    "type": "text",
                    "text": (
                        "⚠️  Cannot connect to Ollama.\n"
                        "     Is the server running?\n"
                        "     Try:  ollama serve   or   sudo systemctl start ollama"
                    ),
                }
            ],
            "isError": True,
        }
    except requests.exceptions.Timeout:
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"⏱  Request timed out for tool '{name}'.\n"
                    "     The model might be too large for your hardware, or "
                    "Ollama is busy.",
                }
            ],
            "isError": True,
        }
    except Exception as exc:
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"💥 Error: {exc}\n\n{traceback.format_exc()}",
                }
            ],
            "isError": True,
        }


# ── Main event loop ──────────────────────────────────────────────────────────


def main() -> None:
    """Run the MCP server: read JSON-RPC requests from stdin and respond."""
    # Stderr is visible in opencode's logs — useful for debugging
    print(f"[{SERVER_NAME} v{SERVER_VERSION}] Starting...", file=sys.stderr)

    while True:
        try:
            msg = read_message()
            if msg is None:
                print(f"[{SERVER_NAME}] EOF — shutting down.", file=sys.stderr)
                break

            msg_id: Any = msg.get("id")
            method: str = msg.get("method", "")
            params: dict = msg.get("params", {})

            # ── initialize ───────────────────────────────────────────
            if method == "initialize":
                write_message({
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "protocolVersion": PROTOCOL_VERSION,
                        "capabilities": {"tools": {}},
                        "serverInfo": {
                            "name": SERVER_NAME,
                            "version": SERVER_VERSION,
                        },
                    },
                })

            # ── initialized notification (no response) ───────────────
            elif method == "notifications/initialized":
                print(
                    f"[{SERVER_NAME}] Client initialized — tools ready.",
                    file=sys.stderr,
                )

            # ── tools/list ───────────────────────────────────────────
            elif method == "tools/list":
                write_message({
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"tools": TOOLS},
                })
                print(
                    f"[{SERVER_NAME}] Listed {len(TOOLS)} tools for client.",
                    file=sys.stderr,
                )

            # ── tools/call ───────────────────────────────────────────
            elif method == "tools/call":
                tool_name = params.get("name", "")
                tool_args = params.get("arguments", {})
                print(
                    f"[{SERVER_NAME}] Calling tool: {tool_name}",
                    file=sys.stderr,
                )
                result = handle_tool_call(tool_name, tool_args)
                write_message({
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": result,
                })

            # ── Fallback ─────────────────────────────────────────────
            else:
                write_message({
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}",
                    },
                })

        except json.JSONDecodeError as jde:
            print(f"[{SERVER_NAME}] JSON decode error: {jde}", file=sys.stderr)
        except KeyboardInterrupt:
            print(f"[{SERVER_NAME}] Interrupted — exiting.", file=sys.stderr)
            break
        except Exception as exc:
            print(
                f"[{SERVER_NAME}] Unhandled error: {exc}",
                file=sys.stderr,
            )
            traceback.print_exc(file=sys.stderr)


if __name__ == "__main__":
    main()
