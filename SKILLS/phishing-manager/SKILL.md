# Phishing Manager — Análisis y Respuesta ante Phishing

## Descripción General

El phishing sigue siendo el vector de ataque inicial más común en incidentes de seguridad. Como CSIRT, recibir reportes de phishing es parte del día a día. Este skill proporciona un flujo de trabajo completo para analizar, contener y documentar campañas de phishing.

**Objetivo:** Estandarizar el análisis de phishing desde la recepción del reporte hasta la generación de indicadores de compromiso (IOCs) y la documentación final en el vault de Obsidian.

**Flujo general:**
1. Recepción y triage del reporte
2. Extracción y análisis de cabeceras email
3. Análisis de URLs y redirecciones
4. Análisis de attachments (documentos, PDFs, scripts)
5. Extracción de IOCs
6. Búsqueda de inteligencia (Threat Intelligence)
7. Contención (bloqueo a nivel gateway/endpoint)
8. Documentación y reporting

**Perfil:** Lucciano Campassi (D4rkDr4g0n) — CSIRT Professional, Arch Linux + Windows 11.

---

## Análisis de Headers Email

Las cabeceras email contienen información crítica: origen real del mensaje, servidores intermedios, autenticación email, y posibles suplantaciones.

### Extracción de cabeceras

Desde el cliente email, exportar el mensaje como `.eml` o `.msg`. Los headers completos se ven con "Mostrar original" (Gmail), "View source" (Outlook Web), o "Message → Raw source" (Thunderbird).

### Verificación SPF (Sender Policy Framework)

SPF verifica que el servidor remitente esté autorizado a enviar correo para el dominio.

**Linux (dig):**

```bash
# Consultar registro SPF del dominio
dig TXT dominio-sospechoso.com +short

# Consulta específica SPF
nslookup -type=TXT dominio-sospechoso.com

# Python3 oneliner
python3 -c "import dns.resolver; print(dns.resolver.resolve('dominio-sospechoso.com', 'TXT').response)"
```

**Windows (PowerShell):**

```powershell
# SPF lookup con Resolve-DnsName
Resolve-DnsName dominio-sospechoso.com -Type TXT | Where-Object {$_.Strings -match "v=spf1"}
```

Interpretar el resultado: `v=spf1 include:_spf.google.com ~all` significa que Google está autorizado y el resto es softfail (`~all`). Si el header muestra `Received-SPF: fail`, el correo no pasó la verificación.

### Verificación DKIM (DomainKeys Identified Mail)

DKIM usa una firma criptográfica en el header del mensaje.

**Linux:**

```bash
# Extraer dominio del header DKIM-Signature
grep -i "dkim-signature" email.eml

# Obtener la clave pública DKIM
dig selector._domainkey.dominio-sospechoso.com TXT +short

# Verificar con python3
python3 -c "
import dkim
with open('email.eml', 'rb') as f:
    msg = f.read()
result = dkim.verify(msg)
print('DKIM válido' if result else 'DKIM inválido')
"
```

**Windows:**

```powershell
Resolve-DnsName "selector._domainkey.dominio-sospechoso.com" -Type TXT
```

### Verificación DMARC (Domain-based Message Authentication, Reporting & Conformance)

DMARC indica qué hacer si SPF y/o DKIM fallan.

**Linux:**

```bash
dig TXT _dmarc.dominio-sospechoso.com +short
```

**Windows:**

```powershell
Resolve-DnsName "_dmarc.dominio-sospechoso.com" -Type TXT
```

Política DMARC: `v=DMARC1; p=reject; sp=reject; pct=100;` — `p=reject` es lo más estricto, `p=quarantine` envía a spam, `p=none` solo monitoreo.

### Análisis de Received Headers

Los headers `Received:` se leen de abajo hacia arriba. El último `Received` es el origen real.

```bash
# Extraer todos los Received headers
grep -a "^Received:" email.eml

# Ver saltos de protocolo (HTTP vs SMTP, tls vs plaintext)
grep -a "with" email.eml | grep -i "received"
```

