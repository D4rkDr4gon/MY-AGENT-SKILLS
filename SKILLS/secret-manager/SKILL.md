---
name: secret-manager
description: Use when managing passwords, secrets, API keys, GPG keys, encrypted files, and credentials. Covers pass (password-store), age, sops, gopass, bitwarden-cli, GPG key management, .env files, and backup of cryptographic material.
---

# secret-manager

Guía para la gestión de secrets, contraseñas y material criptográfico en el contexto de ciberseguridad y administración de sistemas.

## Contexto del usuario

- **SO:** Arch Linux (primario) + Windows 11
- **Gestor de contraseñas:** `pass` (password-store) con git
- **Cifrado de archivos:** `age` (moderno), `gpg` (legacy)
- **Secrets en configs:** `sops` (Mozilla SOPS)
- **Bitwarden:** CLI (`bw`) para vault online
- **GPG:** Claves para firma de commits y cifrado

---

## 1. `pass` — Password Store

### Setup inicial
```bash
# Instalar
sudo pacman -S pass pass-otp

# Inicializar con clave GPG
pass init <gpg-key-id>

# Inicializar con git
pass git init
pass git remote add origin git@github.com:tu-user/password-store.git
```

### Comandos esenciales
```bash
# Agregar contraseña
pass insert lab/htb/portal
pass insert email/security@example.com

# Generar contraseña automática
pass generate lab/thm/vip 32          # 32 caracteres
pass generate lab/thm/vip -n 20       # Sin símbolos
pass generate lab/thm/vip -c 16       # 16 chars, copiar al clipboard

# Ver
pass lab/htb/portal
pass show lab/htb/portal | head -1    # Solo pass, sin metadatos

# Copiar al clipboard (se borra automáticamente en 45s)
pass -c lab/htb/portal

# Editar
pass edit lab/htb/portal

# Buscar
pass find htb
pass grep "example"

# Tree
pass git log --oneline

# OTP (si está configurado)
pass otp lab/vpn/otp-secret
pass otp -c lab/vpn/otp-secret
```

### Estructura recomendada
```
Password Store/
├── email/
│   ├── personal@example.com
│   └── work@company.com
├── lab/
│   ├── htb/
│   │   ├── portal      # Contraseña del portal
│   │   └── vpn         # .ovpn sin credenciales embebidas
│   ├── thm/
│   └── vpn/
├── wifi/
│   ├── casa
│   └── oficina
├── api/
│   ├── github-token
│   ├── digitalocean-token
│   └── cloudflare-token
└── banking/
```

---

## 2. `age` — Cifrado moderno de archivos

`age` es más simple y seguro que GPG para cifrado de archivos. Recomendado para backups y secrets.

```bash
# Generar clave
age-keygen -o ~/.age/key.txt

# Cifrar archivo
age -r age1...pub -o secret.txt.age secret.txt
age -p -o secret.txt.age secret.txt    # Con passphrase

# Descifrar
age -d -i ~/.age/key.txt -o secret.txt secret.txt.age
age -d -o secret.txt secret.txt.age    # Si tiene passphrase

# Cifrar para múltiples destinatarios
age -r age1...pub -r age2...pub -o shared.txt.age shared.txt

# Cifrar para ssh key (sin generar nueva clave)
age -R ~/.ssh/id_ed25519.pub -o secret.txt.age secret.txt
```

### Integración con YubiKey (via age-plugin-yubikey)
```bash
# Cifrar con yubikey
age-plugin-yubikey --identity
age -r age1yubikey... -o secret.txt.age secret.txt
age -d -i ~/.age/yubikey-identity.txt -o secret.txt secret.txt.age
```

---

## 3. `sops` — Secrets en Configs (Mozilla SOPS)

Ideal para cifrar campos específicos en YAML, JSON, ENV, TOML.

```bash
# Instalar
sudo pacman -S sops
# o descargar binario desde GitHub

# Configurar .sops.yaml en el proyecto
cat > .sops.yaml << 'EOF'
creation_rules:
  - age: age1...pub  # Tu clave pública age
  - path_regex: .*\.env$
    age: age1...pub
EOF
```

### Uso con age
```bash
# Crear archivo cifrado nuevo
sops secrets.yaml

# Cifrar archivo existente
sops -e -i secrets.yaml

# Descifrar
sops -d -i secrets.yaml

# Editar archivo cifrado (abre $EDITOR)
sops secrets.yaml

# Ver archivo descifrado sin tocar el archivo
sops -d secrets.yaml

# Usar con .env
sops --input-type dotenv --output-type dotenv -e .env > .env.sops
```

### Uso con age + variables de entorno
```bash
export SOPS_AGE_KEY_FILE=~/.age/key.txt
sops secrets.yaml
```

---

## 4. GPG — GNU Privacy Guard

### Gestión de claves
```bash
# Listar claves
gpg --list-keys                     # Públicas
gpg --list-secret-keys              # Privadas
gpg --list-secret-keys --keyid-format=long

# Generar clave
gpg --full-generate-key

# Exportar/Importar
gpg --export -a <key-id> > clave-publica.asc
gpg --export-secret-keys -a <key-id> > clave-privada.asc
gpg --import clave-publica.asc

# Subir a keyserver
gpg --send-keys <key-id>
gpg --recv-keys <key-id>

# Backup de claves
gpg --export-secret-keys --armor <key-id> > gpg-secret-keys-backup.asc
gpg --export --armor <key-id> > gpg-public-keys-backup.asc

# Revocar clave (necesario tener el certificado de revocación)
gpg --generate-revocation <key-id> > revocacion.asc
gpg --import revocacion.asc
gpg --keyserver keyserver.ubuntu.com --send-keys <key-id>
```

