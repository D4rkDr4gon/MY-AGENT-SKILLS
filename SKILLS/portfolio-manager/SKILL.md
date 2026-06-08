---
name: portfolio-manager
description: Use when the user asks to update, modify, or maintain their personal portfolio/landing page at /files/my-web/ (GitHub Pages). Covers design system, sections, content, and deployment.
---

# portfolio-manager

## Datos del Proyecto

| Campo | Valor |
|-------|-------|
| **Local** | `/files/my-web/index.html` |
| **Foto perfil** | `/files/my-web/profile.png` |
| **GitHub** | `D4rkDr4gon/D4rkDr4gon.github.io` |
| **URL live** | `https://d4rkdr4gon.github.io/` |
| **Deploy** | `git push` a master → GitHub Pages auto-deploy |
| **Server local** | `python3 -m http.server 8080` (correr en `/files/my-web/`) |
| **Framework** | None — single HTML file, vanilla CSS + JS |
| **Fuentes** | JetBrains Mono (monospace) via Google Fonts |
| **Iconos** | Font Awesome 6.5 (CDN) |

## Stack Técnico

- **Single HTML** — todo en un archivo (CSS embebido en `<style>`, JS al final)
- **Sin frameworks** — no React, no build tools, no bundlers
- **CSS nativo** — variables custom, flexbox, grid, media queries
- **JS vanilla** — solo IntersectionObserver para nav activo
- **Sin dependencias externas** salvo Google Fonts y Font Awesome CDN

## Sistema de Diseño

### Colores

```css
:root {
  --red:        #ff2244;   /* acento principal */
  --red-dim:    #cc1133;   /* hover / variante */
  --red-dark:   #881122;   /* bordes secundarios */
  --red-glow:   rgba(255,34,68,0.1);  /* fondos hover */
  --bg:         #0a0a0a;   /* fondo principal */
  --bg-card:    #111;      /* fondos de cards */
  --bg-hover:   #1a1a1a;   /* hover cards */
  --border:     #222;      /* bordes genericos */
  --text:       #ddd;      /* texto principal */
  --text-dim:   #888;      /* texto secundario */
  --text-muted: #555;      /* texto deshabilitado */
}
```

- **Fondo**: negro (#0a0a0a)
- **Acento**: rojo (#ff2244)
- **Texto**: grises claros (#ddd, #888, #555)
- **Bordes**: grises oscuros (#222)
- **Todo `<strong>`** hereda `color: var(--red)` automáticamente vía CSS global

### Tipografía

- **Fuente única**: JetBrains Mono (monospace) para todo
- Body: `color:#ddd`, `line-height:1.6`
- Labels: `.65rem`, uppercase, `letter-spacing:.2em`
- Section titles: `1.3rem`, bold

### Espaciado

- `--radius: 6px` (bordes redondeados)
- Cards: `padding: 18px`
- Sections: `padding: 60px 0`
- Container max-width: `960px`, padding horizontal: `20px`

## Estructura de la Página

### Navegacion (fixed top)
- Brand: `lc.` (rojo el punto)
- Links: expertise, work, skills, projects, contact
- Contact es boton rojo (fondo `var(--red)`)
- Nav activo se resalta via IntersectionObserver (clase `.nav-active`)

### Hero
- Grid 2 columnas: foto (200px) | texto
- Foto: `profile.png` con borde rojo oscuro (`var(--red-dark)`)
- `whoami` → texto de rol en gris
- Tags: IAM, GOVERNANCE, FORENSICS, AI, LINUX (todos en rojo)
- Social icons: email, GitHub, LinkedIn
- Terminal header debajo con dots (rojo/amarillo/verde) y prompt `lcampassi@cyber:~$`
- El texto del `cat intro.md` debe ir sin línea en blanco después del comando (parecer terminal real)

### About (seccion colapsable)
- `details.collapse` con summary "Professional Summary"
- `details.collapse` con summary "Vision & Approach"
- Texto en inglés

### Expertise (cards en grid 2x2)
- Blue Team & DFIR
- IAM & Identity Governance
- Compliance & Auditing
- AI Automation

### Work (job card)
- Estructura `.job-card`:
  - `.job-card-head` con título, empresa, fecha
  - `.job-card-body` con descripción
  - `details.collapse` con "Key achievements" (bullet points con borde rojo izquierdo)
- Empresa actual: Plug-Zone (2023 — Present)
- Descripción debe mencionar NetIQ, OneIdentity, Active Directory, IAM Governance

### Skills (grupos de chips)
- identity & access management
- security
- dev & automation
- ai
- infra & cloud

### Credentials (grid 2 columnas)
- Certifications (icono check rojo)
- Education (icono university rojo)
- Languages al final con chips

### Projects (gallery grid 3 cards)
- dotfiles: Qtile WM, Arch Linux
- flipper-zero-Utils
- MY-AGENT-SKILLS

### Hobbies (tags con iconos)
- CTF, Home Lab, Ethical Hacking, Reading

### Contact (grid cards)
- email, phone, github, linkedin
- Contactos reales del usuario:
  - Email: `D4rkDr4g0n19@protonmail.com`
  - Phone: `+54 011 7006-6543`
  - GitHub: `D4rkDr4gon`
  - LinkedIn: `Lucciano Campassi`

### Footer
- Minimal: "lcampassi · 2026"

## Componentes Reutilizables

### Collapsible (details/summary)
```html
<details class="collapse">
  <summary>Titulo</summary>
  <div class="collapse-body">
    <p>Contenido...</p>
  </div>
</details>
```
- No poner "click to expand" ni texto similar en el summary
- Summary tiene `+` / `−` como indicador via `::after`

### Tags / Chips
```html
<span class="tag red">IAM</span>     <!-- tag roja (acento) -->
<span class="skill-chip">Python</span>  <!-- chip de skill -->
```

### Cards
```html
<div class="exp-card">           <!-- expertise card -->
<div class="gal-card">           <!-- gallery/project card -->
<div class="job-card">           <!-- work card -->
<div class="contact-card">       <!-- contact card -->
```

## Reglas para Modificaciones

1. **Preservar sistema de colores** — no cambiar el rojo como acento principal
2. **Preservar monospace** — no agregar fonts sans-serif
3. **Texto del hero intro**: debe ir pegado al `cat intro.md<br/>` sin `<br/>` extra
4. **Todos los `<strong>`** deben tener color rojo (ya via CSS global, no agregar inline)
5. **No usar JavaScript frameworks** — solo vanilla JS si es necesario
6. **No agregar "click to expand"** ni texto similar en summaries de details
7. **No cambiar las URLs de contacto** a menos que el usuario lo pida explícitamente
8. **ID de secciones** deben coincidir con los href del nav para el IntersectionObserver
9. **No borrar IDs** de secciones existentes sin actualizar el nav y el JS

## Deploy

```bash
cd /files/my-web
git add -A && git commit -m "mensaje" && git push
```

- GitHub Pages auto-deploy desde master
- Esperar ~1-2 min para que se refleje en https://d4rkdr4gon.github.io/
- Para preview local: `python3 -m http.server 8080` desde `/files/my-web/`