Señales de alerta:
- Discrepancia entre el `From:` visible y el `Return-Path:` / `Envelope-From`
- Múltiples saltos inusuales o geografías inconsistentes
- Headers `Reply-To:` diferente al `From:`
- Cabeceras `Message-ID:` con formato extraño o faltante

### Herramienta completa con Python

```bash
#!/usr/bin/env python3
# analyze_headers.py
import sys
import dns.resolver
from email import policy
from email.parser import BytesParser

with open(sys.argv[1], 'rb') as f:
    msg = BytesParser(policy=policy.default).parse(f)

print(f"From: {msg['From']}")
print(f"Reply-To: {msg['Reply-To']}")
print(f"Return-Path: {msg['Return-Path']}")
print(f"Message-ID: {msg['Message-ID']}")
print(f"Date: {msg['Date']}")
print(f"Subject: {msg['Subject']}")

domain = msg['From'].split('@')[-1].rstrip('>')
try:
    spf = dns.resolver.resolve(domain, 'TXT')
    for r in spf:
        if 'v=spf1' in str(r):
            print(f"SPF: {r}")
except: print("SPF: No encontrado")
```

---

## Análisis de URLs

Las URLs son el componente central del phishing. El análisis debe determinar el destino final, la infraestructura utilizada y si el sitio es malicioso.

### Extracción de URLs del email

**Linux:**

```bash
# Extraer todas las URLs del email
grep -a -oP '(https?://[^\s<>"]+|hxxp[s]?://[^\s<>"]+)' email.eml

# Convertir hxxp:// a http:// (formato defanged)
sed 's/hxxp/http/g' email.eml | grep -a -oP 'https?://[^\s<>"]+'

# Con Python (maneja HTML y texto)
python3 -c "
import re
with open('email.eml', 'r', errors='ignore') as f:
    content = f.read()
urls = re.findall(r'https?://[^\s<>\"\']+', content)
for u in urls: print(u)
"
```

### Análisis de cadena de redirecciones

```bash
# Seguir redirecciones (máximo 10 saltos)
curl -Ls -o /dev/null -w "%{url_effective}\n" "https://url-sospechosa.com"

# Ver toda la cadena con códigos de estado
curl -LI "https://url-sospechosa.com" 2>/dev/null | grep -E "^(HTTP|Location)"
```

**Windows (PowerShell):**

```powershell
# Seguir redirecciones con PowerShell
$req = [System.Net.HttpWebRequest]::Create("https://url-sospechosa.com")
$req.AllowAutoRedirect = $true
$req.Method = "HEAD"
try { $resp = $req.GetResponse(); $resp.ResponseUri.AbsoluteUri } catch { $_ }
```

### URLScan.io

```bash
# Consultar un dominio en URLScan.io via API
curl -s "https://urlscan.io/api/v1/search/?q=domain:dominio-sospechoso.com" | jq '.results[:5] | .[] | {url, page, task}'

# Submit una URL para análisis
curl -s -X POST "https://urlscan.io/api/v1/scan/" \
  -H "Content-Type: application/json" \
  -H "API-Key: $URLSCAN_API_KEY" \
  -d '{"url": "https://url-sospechosa.com", "visibility": "public"}' | jq .
```

### VirusTotal

```bash
# Consultar URL en VirusTotal
curl -s "https://www.virustotal.com/api/v3/urls/$(echo -n 'https://url-sospechosa.com' | base64 -w0 | sed 's/+/-/g;s/\//_/g' | tr -d '=')" \
  -H "x-apikey: $VT_API_KEY" | jq '.data.attributes.last_analysis_stats'
```

### Detección de phishing en dominios

**Técnicas de typosquatting:**

```bash
# Detectar homógrafos Unicode/Punycode
# Convertir un dominio a punycode
python3 -c "
import re
domain = 'xn--e1awg7d.com'  # ejemplo
if domain.startswith('xn--'):
    print(domain.encode('ascii').decode('idna'))
"

# Comparar similitud visual con dominios legítimos
python3 -c "
from Levenshtein import ratio
dominio_legitimo = 'google.com'
sospechoso = 'goog1e.com'
print(f'Similitud: {ratio(dominio_legitimo, sospechoso):.2%}')
"
```

