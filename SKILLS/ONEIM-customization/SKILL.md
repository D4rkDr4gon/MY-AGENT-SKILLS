---
name: ONEIM-customization
description: >
  Use when writing or troubleshooting Designer customization in One Identity Manager (IGA) —
  templates, format scripts, table scripts, Script Library, process/job generation conditions,
  VB.NET Object Layer API (ScriptBase, dollar notation, IEntity/IEntityCollection, UnitOfWork),
  configuration parameters, System Debugger, compilación local/global. Genérico — aplica a
  cualquier instalación o cliente. Cross-platform (Linux + Windows).
---

# ONEIM-customization

## Propósito

Este skill se activa cuando el usuario necesita **escribir, revisar o depurar customización de Designer** en **One Identity Manager** (la plataforma IGA de One Identity, antes Quest). Cubre específicamente:

- **Templates** — cálculo automático de valores de columna (notación `$...$`)
- **Format scripts** — validación/normalización de valores asignados manualmente
- **Table scripts** — lógica en eventos before/after save/load/discard de un objeto
- **Script Library** — funciones VB.NET reutilizables invocadas desde otros scripts
- **Process/job generation conditions** — condiciones `Value = ...` que deciden si un proceso o paso se dispara
- **Configuration parameters** — activación de módulos y compilación condicional (`#If ... #End If`)
- **API de scripting (Object Layer)** — `ScriptBase` (`Base`, `Connection`, `Provider`, `Value`, `Variables`, `Entity`, `Session`), `IEntity`/`IEntityCollection`, `UnitOfWork`, `ObjectWalker`
- **Herramientas**: Designer (edición/compilación local y global), System Debugger (prueba de templates y format scripts), Object Browser (última opción, solo diagnóstico puntual)

**No incluye** — usar los skills hermanos:
- Administración general de la instalación (IT Shop, conectores, Job Queue/DBQueue, health checks) → `ONEIM-manager`
- PAM (Safeguard) → `ONEIM-safeguard`
- Active Roles, OneLogin, Password Manager, Starling → `ONEIM-active-roles`, `ONEIM-onelogin`, `ONEIM-password-manager`, `ONEIM-starling`
- Extensión de esquema (tablas/columnas nuevas), permisos de sistema, formularios de Web Designer → no cubierto todavía; tratar como customización general de `ONEIM-manager` hasta que exista un skill dedicado

> [!important] **Genérico por diseño**
> Este skill NO contiene datos de clientes ni customizaciones prearmadas de ninguna instalación. Siempre se trabaja en función del esquema/módulos que el usuario describa en cada conversación — nunca asumir tablas o columnas custom sin que el usuario las confirme.

---

## Contexto técnico — qué es "customizar" en Identity Manager

Customizar **no** significa tocar el código fuente del producto. Significa extender el **Object Layer** (capa intermedia entre la base SQL y los clientes: Manager, Web Portal, Job Server, Application Server) con piezas declarativas que viven **dentro de la base de metadata** y se compilan a ensamblados .NET al compilar el proyecto en Designer:

| Elemento | Dónde se define | Cuándo corre | Objetivo típico |
|---|---|---|---|
| **Template** | Designer → columna de una tabla (pestaña *Templates*) | Al calcular el valor de esa columna durante el guardado del objeto (siempre, aunque el usuario no haya tocado el campo) | Derivar un valor a partir de otras columnas propias o de objetos relacionados por FK |
| **Format script** | Designer → columna de una tabla (pestaña *Format script*) | **Solo** cuando se asigna explícitamente un valor a esa columna (edición manual o import) | Validar/normalizar el valor ingresado (mayúsculas, trim, regex, `Throw` para rechazar) |
| **Table script** | Designer → tabla (eventos before/after save/load/discard) | En los eventos del ciclo de vida del objeto | Validaciones cruzadas entre columnas, disparo de procesos tras guardar |
| **Script (Script Library)** | Designer → Script Library | Invocado explícitamente desde otros scripts | Reutilizar lógica común (helpers, integraciones) |
| **Process/job generation condition** | Designer → Process Editor, condición de un chain o step | Al evaluar si un proceso/paso debe generarse | Controlar cuándo se dispara un proceso de aprovisionamiento |

> **Diferencia clave Template vs Format script**: el template define *cómo se calcula* el valor (corre siempre al guardar); el format script define *cómo se valida* lo que alguien ya escribió (corre solo ante asignación explícita). Es común combinarlos: template calcula el default, format script garantiza formato si se sobreescribe a mano.

### Lenguaje y compilación

