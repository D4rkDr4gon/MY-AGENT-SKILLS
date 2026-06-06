---
name: container-security-manager
description: Use when securing container environments — Trivy vulnerability scanning, Docker Bench Security, Grype, cosign image signing, SBOM generation, supply chain security, and Dockerfile/Compose security best practices.
---

# container-security-manager

Guía de seguridad de containers para DevSecOps y análisis de malware. Complementa `docker-manager` con el enfoque security.

## Contexto del usuario

- **Containers:** Docker CE + Podman
- **SO:** Arch Linux (primario)
- **Uso principal:** Sandboxing de malware, laboratorios de pentesting, desarrollo
- **Herramientas:** `trivy`, `grype`, `docker-bench-security`, `cosign`, `syft`

---

## 1. Trivy — Vulnerability Scanner

### Escaneo de imágenes
```bash
# Instalar
sudo pacman -S trivy           # o descargar binario de GH releases

# Escanear imagen
trivy image ubuntu:22.04
trivy image python:3.12-slim

# Escanear por severidad
trivy image --severity HIGH,CRITICAL nginx:alpine

# Escanear solo ciertos tipos
trivy image --vuln-type os,library ubuntu:22.04
trivy image --scanners vuln,secret,misconfig my-image:latest

# Salida JSON para procesar
trivy image --format json --output scan.json nginx:1.25
```

### Escaneo de filesystem y repos
```bash
# Escanear proyecto local
trivy fs /home/lcampassi/projects/my-app

# Escanear repositorio git
trivy repo https://github.com/user/repo.git
trivy repo --branch main /path/to/local/repo

# Escanear SBOM
trivy sbom sbom.spdx.json
```

### Integración con Docker
```bash
# Escanear antes de build (CI)
# En Dockerfile o script CI
trivy image --exit-code 1 --severity CRITICAL my-image:latest
# exit-code 1 → falla si hay CRITICAL
```

---

## 2. Docker Bench Security

```bash
# Clonar repo
git clone https://github.com/docker/docker-bench-security.git
cd docker-bench-security

# Ejecutar
sudo ./docker-bench-security.sh

# Docker (ejecutar desde container)
docker run --pid=host -v /etc:/etc:ro \
  -v /usr:/usr:ro \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  --label docker_bench_security \
  docker/docker-bench-security

# Checkpoints importantes que revisa:
# - 1.1: Host Configuration (CIS Benchmark)
# - 2.1: Docker daemon configuration
# - 3.1: Container images
# - 4.1: Container runtime
# - 5.1: Security operations
```

### Resultados clave
```bash
# [PASS]  - Correcto
# [WARN]  - Requiere atención
# [NOTE]  - Recomendación informativa
# [FAIL]  - Incumplimiento (requiere acción)

# Corregir WARN comunes:
# - Usar usuario no-root en container
# - Limitar capabilities (--cap-drop=ALL --cap-add=needed)
# - No exponer /var/run/docker.sock
# - Usar contenido de solo lectura (--read-only)
# - Habilitar Content Trust (DOCKER_CONTENT_TRUST=1)
```

---

## 3. Grype — Vulnerability Scanner (alternativa rápida)

```bash
# Instalar
curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin

# Escanear imagen
grype ubuntu:22.04
grype python:3.12-slim

# Escanear por severidad
grype --only-fixed nginx:alpine   # Solo vulns con fix disponible

# Output JSON
grype -o json nginx:1.25 > grype-scan.json
```

---

## 4. Syft — SBOM Generation

```bash
# Instalar
curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin

# Generar SBOM (Software Bill of Materials)
syft ubuntu:22.04 -o spdx-json > ubuntu-sbom.spdx.json
syft ubuntu:22.04 -o cyclonedx-json > ubuntu-sbom.cyclonedx.json
syft ubuntu:22.04 -o syft-json > ubuntu-sbom.syft.json

# SBOM de un proyecto
syft dir:/home/lcampassi/projects/my-app -o spdx-json

# Verificar SBOM con el propio syft
syft packages sbom:ubuntu-sbom.spdx.json
```

---

## 5. Cosign — Container Signing