**WHOIS y creación reciente:**

```bash
# Verificar fecha de creación del dominio
whois dominio-sospechoso.com | grep -i "creation date"

# Ver nameservers y registrante
whois dominio-sospechoso.com | grep -iE "name server|registrant|org|admin"
```

**Windows:**

```powershell
whois.exe dominio-sospechoso.com | Select-String "Creation Date"
```

### Verificación de reputación

```bash
# AbuseIPDB
curl -s "https://api.abuseipdb.com/api/v2/check?ipAddress=1.2.3.4" \
  -H "Key: $ABUSEIPDB_API_KEY" \
  -H "Accept: application/json" | jq .

# ThreatMeter (OTX)
curl -s "https://otx.alienvault.com/api/v1/indicators/domain/dominio-sospechoso.com/general" \
  -H "X-OTX-API-Key: $OTX_API_KEY" | jq .
```

### Captura de pantalla del sitio

```bash
# Con playwright (Linux)
python3 -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('https://url-sospechosa.com')
    page.screenshot(path='phishing_screenshot.png')
    browser.close()
"
```

---

## Análisis de Attachments

Los attachments son el mecanismo de entrega más común para malware. El análisis debe ser seguro (nunca abrir en el host productivo, siempre en sandbox o máquina aislada).

### Análisis de Documentos Office (OLE2 / OOXML)

**Linux (oletools):**

```bash
# Identificar tipo de documento OLE
oleid documento.doc

# Extraer y analizar macros (VBA)
olevba documento.doc

# Buscar URLs dentro del documento
olevba -c documento.doc | grep -oP 'https?://[^\s<>"\']+' > urls_doc.txt

# Extraer objetos OLE embebidos
oleobj documento.doc

# Analisis de relaciones OOXML (docx, xlsx, pptx)
python3 -c "
from oletools.olevba import VBA_Parser
vbaparser = VBA_Parser('documento.doc')
if vbaparser.detect_macros():
    print('Macros detectadas!')
    for (filename, stream_path, vba_filename, vba_code) in vbaparser.extract_macros():
        print(f'Macro en: {stream_path}')
        print(vba_code[:500])
"
```

**Análisis de DDE (Dynamic Data Exchange):**

```bash
# Detectar campos DDE en documentos
python3 -c "
import olefile
ole = olefile.OleFileIO('documento.doc')
if ole.exists('WordDocument'):
    data = ole.openstream('WordDocument').read()
    if b'DDE' in data or b'DDEAUTO' in data:
        print('Posible DDE detectado!')
"
```

### Análisis de PDFs

**Linux (pdfid, pdf-parser de Didier Stevens):**

```bash
# Identificar objetos y filtros en PDF
pdfid.py documento.pdf

# Extraer objetos que ejecutan JavaScript
pdf-parser.py --search=JavaScript documento.pdf

# Analizar URLs en el PDF
pdf-parser.py --search=URI documento.pdf

# Extraer objetos que contienen /OpenAction (ejecución automática)
pdf-parser.py --type=/OpenAction documento.pdf

# Obtener estadísticas completas
pdfid.py --json documento.pdf | jq .
```

**Windows (herramientas similares):**

```powershell
# Usar pdfid desde PowerShell
python3 "$env:USERPROFILE\Tools\pdfid.py" documento.pdf

# Ver propiedades del PDF (PowerShell nativo)
$shell = New-Object -ComObject Shell.Application
$folder = $shell.Namespace((Get-Item "documento.pdf").DirectoryName)
$file = $folder.ParseName((Get-Item "documento.pdf").Name)
0..300 | ForEach-Object { $prop = $folder.GetDetailsOf($file, $_); if ($prop) { "$_ : $prop" } }
```

### Envío a Sandbox

**Configuración local (Cuckoo/CAPE):**

```bash
# Enviar sample a CAPE sandbox
curl -F "file=@malware.doc" -F "timeout=120" http://sandbox.local:8090/tasks/create/file/ | jq .

# Ver estado de la tarea
curl -s http://sandbox.local:8090/tasks/view/12345/ | jq '.task.status'
```

**Joe Sandbox / Any.Run:**