- El único lenguaje nativo de estos puntos de extensión es **VB.NET**. **C# no está soportado directamente** — si se necesita, se escribe en una DLL custom y se referencia/invoca desde el snippet VB.NET con `References`/`Imports` (envueltos en `#If Not SCRIPTDEBUGGER Then ... #End If`). C# nativo solo aplica al Web Portal y a proyectos de sincronización configurados explícitamente en C#.
- **Configuration parameters**: se leen con `Session.Config.GetConfigParm("Ruta\Del\Parametro")` (nunca la tabla directamente) y habilitan bloques `#If NOMBREPARM Then ... #End If` para compilación condicional según qué módulos están activos en esa instalación.
- **Compilación local** (solo el snippet en edición, feedback inmediato) vs **compilación global** (todo el proyecto → ensamblados que usan Manager/Job Server/Application Server en producción). Un template que compila local puede fallar en compilación global si referencia una tabla de un módulo deshabilitado sin el `#If` correspondiente — causa típica de errores al mover customización entre entornos.
- **System Debugger**: herramienta de Designer para probar templates y format scripts en vivo antes de compilar el proyecto completo.

### Sintaxis dólar (`$...$`) — resumen

| Notación | Significa |
|---|---|
| `$Columna$` | Valor de una columna del objeto base (String por defecto) |
| `$FK(UID_X).Columna$` | Columna de un objeto relacionado por clave foránea (encadenable) |
| `$Columna:Tipo$` | Fuerza tipo — `:Int`, `:Bool`, `:Date`, `:Double`, `:Long`, `:Decimal` |
| `$Columna[D]$` | Valor de display (resuelve limited values / multi-idioma) |
| `$Columna[o]$` | Valor original cargado de base (solo válido en la primera referencia de la expresión) |
| `$[IsLoaded]:Bool$`, `$[IsDeleted]:Bool$`, `$[IsChanged]:Bool$`, `$[IsDifferent]:Bool$`, `$[Display]$` | Estado del objeto |
| `DbVal.IsEmpty($Col:Tipo$, ValType.Tipo)` | Chequeo correcto de "sin valor" (evita falsos negativos con fechas/strings) |

### API `ScriptBase` — miembros disponibles en todo script

| Miembro | Tipo | Uso |
|---|---|---|
| `Value` | `Object` | Templates/format scripts: valor de entrada y salida |
| `Connection` | `IConnection` | `Connection.BeginTransaction()`, `Connection.GetConfigParm(...)` |
| `Session` | `ISession` | Acceso central: `Session.Source`, `Session.StartUnitOfWork()`, `Session.Config` |
| `Provider` | `IValueProvider` | Resolución equivalente a `$...$`: `Provider.GetValue("Col").String` |
| `Variables` | `VarContext` | Variables de la conexión, ej. `Variables("FULLSYNC")` |
| `Entity` / `Base` | `IEntity` / `ISingleDbObject` | Objeto base (no disponibles en templates/format scripts) |

Métodos: `MsgBox(prompt, buttons, title)`, `RaiseMessage(severity, message)` (log de servicio), `ShowProgress(message)`.

### Object Layer — CRUD típico desde script

```vb
' Query + colección
Dim q = Query.From("Person").Where(Function(c) c.Column("FirstName") = "Paula").SelectAll()
Dim col As IEntityCollection = Session.Source.GetCollection(q, EntityCollectionLoadType.Bulk)

' Crear
Dim dbPerson As IEntity = Session.Source.CreateNew("Person")
dbPerson.PutValue("FirstName", "Albert")
dbPerson.PutValue("LastName", "Einstein")
Using uow As IUnitOfWork = Session.StartUnitOfWork()
    uow.Put(dbPerson)
    uow.Commit()
End Using

' Borrar
Using uow = Session.StartUnitOfWork()
    For Each p As IEntity In col
        p.MarkForDeletion()
        uow.Put(p)
    Next
    uow.Commit()
End Using

' ObjectWalker — leer FK sin cargar el objeto completo, con cache
Dim val = dbObj.CreateWalker(Session).GetValue("FK(UID_X).FK(UID_Y).Columna").String
```

Manejo de errores: `Try / Catch / Finally`, con `Session.RollbackTransaction()` en el `Catch` cuando hay transacción abierta, y `Throw` (relanzar) o `Throw New Exception("mensaje", ex)` para envolver con contexto.

---

## Fuentes de referencia (en orden de prioridad)