### Configurar GPG Agent
```bash
# ~/.gnupg/gpg-agent.conf
default-cache-ttl 600
max-cache-ttl 7200
pinentry-program /usr/bin/pinentry-qt   # o pinentry-tty
```

### Cifrado simétrico (passphrase)
```bash
gpg -c archivo.txt                    # Cifrar con passphrase
gpg -o archivo.txt -d archivo.txt.gpg # Descifrar
```

### Cifrado asimétrico (por clave pública)
```bash
gpg -e -r <key-id> archivo.txt        # Cifrar para un destinatario
gpg -d archivo.txt.gpg                # Descifrar
```

---

## 5. Bitwarden CLI (`bw`)

```bash
# Login
bw login
bw login --apikey                     # Con API key (para CI/CD)

# Desbloquear vault (obtener session key)
bw unlock
export BW_SESSION="<session-key>"

# Buscar items
bw list items --search "htb"
bw list items | jq '.[].name'

# Obtener item específico
bw get item <id>
bw get password <id>
bw get username <id>

# Agregar item
bw get template item | jq '.name = "lab/vpn/htb" | .login.username = "$USER"' | bw encode | bw create item

# Editar
bw edit item <id>

# Sincronizar
bw sync

# Logout
bw lock
bw logout
```

---

## 6. API Keys y Tokens

### Almacenamiento seguro con pass
```bash
# Guardar tokens de API
pass insert api/github-token
pass insert api/digitalocean-token
pass insert api/cloudflare-token

# Usar en scripts (cuidado con subshell en log)
export GITHUB_TOKEN=$(pass api/github-token | head -1)
```

### .env cifrado
```bash
# Crear .env.example (sin valores reales)
cat > .env.example << 'EOF'
GITHUB_TOKEN=
DIGITALOCEAN_TOKEN=
OPENAI_API_KEY=
EOF

# .env real cifrado con age
age -p -o .env.age .env

# Cargar en shell
eval $(age -d .env.age)
# o
set -a; source <(age -d .env.age); set +a
```

### SOPS para .env
```bash
# Cifrar .env manteniendo formato
sops --encrypt --input-type dotenv --output-type dotenv .env > .env.sops

# Cargar en shell
eval $(sops -d .env.sops)
```

---

## 7. Backup de Secrets

### Backup completo de material criptográfico
```bash
# 1. GPG keys (toda la jerarquía)
gpg --export-secret-keys --armor > gpg-keys.asc
gpg --export-secret-subkeys --armor >> gpg-keys.asc
gpg --export-ownertrust > gpg-ownertrust.txt

# 2. age keys
cp ~/.age/key.txt ~/backup/age-key.txt

# 3. pass store (el repo git ya es backup si está pusheado)
pass git push

# 4. SSH keys
cp -r ~/.ssh ~/backup/ssh

# 5. Cifrar el backup con age
tar czf secrets-backup.tar.gz gpg-keys.asc gpg-ownertrust.txt age-key.txt ssh/
age -p -o secrets-backup.tar.gz.age secrets-backup.tar.gz

# 6. Almacenar en lugar seguro (USB offline, vault)
```

### Restore
```bash
age -d secrets-backup.tar.gz.age > secrets-backup.tar.gz
tar xzf secrets-backup.tar.gz
gpg --import gpg-keys.asc
gpg --import-ownertrust gpg-ownertrust.txt
cp -r ssh ~/.ssh
chmod 600 ~/.ssh/*
```

---

## 8. Buenas prácticas

### General
1. **Un gestor centralizado** — `pass` para todo, no dispersar credenciales
2. **Backup offline** — claves GPG/age en USB cifrado guardado en lugar seguro
3. **Principio de mínimo privilegio** — cada servicio con su propio token, no compartir
4. **Rotación periódica** — contraseñas de laboratorio cada 90 días, API keys al detectar fuga
5. **Nunca hardcodear secrets** — ni en código, ni en scripts, ni en dotfiles
6. **.gitignore** siempre incluir: `*.env`, `*.age`, `*.sops`, `*secret*`, `*password*`
7. **Preferir `age` sobre `gpg`** para cifrado nuevo — más simple, menos superficie de ataque
8. **2FA/MFA** en todos los servicios que lo soporten, OTP almacenado en `pass otp`

### Para desarrollo
- `.env` local, `.env.sops` en repo (cifrado)
- CI/CD: usar secrets del provider (GitHub Actions Secrets, no variables de entorno del build)
- Pre-commit hooks que detecten credenciales (ver `git-manager`)
- `gitleaks` o `trufflehog` para escaneo de repos en busca de secrets commiteados

### Para ciberseguridad
- Tokens de API de threat intel (AlienVault OTX, VirusTotal, Shodan) en `pass`
- Credenciales de laboratorio (HTB, THM) en `pass` con OTP
- Claves de VPN en `pass`, descifrar y cargar solo durante la sesión
- Certificados y claves TLS internas en `age` cifrado

---

## Referencias

- `pass` docs: `man pass`
- `age` docs: `man age` / https://age-encryption.org
- `sops` docs: https://github.com/getsops/sops
- `bitwarden-cli`: `bw --help`
- GPG: `man gpg`