```bash
# Joe Sandbox API
curl -F "file=@sample.doc" -F "environment=windows-10" \
  -H "api-key: $JOE_API_KEY" \
  "https://jbxcloud.joesecurity.org/api/v2/analysis/submit"

# Any.Run (requiere API key)
curl -s -X POST "https://api.any.run/v1/analysis" \
  -H "Authorization: Bearer $ANYRUN_API_KEY" \
  -F "file=@sample.doc" \
  -F "env=win10" | jq .
```

### Análisis de scripts (JS, VBS, PowerShell)

**Linux:**

```bash
# Analizar JavaScript ofuscado con Extract-JS
python3 -c "
import re
with open('script.js', 'r') as f:
    code = f.read()

# Detectar eval(), document.write(), String.fromCharCode
if 'eval(' in code: print('eval detectado - posible ofuscación')
if 'fromCharCode' in code: print('fromCharCode detectado - posible ofuscación')

# Extraer strings
strings = re.findall(r'\"([^\"]{8,})\"', code)
for s in strings[:20]:
    if any(c in s for c in 'https://.'):
        print(f'URL potencial: {s}')
"

# Decodificar base64
python3 -c "
import base64, re
with open('script.ps1', 'r') as f:
    code = f.read()
b64 = re.search(r'[A-Za-z0-9+/=]{50,}', code)
if b64:
    dec = base64.b64decode(b64.group()).decode('utf-16-le', errors='ignore')
    print(dec[:1000])
"
```

---

## Extracción de Indicadores (IOCs)

Consolidar todos los indicadores encontrados en formato estructurado.

### Extracción automatizada

```bash
#!/usr/bin/env bash
# extract_iocs.sh — Extraer IOCs de un email de phishing
EML="$1"
echo "=== IOCS ===" > iocs.txt

# IPs
grep -aoP '\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b' "$EML" | sort -u >> iocs.txt

# Dominios
grep -aoP '(?<!//)([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(?![a-zA-Z])' "$EML" | sort -u >> iocs.txt

# URLs
grep -aoP 'https?://[^\s<>"\']+' "$EML" | sort -u >> iocs.txt

# Hashes (MD5, SHA1, SHA256)
grep -aoP '\b[A-Fa-f0-9]{32}\b' "$EML" | sort -u >> iocs.txt
grep -aoP '\b[A-Fa-f0-9]{40}\b' "$EML" | sort -u >> iocs.txt
grep -aoP '\b[A-Fa-f0-9]{64}\b' "$EML" | sort -u >> iocs.txt

# Emails
grep -aoP '\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b' "$EML" | sort -u >> iocs.txt

echo "IOCs extraídos en iocs.txt"
```

### Formato MISP/STIX (Python)

```python
#!/usr/bin/env python3
# generar_misp_event.py
from pymisp import MISPEvent, PyMISP, MISPAttribute
import json

event = MISPEvent()
event.info = "Phishing campaign - Banco Falso"
event.add_attribute('url', 'https://phishing.evil.com/login')
event.add_attribute('domain', 'phishing.evil.com')
event.add_attribute('ip-dst', '192.168.1.100')
event.add_attribute('email-src', 'phisher@evil.com')
event.add_attribute('filename', 'factura.doc')
event.add_attribute('md5', 'd41d8cd98f00b204e9800998ecf8427e')

with open('misp_event.json', 'w') as f:
    json.dump(event.to_json(), f, indent=2)
```

### Reglas YARA

```yara
rule Phishing_Attachment_Generic
{
    meta:
        description = "Regla genérica para attachments de phishing"
        author = "D4rkDr4g0n"
        date = "2026-06-05"
    strings:
        $url1 = "https://" ascii wide
        $url2 = "http://" ascii wide
        $macro = "Sub AutoOpen" ascii wide
        $macro2 = "Private Sub" ascii wide
        $dde = "DDEAUTO" ascii wide
        $js = "function" ascii wide
        $payload = "PowerShell" ascii wide
    condition:
        (2 of ($url*)) or ($macro or $macro2) or $dde or $js
}
```

---

## Playbooks de Respuesta

### Triage Inicial