1. **SDK oficial de ejemplos (vault)** — `$BABILONIA_RESOURCES/01-SCRIPTS/VB.NET/`: carpetas `01 Common` (ScriptBase, excepciones, tipos), `02 Database connection`, `03 Using database objects` (CRUD, ObjectWalker, UnitOfWork), `04 Templates`, `05 Process chains`, `06 Files and folders`, `07 Expert knowledge` (LDAP, Registry, AD, referencias externas), `09 COM objects`, `10 Special use cases`, `11 Powershell`, `12 WebService`. Es código ejecutable de One Identity, la fuente más confiable para sintaxis exacta.
2. **Documentación del vault** — `$BABILONIA_ONEIDENTITY/00-IDENTITY GOVERNANCE & ADMINISTRATION/03-CUSTOMIZATION/` (`METODO DE CUSTOMIZACION.md`, `SCRIPTS-TEMPLATES/BASIC TEMPLATES Y SCRIPTS.md`) — notas propias con capturas del curso + texto de apoyo agregado.
3. **Documentación oficial** — [Configuration Guide](https://support.oneidentity.com/technical-documents/identity-manager/9.1.1/configuration-guide) (capítulo *Scripts in One Identity Manager*), `docs.oneidentity.com`, `support.oneidentity.com`, foros de la comunidad (`oneidentity.com/community`).
4. **Web fallback** — si no alcanza lo anterior, buscar en internet el mensaje de error exacto o la firma de API puntual.

---

## Protocolo de actuación

### 1. Pedir contexto (si no está en la conversación)

- ¿Qué versión de One Identity Manager?
- ¿Sobre qué tabla/columna se customiza? ¿Es tabla estándar o extendida por esquema custom?
- ¿Se necesita template, format script, table script, o un método de Script Library?
- ¿Hay configuration parameters/módulos específicos involucrados (para saber si hace falta `#If`)?
- ¿El objetivo es nuevo desarrollo, o troubleshooting de algo que ya existe y falla?

### 2. Revisar fuentes (orden de arriba) antes de escribir código nuevo

Buscar primero si ya existe un ejemplo equivalente en `$BABILONIA_RESOURCES/01-SCRIPTS/VB.NET/` — adaptar sobre un patrón probado del SDK es más seguro que escribir desde cero.

### 3. Responder / resolver

- Entregar el snippet VB.NET completo, indicando **dónde pegarlo** en Designer (columna → Templates / Format script; tabla → Table Scripts; Script Library → nombre de función) y qué **configuration parameters** o `#If` hacen falta si aplica.
- Si el pedido implica IT Shop, conectores, esquema o administración general de la instalación → derivar a `ONEIM-manager`.
- Si no hay certeza sobre una firma de API o comportamiento exacto, decirlo explícitamente y verificar contra el SDK o la documentación oficial antes de afirmar.

### 4. Documentar (solo si el usuario lo pide explícitamente)

- Usar `obsidian-manager` para expandir `$BABILONIA_ONEIDENTITY/00-IDENTITY GOVERNANCE & ADMINISTRATION/03-CUSTOMIZATION/` — **por defecto agregar contenido nuevo sin borrar ni reordenar lo existente**, salvo que el usuario pida explícitamente reescribir.

---

## Troubleshooting — errores comunes

| Síntoma | Causa probable | Acción |
|---|---|---|
| Template/format script no compila en global aunque funciona en local | Referencia una tabla/columna de un módulo deshabilitado sin `#If` | Envolver el bloque en el `#If NOMBREPARM` correspondiente |
| Format script no dispara nunca | Se esperaba que corriera en cada guardado (eso es un template, no un format script) | Si el objetivo es recalcular siempre, usar template; si es validar solo ediciones manuales, el format script es correcto pero hay que verificar que el campo se esté editando explícitamente |
| `$Columna[o]$` da error de compilación | Se usó `[o]` en una posición que no es la primera referencia de columna (ej. `$FK(Col).Otra[o]$`) | Reordenar: `[o]` solo es válido como `$Columna[o]$` o `$FK(Columna[o]).Otra$` |
| Excepción no visible para el usuario final en Manager/Web Portal | Se usó `RaiseMessage`/log en vez de `Throw` en un format script | Para bloquear el guardado y mostrar el mensaje al usuario, usar `Throw New Exception("mensaje")` |
| Referencia a un ensamblado externo rompe el System Debugger | Falta el `#If Not SCRIPTDEBUGGER Then` alrededor de `References`/`Imports` | Envolver siempre `References`/`Imports` en ese preprocesador |

---

## Referencias

- [Configuration Guide — One Identity Manager 9.1.1](https://support.oneidentity.com/technical-documents/identity-manager/9.1.1/configuration-guide)
- SDK de ejemplos: `$BABILONIA_RESOURCES/01-SCRIPTS/VB.NET/`
- Notas del vault: `$BABILONIA_ONEIDENTITY/00-IDENTITY GOVERNANCE & ADMINISTRATION/03-CUSTOMIZATION/`
- GitHub: `https://github.com/OneIdentity`
- Comunidad: `https://www.oneidentity.com/community/identity-manager/`
