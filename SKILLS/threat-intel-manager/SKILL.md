---
name: threat-intel-manager
description: Use when gathering, processing, or analyzing threat intelligence — MISP, STIX/TAXII feeds, IOC management, OpenCTI, threat research workflows, and integration with OSINT/SIEM.
---

# threat-intel-manager

Guía de threat intelligence para CSIRT y blue team. Cubre recolección, procesamiento y operacionalización de inteligencia de amenazas.

## Contexto del usuario

- **Rol:** CSIRT / Blue Team
- **Plataformas:** MISP (local o cloud), OpenCTI (opcional)
- **Formatos:** STIX 2.1, TAXII, OpenIOC, YARA
- **Integraciones:** OSINT (ver `argos`), SIEM, logs (ver `apolo`)
- **Feeds:** AlienVault OTX, VirusTotal, AbuseIPDB, FeodoTracker, URLhaus

---

## 1. MISP — Threat Intelligence Platform

### Setup básico (Docker)
```bash
# Usando docker-compose de MISP
git clone https://github.com/MISP/misp-docker.git
cd misp-docker
cp template.env .env
# Editar .env: MYSQL_ROOT_PASSWORD, MISP_ADMIN_EMAIL, MISP_BASEURL
docker compose up -d
```

### Consultas CLI
```bash
# Autenticación (API key desde la UI)
export MISP_URL="https://misp.local"
export MISP_KEY="your-api-key"

# Buscar eventos
misp-search -q "ransomware"
misp-search -q "APT29" --date-from 2026-01-01

# Buscar IOCs
misp-search -i 185.220.101.14
misp-search -i "evil.exe" --type filename

# Listar eventos recientes
misp-events --limit 10

# Publicar evento
misp-event-publish <event-id>

# Exportar en STIX 2
misp-export-stix2 --event <event-id> > evento-stix2.json
```

### PyMISP — Automatización
```python
from pymisp import ExpandedPyMISP
import warnings
warnings.filterwarnings("ignore")

misp_url = "https://misp.local"
misp_key = "your-api-key"
misp = ExpandedPyMISP(misp_url, misp_key, ssl=False)

# Buscar eventos por tag
events = misp.search_index(tags=["tlp:amber"])
for event in events:
    print(f"[{event['id']}] {event['info']} - {event['date']}")

# Crear evento
event = misp.new_event(
    info="Indicadores de campaña X",
    distribution=1,  # 0: Org, 1: Community
    threat_level_id=2,
    analysis=1
)

# Agregar IOC
attr = misp.add_attribute(
    event_id=event["Event"]["id"],
    type="ip-dst",
    value="185.220.101.14",
    category="Network activity",
    comment="C2 server"
)

# Publicar
misp.publish(event["Event"]["id"])
```

---

## 2. STIX 2.1 — Structured Threat Information Expression

### Conceptos clave
```
STIX Domain Objects (SDOs):
  - Indicator: Patrón de IOC observable
  - Attack Pattern: TTP (técnica MITRE ATT&CK)
  - Threat Actor: Actor de amenaza (APT, grupo criminal)
  - Campaign: Campaña específica
  - Malware: Familia de malware
  - Tool: Herramienta usada en ataque
  - Vulnerability: CVE
  - Report: Reporte de inteligencia
  - Identity: Identidad del reportante

STIX Cyber-observable Objects (SCOs):
  - ipv4-addr, domain-name, url, file, email-message
  - process, network-traffic, windows-registry-key

Relationship Objects (SROs):
  - Relationship: indicated-by, targets, uses
  - Sighting: avistamiento de un indicador
```

### Procesar STIX con Python
```python
from stix2 import MemoryStore, Filter
import json

# Cargar bundle STIX
with open("evento-stix2.json") as f:
    bundle_data = json.load(f)

src = MemoryStore(bundle_data)

# Listar todos los indicators
indicators = src.query([Filter("type", "=", "indicator")])
print(f"Indicadores: {len(indicators)}")
for ind in indicators:
    print(f"  [{ind.pattern_type}] {ind.pattern}")

# Filtrar por threat actor
actor_iocs = src.query([
    Filter("type", "=", "indicator"),
    Filter("pattern", "contains", "185.220.101")
])

# Obtener relaciones
for rel in src.query([Filter("type", "=", "relationship")]):
    print(f"{rel.source_ref} -> {rel.relationship_type} -> {rel.target_ref}")
```