| Prioridad | Criterio | Acción |
|-----------|----------|--------|
| **P1** | Credenciales de ejecutivos/C-level comprometidas | Bloqueo inmediato, reset credenciales, notificar CISO |
| **P2** | Phishing dirigido (spear-phishing) con attachment | Análisis forense del attachment, bloqueo en gateway |
| **P3** | Campaña masiva genérica | Bloquear URLs/dominios, alertar usuarios |
| **P4** | Phishing reportado por usuario, no malicioso | Cerrar reporte, documentar, feedback al usuario |

### Flujo de Contención

1. **Verificar si el usuario hizo clic o ingresó credenciales**
   - Revisar logs de proxy/DNS para conexiones al dominio malicioso
   - Verificar autenticaciones exitosas desde IPs sospechosas (Azure AD / AD logs)
   - Si hay credenciales comprometidas: forzar reseteo y revocar sesiones activas

2. **Bloqueo a nivel de gateway email**
   - Agregar dominio remitente/IP a blocklist del mail gateway
   - Crear regla de contenido para el asunto/remitente
   - Marcar todos los mensajes similares como spam

3. **Bloqueo a nivel de DNS/Proxy**
   ```bash
   # Agregar dominio a bloqueo en Pi-hole / DNS sinkhole
   echo "0.0.0.0 dominio-falso.com" >> /etc/pihole/domains.txt
   pihole restartdns

   # Bloquear IP en firewall (iptables/nftables)
   sudo iptables -A FORWARD -d 1.2.3.4 -j DROP
   ```

4. **Bloqueo en endpoints (Windows)**
   ```powershell
   # Agregar dominio a hosts file
   Add-Content -Path "$env:SystemRoot\System32\drivers\etc\hosts" -Value "0.0.0.0 dominio-falso.com"

   # Bloquear IP en firewall de Windows
   netsh advfirewall firewall add rule name="Block Phishing IP" dir=out remoteip=1.2.3.4 action=block
   ```

5. **Aislar el equipo comprometido (si aplica)**
   - Desconectar de la red (VLAN de cuarentena)
   - Tomar imagen forense del disco (FTK Imager / dd)
   - Recolectar volátil (RAM) antes de apagar

### Notificación a Usuarios

Template para comunicación corporativa:

```
Subject: [ALERTA] Reporte de phishing recibido

Hola [Nombre],

Hemos recibido tu reporte de phishing (Ticket #XXXXX).
Nuestro equipo ya está analizando el mensaje.

**¿Qué debes hacer?**
- No reenviar el mensaje a otros compañeros
- Si hiciste clic en algún enlace, notifícanos inmediatamente
- Si ingresaste tus credenciales, cámbialas ahora mismo

Gracias por tu colaboración.
— CSIRT
```

### Reporte Interno

```markdown
# Reporte de Phishing — [TICKET-XXXXX]

## Resumen
- **Fecha/hora reporte:** 2026-06-05 14:30 UTC
- **Reportado por:** usuario@empresa.com
- **Clasificación:** Spear-phishing (P2)
- **Vector inicial:** Email con attachment malicioso

## Detalles del Email
- **Remitente (From):** soporte@banco-falso.com
- **Reply-To:** fraud@evil.com
- **Asunto:** "Factura pendiente de pago — acción requerida"
- **Message-ID:** <abc123@mx.evil.com>
- **SPF:** Fail | **DKIM:** No firmado | **DMARC:** None

## Indicadores (IOCs)
- Dominio: banco-falso.com (creado 2026-05-01, WHOIS oculto)
- URL: https://banco-falso.com/login?token=abc123
- IP destino: 203.0.113.45 (AS3266 — Hosting en Rusia)
- Attachment: factura.doc (MD5: d41d8cd98f00b204e9800998ecf8427e)
- Payload: AgentTesla (detectado en sandbox)

## Acciones Tomadas
- [x] Bloqueo de dominio en gateway email
- [x] Bloqueo de IP en firewall perimetral
- [x] Regla YARA desplegada en EDR
- [x] Usuario notificado y credenciales reseteadas
- [ ] Reporte a CERT/CSIRT externo

## Timeline
| Hora | Acción |
|------|--------|
| 14:30 | Usuario reporta phishing |
| 14:35 | Triage inicial — clasificado P2 |
| 14:45 | Análisis de headers — SPF fail |
| 15:00 | Extracción de IOCs y bloqueo |
| 15:30 | Análisis en sandbox — payload confirmado |
| 16:00 | Documentación y cierre |
```

