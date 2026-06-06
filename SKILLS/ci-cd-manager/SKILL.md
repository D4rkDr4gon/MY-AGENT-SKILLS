---
name: ci-cd-manager
description: Use when setting up or managing CI/CD pipelines — GitHub Actions, Git hooks, automation of builds/tests/deploy, matrix builds, environment management, secrets in CI, and deployment strategies.
---

# ci-cd-manager

Guía de CI/CD para automatización de builds, tests y deploys. Orientada a proyectos personales en GitHub.

## Contexto del usuario

- **Plataforma:** GitHub (gh CLI + GitHub Actions)
- **Repos:** `D4rkDr4g0n/dotfiles`, proyectos en `~/projects/`
- **Lenguajes:** Python, Go, Shell, JavaScript/TypeScript, Rust
- **Editor:** Neovim (LazyVim)

---

## 1. GitHub Actions — Conceptos

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Run a script
        run: echo "Hello from CI!"
```

### Triggers comunes
```yaml
on:
  push:                              # En cada push
  pull_request:                      # En PRs
  schedule:                          # Programado
    - cron: '0 6 * * 1'             # Lunes 6am UTC
  workflow_dispatch:                 # Manual (botón en UI)
  release:
    types: [published]               # Cuando se publica release
```

---

## 2. Workflows por lenguaje

### Python
```yaml
name: Python CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']
    
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov ruff mypy
      
      - name: Lint
        run: ruff check .
      
      - name: Type check
        run: mypy src/
      
      - name: Test
        run: pytest --cov=src/ --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v4
```

### Go
```yaml
name: Go CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-go@v5
        with:
          go-version: '1.22'
          cache: true
      
      - name: Lint
        uses: golangci/golangci-lint-action@v4
      
      - name: Test
        run: go test -v -race ./...
      
      - name: Build
        run: go build -o app .
```

### Rust
```yaml
name: Rust CI

on: [push, pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions-rust-lang/setup-rust-toolchain@v1
      
      - name: Format check
        run: cargo fmt --check
      
      - name: Clippy
        run: cargo clippy -- -D warnings
      
      - name: Test
        run: cargo test
      
      - name: Build
        run: cargo build --release
```

### Node.js / TypeScript
```yaml
name: Node CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: ['18', '20', '22']
    
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'
      
      - run: npm ci
      - run: npm run lint
      - run: npm test
      - run: npm run build
```

---

## 3. Secretos y variables de entorno

```yaml
# NUNCA hardcodear secrets en el workflow
# Usar GitHub Secrets (Settings → Secrets and variables → Actions)

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        env:
          API_KEY: ${{ secrets.API_KEY }}
          API_URL: ${{ vars.API_URL }}            # Variables de entorno
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}    # Token automático
        run: ./deploy.sh
```

### Secrets recomendados para tu perfil
```
DOCKER_USERNAME        # Para push a Docker Hub/GHCR
DOCKER_PASSWORD
API_KEY                # Para services
SSH_PRIVATE_KEY        # Para deploy via SSH (base64)
```

---

## 4. Publicación y releases

### GitHub Release Automation
```yaml
name: Release

on:
  push:
    tags:
      - 'v*.*.*'

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Build
        run: |
          mkdir -p dist
          # Build for multiple platforms
          GOOS=linux GOARCH=amd64 go build -o dist/app-linux-amd64
          GOOS=windows GOARCH=amd64 go build -o dist/app-windows-amd64.exe
      
      - name: Create Release
        uses: softprops/action-gh-release@v2
        with:
          files: |
            dist/*
          generate_release_notes: true
          draft: false
```

### Publish to PyPI
```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      id-token: write  # OIDC for PyPI
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      
      - run: pip install build
      - run: python -m build
      
      - name: Publish
        uses: pypa/gh-action-pypi-publish@release/v1
```

---

## 5. Git Hooks + CI (pre-commit)

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
  
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.10.0
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]
  
  - repo: https://github.com/woodruffw/zizmor
    rev: v0.3.0
    hooks:
      - id: zizmor  # Security audit for GH Actions
```

```bash
# Instalar hooks
pip install pre-commit
pre-commit install

# Ejecutar manualmente
pre-commit run --all-files
```

---

## 6. Matrix Builds

```yaml
# Estrategia de matrices (útil para multi-plataforma)
jobs:
  build:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python: ['3.10', '3.11', '3.12']
        exclude:
          - os: macos-latest
            python: '3.10'       # Excluir combinaciones específicas
        include:
          - os: ubuntu-latest
            python: '3.12'
            extra: 'coverage'    # Variables extra por celda
    
    runs-on: ${{ matrix.os }}
    
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python }}
```

---

## 7. Docker CI

```yaml
name: Docker Build

on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  docker:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Login to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ghcr.io/${{ github.repository }}
      
      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

---

## 8. Seguridad en CI/CD

### Zizmor — Audit de Actions
```yaml
# Zizmor detecta configuraciones inseguras en workflows
# Se ejecuta como pre-commit hook (ver sección 5)

# Ejemplos de lo que detecta:
# - Pin actions por SHA (no por tag)
# - No usar GITHUB_TOKEN con permisos excesivos
# - No usar `pull_request_target` sin validación
# - No inyectar inputs directamente en scripts
```

### Buenas prácticas de seguridad en CI
```yaml
# ✅ Pin actions a SHA commit
- uses: actions/checkout@v4                              # ❌ Tag (mutable)
- uses: actions/checkout@a81bbbf8298c0fa03ea29cdc473d45769f953675  # ✅ SHA (inmutable)

# ✅ Mínimos permisos
permissions:
  contents: read           # Solo lo que necesita
  # No escribir si no es necesario

# ✅ No usar pull_request_target input sin validación
# ❌ Peligroso: permite PRs maliciosos acceder a secrets
```

---

## 9. Buenas prácticas

1. **CI antes de merge** — nunca pushear a main sin pasar CI
2. **Tests rápidos** — CI debe correr en < 5 minutos idealmente
3. **Matrix builds** — testear contra múltiples versiones/OS
4. **Caché de dependencias** — pip/npm/go cache reduce tiempo >50%
5. **Secrets en GitHub Secrets** — nunca en código ni en vars de workflow
6. **Pinned actions** — usar SHA en lugar de tags para seguridad
7. **Workflows pequeños** — un workflow por propósito (test, lint, deploy)
8. **Release automation** — tags v*.*.* automaticen builds y publicación
9. **Pre-commit hooks** — atrapar errores antes del CI (feedback loop más rápido)
10. **Monitorear fallos** — configurar notificaciones en GitHub