### TAXII Client
```bash
# Conectar a servidor TAXII
taxii-clients -s https://taxii.server.com/taxii2/
taxii-client -u <user> -p <pass> -s <server> get collections
taxii-client -u <user> -p <pass> -s <server> get objects --collection <id>
```

---

## 3. Feeds de Threat Intel

### Fuentes públicas gratuitas
```bash
# AlienVault OTX (API key requerida)
curl -s -H "X-OTX-API-KEY: <key>" \
  https://otx.alienvault.com/api/v1/indicators/IPv4/185.220.101.14/general | jq .

# AbuseIPDB
curl -s -G https://api.abuseipdb.com/api/v2/check \
  --data-urlencode "ipAddress=185.220.101.14" \
  -H "Key: <api-key>" -H "Accept: application/json" | jq .

# URLhaus (público, sin key)
curl -s https://urlhaus.abuse.ch/downloads/csv_recent/ | head -20

# FeodoTracker (C2 feeds)
curl -s https://feodotracker.abuse.ch/downloads/ipblocklist.csv

# VirusTotal (API key)
curl -s -H "x-apikey: <key>" \
  https://www.virustotal.com/api/v3/ip_addresses/185.220.101.14 | jq .
```

### Automatizar recolección
```bash
# Script simple para consolidar feeds
#!/bin/bash
# save as ~/scripts/intel-feeds.sh
OUTDIR="$HOME/threat-intel/feeds"
DATE=$(date +%Y%m%d)

mkdir -p $OUTDIR/$DATE

# AbuseIPDB
curl -s -G https://api.abuseipdb.com/api/v2/blacklist \
  -d "confidenceMinimum=90" \
  -H "Key: <key>" > $OUTDIR/$DATE/abuseipdb.json

# URLhaus
curl -s https://urlhaus.abuse.ch/downloads/csv_recent/ > $OUTDIR/$DATE/urlhaus.csv

# FeodoTracker
curl -s https://feodotracker.abuse.ch/downloads/ipblocklist.csv > $OUTDIR/$DATE/feodo.csv
```

---

## 4. MITRE ATT&CK Framework

```bash
# Navegar MITRE ATT&CK
# Web: https://attack.mitre.org
# API pública: https://attack.mitre.org/api/

# Obtener técnicas via API
curl -s https://attack.mitre.org/api/techniques | jq '.techniques[] | {id: .id, name: .name}'

# Buscar técnicas por grupo
curl -s https://attack.mitre.org/api/groups/G0016 | jq '.techniques[] | .name'

# ATT&CK Navigator (capa JSON)
cat > /tmp/attack-layer.json << 'EOF'
{
  "name": "Capa personalizada",
  "techniques": [
    {"techniqueID": "T1059", "score": 1, "comment": "Command and Scripting Interpreter"},
    {"techniqueID": "T1566", "score": 1, "comment": "Phishing"}
  ],
  "gradient": {"colors": ["#ffe766", "#ff6666"]}
}
EOF
```

### Integración con MISP
```bash
# MISP ya tiene galaxy MITRE ATT&CK integrada
misp-galaxies --name mitre-attack-pattern
misp-galaxies --name mitre-threat-actor

# Taggear evento con técnica
misp-tag --event <id> --tag "misp-galaxy:mitre-attack-pattern=\"T1059.001 - PowerShell\""
```

---

## 5. IOC Management

### Clasificación de IOCs
```yaml
# ioc-template.yaml
ioc:
  - value: "185.220.101.14"
    type: "ip-dst"
    category: "network"
    confidence: 85
    tags: ["c2", "emotet"]
    source: "feodo-tracker"
    first_seen: "2026-06-01"
    
  - value: "evil.example.com"
    type: "domain"
    category: "network"
    confidence: 70
    tags: ["phishing", "credential-theft"]
    
  - value: "a"*64
    type: "sha256"
    category: "file"
    tags: ["malware", "emotet"]
    file_name: "invoice.pdf.exe"
```