---

## Herramientas por Plataforma

### Tabla Comparativa

| Función | Linux | Windows |
|---------|-------|---------|
| **DNS Lookups** | `dig`, `nslookup` | `Resolve-DnsName`, `nslookup.exe` |
| **WHOIS** | `whois` | `whois.exe` (SysInternals) |
| **SPF/DKIM/DMARC** | Python + `dnspython` | Python + `dnspython` |
| **Análisis PDF** | `pdfid.py`, `pdf-parser.py` | `pdfid.py`, `pdf-parser.py` |
| **Análisis Office** | `oletools` (oleid, olevba) | `oletools` (Python) |
| **Seguimiento URLs** | `curl -LI` | `curl.exe`, PowerShell |
| **URLScan.io** | `curl` + API | `curl.exe`, PowerShell |
| **VirusTotal** | `curl` + API | `curl.exe`, PowerShell |
| **Sandbox** | CAPE/Cuckoo (local), pyattck | Any.Run, Joe Sandbox |
| **Captura web** | Playwright/selenium | Playwright/selenium |
| **YARA** | `yara`, `yarac` | `yara.exe`, `yarac.exe` |
| **Análisis de red** | `tcpdump`, `tshark`, `zeek` | Wireshark, `netsh trace` |
| **Forensia** | `dd`, `guymager`, `sleuthkit` | FTK Imager, KAPE |
| **Threat Intel** | MISP, OpenCTI | MISP, OpenCTI |
| **Scripting** | Bash + Python3 | PowerShell + Python3 |

### Comandos de instalación

**Arch Linux (yay/paru):**

```bash
yay -S oletools pdfid pdf-parser yara python-dnspython python-playwright
pip install pymisp
```

**Windows (Chocolatey/Winget):**

```powershell
choco install oletools pdfid pdf-parser yara python3
pip install dnspython pymisp playwright
```

---

## Documentación en Vault (Obsidian)

Las notas de análisis de phishing se almacenan en el vault Personal-Vault de Obsidian.

### Rutas (Linux — Arch)

```
~/Personal-Vault/CSIRT/Phishing/
├── Campañas/
│   └── YYYY-MM-DD_Campana_BancoX.md
├── Analisis/
│   ├── YYYY-MM-DD_Analisis_Headers_EmailX.md
│   └── YYYY-MM-DD_Analisis_URL_DominioX.md
├── IOCs/
│   └── YYYY-MM-DD_IOCs_CampanaX.md
└── Reportes/
    └── YYYY-MM-DD_Reporte_CampanaX.md
```

### Rutas (Windows 11)

```
D:\Personal-Vault\CSIRT\Phishing\
├── Campañas\
├── Analisis\
├── IOCs\
└── Reportes\
```

### Template de nota rápida (Obsidian)

```markdown
---
tags: [phishing, csirt, analysis]
date: {{date}}
ticket: XXXXX
severity: P2
status: open
---

# Phishing — {{title}}

## Remitente
`{{from}}` → SPF: {{spf_result}} | DKIM: {{dkim_result}} | DMARC: {{dmarc_result}}

## Asunto
`{{subject}}`

## URLs detectadas
- [ ] {{url1}}
- [ ] {{url2}}

## IOCs extraídos
- Dominios::
- IPs::
- Hashes::

## Acciones tomadas
- [ ] Bloqueo gateway
- [ ] Bloqueo DNS
- [ ] Análisis sandbox
- [ ] Reporte al usuario

## Playbook utilizado
[[Phishing Response Playbook]]

## Notas adicionales
...
```

### Automatización desde terminal

```bash
# Crear nota de phishing desde CLI (requiere obsidian-advanced-uri plugin)
curl -G "obsidian://advanced-uri?filepath=CSIRT/Phishing/Campañas/$(date +%Y-%m-%d)_Campana_Ejemplo.md"
```

