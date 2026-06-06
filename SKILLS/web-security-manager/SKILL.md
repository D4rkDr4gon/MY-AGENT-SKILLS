---
name: web-security-manager
description: Use when assessing web application security — OWASP Top 10, Burp Suite, ZAP, SSL/TLS scanning, CORS/CSP/XXE/SSRF analysis, web fuzzing, and secure headers audit. Cross-platform (Linux + Windows).
---

# web-security-manager

Guía de seguridad de aplicaciones web para pentesting y blue team. Cubre herramientas, técnicas y checklist.

## Contexto del usuario

- **Rol:** Pentester (red-copilot) + Blue Team (blue-copilot)
- **SO:** Arch Linux (Burp Suite via AUR, ZAP via snap/pkg)
- **Windows:** Burp Suite (installer), Fiddler, ZAP
- **Navegadores:** Firefox + Chromium para pruebas

---

## 1. OWASP Top 10 (2021)

```
A01 - Broken Access Control
A02 - Cryptographic Failures
A03 - Injection (SQL, NoSQL, OS, LDAP)
A04 - Insecure Design
A05 - Security Misconfiguration
A06 - Vulnerable and Outdated Components
A07 - Identification and Authentication Failures
A08 - Software and Data Integrity Failures
A09 - Security Logging and Monitoring Failures
A10 - Server-Side Request Forgery (SSRF)
```

### Checklist rápido por categoría
```bash
# A01 - Access Control
# Probar: IDOR en parámetros, escalación de privilegios, path traversal
curl -s "https://target.com/api/users/123"       # Intentar 124, 125
curl -s "https://target.com/admin"                # Admin sin auth
curl -s "https://target.com/../etc/passwd"        # Path traversal

# A03 - Injection
# SQLi básico
curl -s "https://target.com/page?id=1' OR '1'='1"
curl -s "https://target.com/page?id=1 UNION SELECT 1,2,3--"

# A10 - SSRF
curl -s "https://target.com/fetch?url=http://169.254.169.254/"  # AWS metadata
curl -s "https://target.com/fetch?url=http://localhost:8080/"
```

---

## 2. Burp Suite

### Setup en Arch Linux
```bash
# Community Edition
sudo pacman -S burp-suite
burp-suite                              # Lanzar GUI

# O desde AUR (Professional si tenés licencia)
yay -S burpsuite-pro

# Proxy setup
# 1. Burp → Proxy → Listeners: 127.0.0.1:8080
# 2. Firefox → Settings → Network → Manual proxy: 127.0.0.1:8080
# 3. Instalar cert de Burp: http://burpsuite → Download CA Certificate
# 4. Importar en Firefox: Preferences → Privacy → Certificates → Import
```

### Workflow básico
```bash
# 1. Interceptar tráfico
#   - Proxy → Intercept → Intercept is on
#   - Navegar por la app web

# 2. Target scope
#   - Target → Scope → Add URL pattern
#   - Filtra tráfico fuera de scope

# 3. Spider/Crawl
#   - Target → Site map → Right click → Spider this host

# 4. Scanner (Community limitado, Professional tiene scan automático)

# 5. Repeater (pruebas manuales)
#   - Right click request → Send to Repeater
#   - Modificar y reenviar requests

# 6. Intruder (fuzzing)
#   - Right click → Send to Intruder
#   - Positions: marcar payload positions
#   - Payloads: wordlists, numbers, custom
#   - Start attack

# 7. Extensions
#   - Extender → BApp Store
#   - Imprescindibles: 
#     - JSON Web Tokens (JWT Editor)
#     - Autorize (access control testing)
#     - Content Type Converter
#     - Turbo Intruder (fuzzing rápido)
```

### Burp Suite CLI (Headless)
```bash
# Proyecto desde CLI (útil para automatización)
java -jar burpsuite_pro.jar \
  --project-file=target-project.burp \
  --config-file=config.json

# Con headless
java -jar burpsuite_pro.jar --headless \
  --project-file=project.burp \
  --config-file=default.json \
  --url=https://target.com
```

---

## 3. OWASP ZAP

```bash
# Instalar
sudo pacman -S zaproxy
zaproxy                                 # GUI

# ZAP Headless (automatización)
zap.sh -daemon -host 127.0.0.1 -port 8080

# ZAP CLI
zap-cli quick-scan -s xss,sqli,csrf https://target.com
zap-cli spider https://target.com
zap-cli active-scan https://target.com
zap-cli alerts                          # Mostrar alertas

# API (ZAP running en daemon)
curl "http://127.0.0.1:8080/JSON/ascan/action/scan/?url=https://target.com&recurse=true"

# Docker
docker run -u zap -p 8080:8080 -i softwaresecurityproject/zap-stable \
  zap.sh -daemon -host 0.0.0.0 -port 8080
```

---

## 4. SSL/TLS Scanning

