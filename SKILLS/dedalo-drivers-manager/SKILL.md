---
name: dedalo-drivers-manager
description: >
  Use when working with IDM drivers — Active Directory, API Rest, LDAP, Remote Loader,
  policies, filters, XPATH nouns, shim configuration, driver health, traces.
  Cross-platform (Linux + Windows).
---

# dedalo-drivers-manager

Contexto sobre **Drivers de NetIQ Identity Manager**.

## Ubicación de la documentación en el vault

| Área | Linux | Windows |
|------|-------|---------|
| IDM Drivers | `/files/Personal-Vault/Manuales/04-SPECIALIZED-DOMAINS/01-IAM-IDENTITY/01-IDM/05-DRIVERS/` | `C:\Users\lcampassi\Proton Drive\D4rkDr4g0n19\My files\Personal-Vault\Manuales\04-SPECIALIZED-DOMAINS\01-IAM-IDENTITY\01-IDM\05-DRIVERS\` |

## Documentación disponible

### Active Directory
- `Instalacion y configuracion Remote Loader NetIQ Identity Manager 4.8.6.md`
  - Instalación de Remote Loader 64 bits y .NET
  - Configuración de servicio: puertos, claves de cifrado, credenciales
  - Vinculación del driver de AD con Remote Loader
  - Validación de checksums, apertura de puertos (8064, 636)
  - Generación y exportación de certificados autogenerados

### APIs
- `Entendiendo el driver de API Rest.md` — Conceptos del driver REST: autenticación (Anónima, Básica, OAuth2.0), métodos HTTP (GET, POST, PUT, PATCH, DELETE), formato XML/JSON
- `Metodos de llamada de APIs.md` — Métodos concretos para llamadas REST desde IDM

### XPATH
- `XPATH nouns para drivers.md` — Referencia de XPATH nouns utilizados en policies de drivers

## Conceptos clave

### Tipos de drivers documentados
- **Active Directory**: sincronización IDM ↔ AD vía Remote Loader (puerto 8064)
- **API Rest**: driver genérico para servicios RESTful. Soportes CRUD, sync de contraseñas
- **LDAP**: drivers para directorios LDAP (eDirectory, OpenLDAP, etc.)

### Remote Loader
- Componente intermedio para drivers que no corren en el mismo servidor que IDM
- Comunicación cifrada entre IDM y Remote Loader
- Puertos típicos: 8060-8069
- Instalación en Windows Server con .NET Framework

### Policies
- Las policies de los drivers definen reglas de transformación de eventos
- Se configuran en Designer y se aplican en el canal de Publisher/Subscriber
- Usan XPATH para navegar y transformar el documento de eventos (XDX)
