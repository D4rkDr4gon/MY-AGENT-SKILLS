---
name: portfolio-manager
description: Use when the user asks to update, modify, or maintain their personal portfolio/landing page (GitHub Pages). Covers design system, sections, content, blog integration, and deployment.
---

# portfolio-manager

## Datos del Proyecto

| Campo | Valor |
|-------|-------|
| **Local** | `$BLOG_ROOT/` |
| **Foto perfil** | `$BLOG_ROOT/public/profile.png` |
| **GitHub** | `$BLOG_REPO` |
| **URL live** | `https://$BLOG_DOMAIN` |
| **Deploy** | GitHub Actions (`.github/workflows/deploy.yml`) — push a master |
| **Server local** | `npm run dev` (Vite, http://localhost:8080) |
| **Build tool** | **Vite 6** — dev server HMR + production builds |
| **Fuentes** | JetBrains Mono (monospace) via Google Fonts |
| **Iconos** | Font Awesome 6.5 (CDN) |

## Stack Técnico

- **Vite 6** — build tool, dev server con HMR, bundling, code splitting
- **CSS modular** — partials con `@import`, variables, componentes, responsive
- **JS modular** — ES modules con import/export, IntersectionObserver
- **HTML partials** — secciones separadas con `<!-- @include: -->` + plugin custom (`html-include`)
- **Multi-page** — portfolio + blog listing + todos los posts en un mismo build
- **Escaneo automático de entradas** — `findHtmlFiles()` en `vite.config.js` busca recursivamente HTML en `docs/` y los agrega como entradas de Vite sin tocar configuración
- **Sin frameworks JS** — vanilla JS modules, sin React/Vue/Angular
- **Sin dependencias externas** salvo Google Fonts, Font Awesome y Vite

## Estructura del Proyecto

```
$BLOG_ROOT/
├── index.html                       # Portfolio entry (template con @include)
├── package.json                     # Vite + scripts
├── vite.config.js                   # HTML includes + multi-page entries
├── .gitignore
├── .github/workflows/deploy.yml     # GitHub Actions → GitHub Pages
├── public/                          # Static assets (copiados a dist/ tal cual)
│   ├── profile.png
│   └── CNAME
├── docs/                            # Blog (Vite multi-page entries, escaneados automáticamente)
│   ├── index.html                   # Blog listing — importa /src/styles/blog.css
│   └── posts/                       # 11 posts individuales
│       ├── 2026-06-08-*.html
│       └── ...
├── src/
│   ├── styles/
│   │   ├── index.css                # Portfolio: @import de partials
│   │   ├── blog.css                 # Blog: @import variables + reset + componentes blog
│   │   ├── _variables.css           # Design tokens (colores, fuentes, spacing)
│   │   ├── _reset.css               # CSS reset / normalize
│   │   ├── _base.css                # Layout utilities (.container, .section, .label)
│   │   ├── _components.css          # Todos los componentes del portfolio
│   │   └── _media.css               # Responsive queries
│   ├── scripts/
│   │   ├── index.js                 # Portfolio: entry point
│   │   ├── _navigation.js           # IntersectionObserver para nav highlight
│   │   ├── blog.js                  # Blog: entry point (solo listing, no posts)
│   │   └── blog-search.js           # Blog: búsqueda en tiempo real
│   └── sections/                    # Portfolio HTML partials
│       ├── nav.html
│       ├── hero.html
│       ├── about.html
│       ├── expertise.html
│       ├── work.html
│       ├── skills.html
│       ├── credentials.html
│       ├── projects.html
│       ├── hobbies.html
│       ├── contact.html
│       └── footer.html
└── dist/                            # Build output (gitignored)
    ├── index.html
    ├── docs/
    │   ├── index.html
    │   └── posts/*.html
    ├── assets/ (hasheados: CSS, JS, images)
    └── CNAME
```

## Comandos

```bash
npm run dev       # Dev server → http://localhost:8080 (HMR)
npm run build     # Build producción → dist/
npm run preview   # Preview del build → http://localhost:8080
```

> ⚠️ **Warning**: `npm run preview` puede colgarse después de un tiempo. Usar `npm run dev` para sesiones largas de testing.

## Sistema de Diseño

### Colores

```css
:root {
  --red:            #ff2244;   /* acento principal */
  --red-dim:        #cc1133;   /* hover / variante */
  --red-dark:       #881122;   /* bordes secundarios */
  --red-glow:       rgba(255,34,68,0.1);  /* fondos hover */
  --red-glow-strong: rgba(255,34,68,0.2);
  --bg:             #0a0a0a;   /* fondo principal */
  --bg-card:        #111;      /* fondos de cards */
  --bg-hover:       #1a1a1a;   /* hover cards */
  --border:         #222;      /* bordes genericos */
  --border-red:     #331115;   /* borde rojo oscuro */
  --text:           #ddd;      /* texto principal */
  --text-dim:       #888;      /* texto secundario */
  --text-muted:     #555;      /* texto deshabilitado */
  --radius:         6px;       /* borde redondeado standard */
  --container-max:  960px;     /* ancho máximo del portfolio */
  --nav-height:     52px;      /* altura de la barra de navegación */
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
- Portfolio container: `max-width: 960px`
- Blog container: `max-width: 720px` (más angosto para legibilidad)
- Padding horizontal: `20px`

## Estructura del Portfolio

### Navegacion (fixed top)
- Brand: `lc.` (rojo el punto)
- Links: expertise, work, skills, projects, blog (link a `/docs/`), contact
- Contact es boton rojo (fondo `var(--red)`)
- Nav activo se resalta via IntersectionObserver (clase `.active`)
- Definido en `src/sections/nav.html`

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
- Key achievements tiene padding extra:
  - `.collapse-body`: `padding: 14px 20px 20px`
  - Último `.collapse` dentro de `.job-card`: `margin: 0 18px 24px` (distancia ≥24px del borde inferior de la card)

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
  - Email: `empleo@lcampassi.com`
  - Phone: `+54 011 7006-6543`
  - GitHub: `D4rkDr4gon`
  - LinkedIn: `Lucciano Campassi`

### Footer
- Minimal: "lcampassi · 2026"

## Blog (docs/)

### Arquitectura
El blog comparte el mismo sistema de diseño (variables, reset) con el portfolio pero tiene su propia hoja de estilo (`src/styles/blog.css`) que incluye:

- Navegación propia (`.blog-nav`) con link de vuelta al portfolio
- Header con búsqueda en tiempo real
- Post cards (`.post-card`) con hover effects
- Artículo de post (`.post-article`, `.post-header`, `.post-content`) con estilos para:
  - Párrafos, headings (h2, h3)
  - Listas, código inline (`<code>`), bloques de código (`<pre>`)
  - Blockquotes con borde rojo
  - Links, tablas, imágenes
- Footer propio
- Container más angosto: 720px vs 960px del portfolio
- JS de búsqueda modularizado en `src/scripts/blog-search.js`

### Multi-page entries
Vite escanea `docs/` recursivamente via `findHtmlFiles()` en `vite.config.js`. Cada `.html` en `docs/` es una entry de Vite:

- `docs/index.html` → build a `dist/docs/index.html` (blog listing, sirve en `/docs/`)
- `docs/posts/*.html` → build a `dist/docs/posts/*.html` (posts individuales)

**No hay que tocar `vite.config.js` al agregar un post nuevo** — el escaneo es automático.

### CSS compartido
Todos los HTML del blog (listing + posts) importan `/src/styles/blog.css`. Vite transforma esta ruta al hash de producción en el build (`/assets/blog-xxx.css`). **No usar CSS inline** en los posts.
El listing importa además `/src/scripts/blog.js` (que a su vez importa `blog-search.js`). Los posts no necesitan JS.

### Post template
La clase del nav es `blog-nav` (no `post-nav`), y el wrapper de links usa `nav-links`. Las classes del contenido son:

```html
<article class="post-article">
  <header class="post-header">...</header>
  <div class="post-content">...</div>
</article>
```

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
<span class="tag red">IAM</span>       <!-- tag roja (acento) -->
<span class="skill-chip">Python</span>  <!-- chip de skill -->
```

### Cards
```html
<div class="exp-card">           <!-- expertise card -->
<div class="gal-card">           <!-- gallery/project card -->
<div class="job-card">           <!-- work card -->
<div class="contact-card">       <!-- contact card -->
```

## Cómo Agregar un Post Nuevo

1. **Crear archivo** en `docs/posts/YYYY-MM-DD-titulo-en-ingles.html`
2. **Usar la misma estructura** que los posts existentes:
   - Nav con clases `blog-nav` > `nav-inner` > `nav-links`
   - Link a `/src/styles/blog.css` en el `<head>` (Vite lo transforma en build)
   - No necesita `<script>` (los posts no usan JS de búsqueda)
   - No necesita CSS inline — todo está en `blog.css`
3. **Agregar card en `docs/index.html`** (blog listing), en la posición correcta:
   - Post 1 = "Bienvenidos al blog" (pinneado, siempre primero)
   - Post 2 = el post más nuevo
   - Del más nuevo al más viejo después del pinneado
4. **Build** y deploy

## Reglas para Modificaciones

1. **Preservar sistema de colores** — no cambiar el rojo como acento principal
2. **Preservar monospace** — no agregar fonts sans-serif
3. **Hero intro**: el texto debe ir pegado al `cat intro.md<br/>` sin `<br/>` extra
4. **Todos los `<strong>`** deben tener color rojo (ya via CSS global, no agregar inline)
5. **No usar JavaScript frameworks** — solo vanilla JS modules
6. **No agregar "click to expand"** ni texto similar en summaries de details
7. **No cambiar las URLs de contacto** a menos que el usuario lo pida explícitamente
8. **ID de secciones** deben coincidir con los href del nav para el IntersectionObserver
9. **No borrar IDs** de secciones existentes sin actualizar el nav y el JS
10. **CSS se edita en partials** (`src/styles/_*.css`), no en el HTML
11. **HTML de secciones** se edita en `src/sections/*.html`, no en `index.html`
12. **Blog CSS** se edita en `src/styles/blog.css`, compartido por listing + posts
13. **JS del portfolio** va en `src/scripts/_navigation.js` (importado desde `index.js`)
14. **JS del blog** va en `src/scripts/blog-search.js` (importado desde `blog.js`)
15. **Siempre rebuildear** después de cambios (`npm run build`)
16. **No tocar `vite.config.js`** para agregar HTML nuevos — `findHtmlFiles()` escanea `docs/` automáticamente
17. **El nav del blog usa clase `blog-nav`**, no `post-nav` — mantener consistencia en todos los posts

## Deploy

### Configuración única (ya hecha)
En GitHub → Settings → Pages → Source: **GitHub Actions** (no "Deploy from a branch").

### Automático (recomendado)
El workflow de GitHub Actions (`.github/workflows/deploy.yml`) buildéa con Vite y deploya `dist/` a GitHub Pages automáticamente al pushear a `master`.

```bash
cd "$BLOG_ROOT"
git add -A && git commit -m "mensaje" && git push
```

- El build produce: portfolio (`/`) + blog listing (`/docs/`) + posts (`/docs/posts/*.html`) + assets hasheados en `/assets/`
- GitHub Actions detecta el push, buildéa y deploya
- Esperar ~1-2 min para que se refleje en https://${BLOG_DOMAIN}/
- Build output: `dist/` (gitignored)

### Notas
- `CNAME` está en `public/` y se copia a `dist/` automáticamente
- La carpeta `docs/` en source NO se deploya — se deploya el build de Vite (`dist/docs/`)
- Archivos viejos en el root (`CNAME`, `profile.png`) deben limpiarse del repo si están, ahora están en `public/`