```bash
# testssl.sh (recomendado)
# Clonar repo
git clone --depth 1 https://github.com/drwetter/testssl.sh.git
cd testssl.sh

# Scan completo
./testssl.sh https://target.com

# Scans específicos
./testssl.sh --protocols https://target.com       # Protocolos soportados
./testssl.sh --cipher-per-proto https://target.com # Ciphers por protocolo
./testssl.sh --headers https://target.com          # Security headers
./testssl.sh --vulnerabilities https://target.com  # Heartbleed, CCS, etc.

# SSL Labs API
curl -s "https://api.ssllabs.com/api/v3/analyze?host=target.com"

# OpenSSL manual
openssl s_client -connect target.com:443 -tls1_2
openssl s_client -connect target.com:443 -tls1_3
```

---

## 5. Security Headers Audit

```bash
# Ver headers de respuesta
curl -sI https://target.com | grep -iE 'strict-transport|content-security|x-frame|x-content|x-xss|referrer'

# Headers esenciales
# Strict-Transport-Security: max-age=31536000; includeSubDomains
# Content-Security-Policy: default-src 'self'; script-src 'self'
# X-Frame-Options: DENY
# X-Content-Type-Options: nosniff
# Referrer-Policy: strict-origin-when-cross-origin
# Permissions-Policy: geolocation=(), camera=(), microphone=()
# X-XSS-Protection: 0  (deprecated pero a veces presente)

# Verificar con securityheaders.com
curl -s "https://securityheaders.com/?q=https://target.com&followRedirects=on"
```

### Cheatsheet CSP
```bash
# CSP segura (start)
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'

# CSP permisiva (solo para testing)
Content-Security-Policy: default-src 'none'; script-src 'unsafe-inline'; ...

# Report-only (no bloquea, solo reporta)
Content-Security-Policy-Report-Only: default-src 'self'; report-uri /csp-report
```

---

## 6. Fuzzing web

```bash
# ffuf (rápido, moderno)
ffuf -u https://target.com/FUZZ -w /usr/share/wordlists/dirb/common.txt
ffuf -u https://target.com/api/FUZZ -w api-endpoints.txt
ffuf -u https://target.com/page?id=FUZZ -w ids.txt -fc 404

# Con extensiones
ffuf -u https://target.com/FUZZ -w wordlist.txt -e .php,.asp,.aspx,.jsp

# Con headers personalizados
ffuf -u https://target.com/FUZZ -w wordlist.txt -H "Authorization: Bearer <token>"

# Gobuster (alternativa)
gobuster dir -u https://target.com -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
gobuster vhost -u https://target.com -w subdomains.txt  # Virtual hosts

# Param mining (con ParamSpider o similar)
# Buscar parámetros ocultos en JS
curl -s https://target.com/static/app.js | grep -oP '["'"'"']?\w+["'"'"']?\s*[:=]' | tr -d '":= '
```

---

## 7. Análisis de JWT

```bash
# Decodificar JWT (sin verificar firma)
jwt-cli decode "eyJhbGciOiJIUzI1NiIs..."
echo "eyJhbGciOiJIUzI1NiIs..." | base64 -d 2>/dev/null || true

# jwt_tool (auditoría de JWT)
git clone https://github.com/ticarpi/jwt_tool.git
python3 jwt_tool.py "eyJhbGciOiJIUzI1NiIs..."

# Ataques comunes
# - alg: none → cambiar a "alg": "none"
# - alg: HS256 → usar clave pública como HMAC secret
# - JWK injection → injectar clave pública falsa
# - Kid injection → path traversal en kid header
# - Expiración → cambiar a valores futuros
```

---

## 8. API Security

```bash
# REST API fuzzing
ffuf -u https://api.target.com/v1/FUZZ -w api-endpoints.txt
ffuf -u https://api.target.com/v1/user -X POST -d '{"FUZZ":"test"}' -w params.txt

# Rate limiting test
for i in $(seq 1 100); do
  curl -s -o /dev/null -w "%{http_code}\n" -X POST \
    https://api.target.com/login -d 'user=admin&pass=test'
done | sort | uniq -c

# GraphQL introspection
curl -s https://api.target.com/graphql \
  -H 'Content-Type: application/json' \
  -d '{"query": "{ __schema { types { name fields { name } } } }"}'

# Mass assignment
curl -X PUT https://api.target.com/user/123 \
  -H 'Content-Type: application/json' \
  -d '{"role": "admin", "is_admin": true}'  # Probar parámetros no esperados
```

---

## 9. Buenas prácticas

1. **Siempre con autorización** — no escanear sin permiso explícito
2. **Scope claro** — definir URLs en scope en Burp/ZAP antes de empezar
3. **Proxy + Browser** — configurar proxy antes de navegar
4. **Certificados** — instalar CA cert de Burp/ZAP en el browser para ver HTTPS
5. **Wordlists** — usar SecLists (`/usr/share/seclists/` en Kali/Arch)
6. **Logging** — guardar requests/respuestas interesantes
7. **Falsos positivos** — verificar manualmente antes de reportar
8. **Rate limiting** — no saturar el target (agregar delays)
9. **JWT siempre sospechoso** — verificar alg, exp, kid, jku
10. **Documentar findings** — capturar request, response, y evidencia
