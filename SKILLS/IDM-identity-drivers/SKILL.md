---
name: IDM-identity-drivers
description: >
  Use when working with IDM drivers — Active Directory, API Rest, LDAP, Remote Loader,
  policies, filters, XPATH nouns, shim configuration, driver health, traces.
  Cross-platform (Linux + Windows).
---

# IDM-identity-drivers

Contexto sobre **Drivers de Identity Manager**.

## Ubicación de la documentación en el vault

| Área | Ruta (via env var) |
|------|-------------------|
| IDM Drivers | `$BABILONIA_IDM/05-DRIVERS/` |

## Documentación disponible

### Active Directory
- `Instalacion y configuracion Remote Loader NetIQ Identity Manager 4.8.6.md`
  - Instalación de Remote Loader 64 bits y .NET
  - Configuración de servicio: puertos, claves de cifrado, credenciales
  - Vinculación del driver de AD con Remote Loader
  - Validación de checksums, apertura de puertos (8064, 636)
  - Generación y exportación de certificados autogenerados

### APIs
- `Entendiendo el driver de API Rest.md` — Conceptos: autenticación (Anónima, Básica, OAuth2.0), métodos HTTP (GET, POST, PUT, PATCH, DELETE), formato XML/JSON
- `Metodos de llamada de APIs.md` — Métodos concretos para REST desde IDM

### XPATH
- `XPATH nouns para drivers.md` — Referencia de XPATH nouns en policies de drivers

## Conceptos clave

### Tipos de drivers documentados
- **AD**: sincronización IDM↔AD vía Remote Loader (puerto 8064)
- **API Rest**: driver genérico para servicios RESTful. CRUD + sync de contraseñas
- **LDAP**: drivers para directorios LDAP (eDirectory, OpenLDAP, etc.)

### Remote Loader
- Componente intermedio para drivers fuera del servidor IDM
- Comunicación cifrada entre IDM y Remote Loader
- Puertos típicos: 8060-8069
- Instalación en Windows Server con .NET Framework

### Policies
- Reglas de transformación de eventos en canales Publisher/Subscriber
- Configuración en Designer usando XPATH
