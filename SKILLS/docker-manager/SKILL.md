---
name: docker-manager
description: Use when managing Docker/Podman containers, images, volumes, networks, or Docker Compose. Cross-platform (Linux + Windows + WSL). Also for malware analysis sandboxing.
---

# docker-manager

## Cross-Platform

Este skill funciona en **Arch Linux** y **Windows 11** (via Docker Desktop o WSL):

| Recurso | Linux (Arch) | Windows |
|---------|-------------|---------|
| Engine | Docker CE + podman | Docker Desktop / podman |
| Comando | `docker`, `podman` | `docker`, `podman` |
| Compose | `docker compose` (plugin) | `docker compose` |
| WSL integration | — | `wsl -d docker-desktop` |
| Almacenamiento | `/var/lib/docker/` | `C:\ProgramData\Docker\` |

## Comandos esenciales

### Containers

```bash
# Listar
docker ps                    # En ejecución
docker ps -a                 # Todos
docker ps --format '{{.Names}} {{.Status}}'

# Ejecutar
docker run -it --rm ubuntu:22.04 bash
docker run -d --name web -p 8080:80 nginx:alpine
docker run --rm -v "$(pwd):/data" -w /data python:3.12 python script.py

# Gestion
docker start/stop/restart <container>
docker rm <container>        # Eliminar
docker rm -f $(docker ps -aq)  # Eliminar todos
docker logs -f <container>   # Logs en vivo
docker exec -it <container> bash

# Inspect
docker inspect <container>   # JSON completo
docker stats                 # Recursos en vivo
docker top <container>       # Procesos dentro
```

### Images

```bash
# Listar y buscar
docker images
docker search <name>

# Build
docker build -t my-image:tag .
docker build --no-cache -t my-image:tag .

# Push/Pull
docker pull ubuntu:22.04
docker push myuser/my-image:tag

# Limpiar
docker rmi <image>           # Eliminar
docker image prune           # Huérfanas
docker system prune -a       # TODO lo no usado (cuidado)
```

### Volumes

```bash
docker volume ls
docker volume create my-volume
docker volume inspect my-volume
docker volume prune          # Eliminar no usados
```

### Networks

```bash
docker network ls
docker network create --subnet 172.20.0.0/16 lab-net
docker network inspect lab-net
docker run --net lab-net --ip 172.20.0.10 -d nginx
```

## Docker Compose

```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8080:8080"
    volumes:
      - .:/app
    environment:
      - DEBUG=true
  db:
    image: postgres:15
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: changeme

volumes:
  pgdata:
```

```bash
docker compose up -d              # Levantar
docker compose down               # Bajar
docker compose logs -f            # Logs
docker compose build              # Rebuild
docker compose exec app bash      # Shell dentro de servicio
docker compose -f lab.yml up -d   # Archivo específico
```

## Sandboxing para Malware Analysis

Este es un caso de uso específico para tu perfil CSIRT:

### REMnux (análisis de malware Linux)
```bash
docker pull remnux/remnux-distro
docker run -it --rm \
  -v $HOME/malware-samples:/samples:ro \
  --cap-add=SYS_PTRACE \
  --security-opt seccomp=unconfined \
  remnux/remnux-distro bash
```

### Sandbox aislado con red limitada
```bash
# Crear red sin salida a internet
docker network create --internal sandbox-net

# Ejecutar con red aislada
docker run -it --rm \
  --net sandbox-net \
  -v $HOME/malware-samples:/samples:ro \
  ubuntu:22.04 bash
```

### Cuckoo Sandbox (si usás)
```bash
docker pull blacktop/cuckoo
docker run -d --name cuckoo \
  -v $HOME/cuckoo/conf:/conf \
  -v $HOME/cuckoo/storage:/storage \
  -p 8090:8090 \
  blacktop/cuckoo
```

### FLARE VM (Windows en VM, no Docker)
Para análisis en Windows, preferí VM con FLARE VM en lugar de Docker.

## Podman (alternativa rootless)

```bash
# En Arch
sudo pacman -S podman podman-compose

# Comandos equivalentes (ídem docker)
podman ps
podman run -it --rm ubuntu:22.04 bash
podman build -t my-image .

# Rootless (seguridad)
podman run --userns=keep-id -v "$(pwd):/data:Z" ...
```

## Dockerfiles útiles

### Python minimal
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

### Rust build
```dockerfile
FROM rust:1.75-slim AS builder
WORKDIR /app
COPY . .
RUN cargo build --release

FROM debian:bookworm-slim
COPY --from=builder /app/target/release/app /usr/local/bin/
CMD ["app"]
```

### Multi-stage (Go/Python)
```dockerfile
# Build stage
FROM golang:1.22 AS build
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 go build -o server .

# Runtime stage
FROM alpine:3.19
RUN apk add --no-cache ca-certificates
COPY --from=build /app/server /server
EXPOSE 8080
CMD ["/server"]
```

## Limpieza y mantenimiento

```bash
# Espacio en disco
docker system df

# Limpieza segura (solo lo no usado)
docker container prune
docker image prune
docker volume prune
docker network prune

# Nuclear (cuidado — borra TODO)
docker system prune -a --volumes
```

## Buenas prácticas

1. **Siempre especificar versión de imagen** (`ubuntu:22.04`, no `ubuntu:latest`)
2. **Usar `.dockerignore`** para no copiar basura al build context
3. **Preferir imágenes slim/alpine** para producción
4. **No ejecutar como root** dentro del container si no es necesario
5. **No exponer el daemon socket de Docker** (`/var/run/docker.sock`) a menos que sea estrictamente necesario
6. **Para malware analysis**: usar red aislada (`--internal`), mounts de solo lectura, y nunca exponer el sandbox a tu LAN
7. **Docker Compose** para entornos multi-servicio (labs de pentesting, entornos de desarrollo)
8. **Healthchecks** en producción
9. **Logging limitado**: `--log-opt max-size=10m --log-opt max-file=3`