---

## Buenas Prácticas

### Cadena de Custodia

1. **Preservar el email original**: Guardar el `.eml` o `.msg` completo, sin modificar. No reenviar el email (se alteran los headers).
2. **Hash del artefacto**: Calcular SHA256 del archivo original antes de cualquier manipulación.
   ```bash
   sha256sum email_original.eml > email_original.eml.sha256
   ```
3. **Documentar cada paso**: Fechas, horas, herramientas usadas, resultados. Todo debe ser reproducible.
4. **No trabajar sobre el original**: Hacer copias de trabajo. Preservar el original como evidencia.
5. **Registro de cambios**: Mantener un log de todas las acciones tomadas durante el análisis.
6. **Firma digital**: Si se requiere presentar como evidencia legal, firmar los reportes y los hashes.

### Evidencia Digital

- Almacenar en un volumen cifrado (LUKS en Linux, BitLocker en Windows)
- Backup en servidor forense con hash chain
- Metadata: quién recoleció, cuándo, dónde, con qué herramienta

### Reportes

- Seguir formato NIST 800-61 o el estándar de tu organización
- Incluir timeline completo de la respuesta
- Recomendaciones de mejora (lecciones aprendidas)
- Clasificar por nivel de criticidad
- Compartir IOCs con la comunidad (MISP, AlienVault OTX)

### Uso de Defanging

Siempre presentar indicadores en formato defanged para evitar clics accidentales:

| Original | Defanged |
|----------|----------|
| `https://evil.com` | `hxxps://evil[.]com` |
| `1.2.3.4` | `1[.]2[.]3[.]4` |
| `user@evil.com` | `user[@]evil[.]com` |
| `d41d8cd98f00b204e9800998ecf8427e` | `d41d8cd98f00b204e9800998ecf8427e` (hash no cambia) |

### Automatización del flujo

```bash
#!/usr/bin/env bash
# phishing_analyzer.sh — Pipeline automatizado de análisis
# Uso: ./phishing_analyzer.sh email.eml
EML="$1"
BASE=$(basename "$EML" .eml)
DIR="analisis_$BASE"

mkdir -p "$DIR"
cp "$EML" "$DIR/original.eml"
sha256sum "$EML" > "$DIR/hash.sha256"

echo "[*] Extrayendo headers..."
grep -a "^Received:\|^From:\|^Reply-To:\|^Return-Path:\|^Message-ID:\|^Date:" "$EML" > "$DIR/headers.txt"

echo "[*] Extrayendo URLs..."
grep -aoP '(https?://[^\s<>"\']+|hxxp[s]?://[^\s<>"\']+)' "$EML" > "$DIR/urls.txt"

echo "[*] Extrayendo IPs..."
grep -aoP '\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b' "$EML" > "$DIR/ips.txt"

echo "[*] Extrayendo dominios..."
grep -aoP '(?<!//)([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(?![a-zA-Z])' "$EML" > "$DIR/dominios.txt"

echo "[*] Análisis SPF/DKIM/DMARC..."
domain=$(grep -a "^From:" "$EML" | grep -oP '(?<=@)[^>]+')
if [ -n "$domain" ]; then
    dig TXT "$domain" +short > "$DIR/spf.txt" 2>/dev/null
    dig TXT "_dmarc.$domain" +short > "$DIR/dmarc.txt" 2>/dev/null
fi

echo "[+] Análisis completo. Resultados en: $DIR"
```

### Checklist de Verificación

- [ ] Headers autenticación verificados (SPF/DKIM/DMARC)
- [ ] Cadenas de Received headers analizadas
- [ ] URLs extraídas y analizadas (redirecciones + reputación)
- [ ] Attachments analizados en sandbox
- [ ] IOCs consolidados en formato MISP/CSV
- [ ] Bloqueos aplicados (gateway, DNS, firewall, EDR)
- [ ] Usuario notificado
- [ ] Credenciales reseteadas (si aplica)
- [ ] Reporte documentado en vault
- [ ] IOCs compartidos con comunidad (MISP/OTX)
- [ ] Lecciones aprendidas registradas