```bash
# Instalar
sudo pacman -S cosign

# Generar par de claves
cosign generate-key-pair

# Firmar imagen
cosign sign --key cosign.key ghcr.io/user/image:tag

# Verificar firma
cosign verify --key cosign.pub ghcr.io/user/image:tag

# Verificar sin clave (usando keyless)
cosign verify ghcr.io/user/image:tag

# Verificar en Dockerfile/CI
cosign verify-attestation --type spdx ghcr.io/user/image:tag
```

---

## 6. Dockerfile Security Best Practices

```dockerfile
# ❌ Mal
FROM ubuntu:latest
RUN apt-get update && apt-get install -y python3
COPY . /app
CMD ["python3", "app.py"]

# ✅ Bien
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Security: no-root
RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser

COPY app.py .
CMD ["python", "app.py"]

# Notas de seguridad:
# - No usar :latest, pin versión
# - Multi-stage para reducir superficie
# - No root
# - --no-cache-dir (no caché pip innecesaria)
# - COPY explícito, no COPY . .
# - --chown=appuser:appuser en COPY si necesitás writes
```

### Docker Compose Security
```yaml
version: '3.8'
services:
  app:
    image: my-app:1.0
    # No root
    user: "1000:1000"
    # Read-only filesystem (solo tmpfs para writes)
    read_only: true
    tmpfs:
      - /tmp
    # Dropear todas las capabilities, agregar solo necesarias
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    # No privileged
    privileged: false
    # No exponer docker socket
    # volumes:
    #   - /var/run/docker.sock:/var/run/docker.sock  # ❌ No hacer
    # Security options
    security_opt:
      - no-new-privileges:true
      - seccomp=default
    # Limitar recursos
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```

---

## 7. Supply Chain Security

```bash
# Verificar firmas de imágenes oficiales
docker trust inspect --pretty alpine:latest

# Habilitar Docker Content Trust (solo imágenes firmadas)
export DOCKER_CONTENT_TRUST=1
docker pull alpine:latest   # Fallará si no está firmada
docker push my-image:tag    # Forzará firmar

# Escanear dependencias del proyecto
trivy fs --scanners vuln --severity HIGH,CRITICAL /home/lcampassi/projects/my-app

# Verificar checksums de imágenes
docker image inspect --format '{{.RepoDigests}}' alpine:latest
```

---

## 8. Sandboxing Seguro (Malware Analysis)

Combinación con `docker-manager` para análisis de malware:

```bash
# Container ultra-restrictivo para análisis
docker run -it --rm \
  --name sandbox \
  --network none \                            # Sin red
  --cap-drop ALL \                            # Sin capabilities
  --security-opt seccomp=/tmp/deny-all.json \ # Seccomp restrictivo
  --security-opt apparmor=sandbox-profile \   # AppArmor (si configurado)
  --read-only \                               # FS solo lectura
  --tmpfs /tmp:noexec,nosuid,size=100M \      # /tmp en memoria
  --memory 512m \                             # Límite RAM
  --cpus 0.5 \                                # Límite CPU
  --pids-limit 50 \                           # Límite de procesos
  -v /home/lcampassi/samples:/samples:ro \    # Muestras RO
  ubuntu:22.04 bash
```

---

## 9. Buenas prácticas

1. **No usar `:latest`** — siempre pin tear versión específica
2. **Multi-stage builds** — imagen final solo con lo necesario
3. **No root** — crear y usar usuario no-root en containers
4. **Read-only filesystem** — `read_only: true` en compose
5. **Drop all capabilities** — `cap_drop: ALL` y solo agregar necesarias
6. **No privileged** — `privileged: false` siempre
7. **No exponer docker.sock** — a menos que sea estrictamente necesario
8. **Escanear imágenes** — trivy/grype antes de deployar
9. **Limitar recursos** — memoria, CPU, pids para evitar DoS
10. **Seccomp/AppArmor** — perfiles de seguridad para restringir syscalls
11. **Content Trust** — verificar firmas de imágenes oficiales
12. **SBOM** — mantener SBOM actualizado para auditoría de supply chain