### Convertir entre formatos
```bash
# MISP events → STIX
misp-export-stix2 --event 123 > event.stix2

# OpenIOC → MISP
# Usar la UI de MISP o pyMISP

# CSV → MISP (via script)
python3 -c "
from pymisp import ExpandedPyMISP
misp = ExpandedPyMISP('url', 'key')
# Leer CSV, crear attributes
"

# YARA → IOC
# Las reglas YARA son indicadores en sí mismas
```

### Enriquecimiento de IOCs
```bash
# Reverse DNS
dig +short -x 185.220.101.14

# WHOIS
whois 185.220.101.14 | grep -E 'OrgName|NetName|Country|descr'

# SSL Certificate (si es web)
echo | openssl s_client -connect evil.example.com:443 2>/dev/null | openssl x509 -noout -subject -issuer -dates

# VirusTotal
curl -s -H "x-apikey: <key>" \
  "https://www.virustotal.com/api/v3/search?query=185.220.101.14" | jq '.data[].attributes.last_analysis_stats'
```

---

## 6. OpenCTI — Open Cyber Threat Intelligence

```bash
# Setup con Docker
git clone https://github.com/OpenCTI-Platform/docker.git
cd docker
docker compose up -d
# Acceder: http://localhost:8080
# Default: admin@opencti.io / admin

# CLI via API
export OPENCTI_URL="http://localhost:8080"
export OPENCTI_TOKEN="<api-token>"

# Consultar entidades
curl -s -H "Authorization: Bearer $OPENCTI_TOKEN" \
  -H "Content-Type: application/json" \
  -X POST "$OPENCTI_URL/graphql" \
  -d '{"query": "{ stixCoreObjects(first: 10) { edges { node { ... on StixObject { id entity_type } } } } }"}'
```

---

## 7. Integración con SIEM (Sigma Rules)

Sigma es el puente entre threat intel y detección en SIEM.

```yaml
title: Deteccion de C2 Emotet
id: sigma-c2-emotet-001
status: experimental
description: Detecta conexiones a servidores C2 de Emotet
references:
  - https://feodotracker.abuse.ch/
author: lcampassi
date: 2026-06
tags:
  - attack.command_and_control
  - attack.t1071
logsource:
  category: network_connection
  product: windows
detection:
  selection:
    DestinationIp:
      - "185.220.101.14"
      - "45.33.32.156"
  condition: selection
falsepositives:
  - Cambio de IP legítimo
level: high
```

```bash
# Convertir Sigma a formato SIEM
sigma convert -t splunk -p splunk-windows sigma-rule.yml
sigma convert -t elastalert -p default sigma-rule.yml
sigma convert -t qradar sigma-rule.yml
```

---

## 8. Flujo de trabajo CSIRT

```
1. RECOLECCIÓN
   ├── Feeds automáticos (AbuseIPDB, URLhaus, Feodo)
   ├── OSINT (argos)
   ├── Comunidad (MISP sharing groups)
   └── Análisis propio (hecate)

2. PROCESAMIENTO
   ├── Validar IOCs (falsos positivos)
   ├── Enriquecer (WHOIS, DNS, VirusTotal)
   ├── Clasificar (tipo, severidad, TLP)
   └── Estructurar (STIX, MISP event)

3. DETECCIÓN
   ├── Crear reglas Sigma
   ├── Configurar SIEM
   ├── IOC feeds en firewall/IDS
   └── YARA rules para análisis

4. RESPUESTA
   ├── Alertas a equipo CSIRT
   ├── Búsqueda de compromiso (hunting)
   ├── Contención (bloqueo en firewall/DNS)
   └── Documentar en Obsidian
```

---

## 9. Buenas prácticas

1. **TLP siempre** — clasificar con Traffic Light Protocol (RED, AMBER, GREEN, WHITE)
2. **Fuentes primarias** — verificar IOCs contra múltiples fuentes antes de operacionalizar
3. **Falsos positivos** — documentar y compartir en comunidad
4. **Automatizar** — la recolección debe ser automática, el análisis humano
5. **Operacionalizar** — un IOC no es útil hasta que está en una regla de detección
6. **Preservar evidencia** — screenshots, PCAPs, hashes originales
7. **NO compartir TLP:RED** — fuera del equipo, el que filtra pierde la fuente
8. **MITRE ATT&CK** — mapear IOCs a técnicas para entender el panorama
9. **Feedback loop** — incidentes nuevos retroalimentan las reglas de detección
10. **Documentar en Obsidian** — cada investigación deja un reporte
