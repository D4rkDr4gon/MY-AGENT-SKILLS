---
name: portfolio-manager
description: Use when the user asks to update, modify, or maintain their personal portfolio/landing page (GitHub Pages). Covers positioning, bilingual EN/ES sections, design system (light/dark), SEO, blog integration, and deployment.
---

# portfolio-manager

## Qué es el sitio (leer antes de tocar contenido)

`https://$BLOG_DOMAIN` es, en este orden de prioridad:

1. **Un CV personal vivo**, siempre actualizado: rol, experiencia, certificaciones, charlas, proyectos.
2. **Quién es y qué valor aporta** como consultor en gestión y gobernanza de identidades.
3. **Servicios de consultoría independiente** (secundario, pero visible): gestión y gobierno de identidades, cumplimiento normativo, gobernanza de seguridad, Active Directory y Entra ID.

Objetivos: verse profesional, posicionar bien en Google, ayudar a la carrera.

### Reglas de contenido (no negociables)

- **Capacidad real, con su voz.** Nada de slogans, frases de marketing, estadísticas de relleno ni métricas inventadas. Si un dato no lo dio el usuario o no está en una fuente verificable, no va.
- **No resaltar escala** (cantidad de identidades, de proyectos, etc.) ni poner "Disponible para…".
- **Agnóstico a la herramienta.** Trabaja con One Identity (suite Identity Fabric completa: Identity Manager/IGA, Safeguard/PAM, OneLogin, Active Roles), NetIQ, Active Directory y Entra ID, pero no se limita a un fabricante. No presentarlo como vendedor/preventa: las acreditaciones de ventas/preventa son certificaciones, no su rol.
- **Títulos oficiales:** rol = "Consultor en Gestión y Gobernanza de Identidades" + "Responsable de cuenta" (EN: "Identity Management & Governance Consultant" + "Account Manager"). Empresa: Plug-Zone, partner líder de One Identity en LATAM.
- **Nunca publicar su localidad** ni dirección. En JSON-LD solo `addressCountry: AR`.
- **Nombres oficiales de certificaciones** tal cual los emite cada organismo. Las que están en curso/preparación se marcan así (hoy: Identity Manager Implementation Professional; SC-200 y SC-900 de Microsoft).
- Formación: "Lic. en Ciberseguridad (UFASTA)" — sin "en curso" en la ficha.
- Cualquier dato nuevo de experiencia/certificaciones se actualiza en **EN y ES** y en **el JSON-LD de ambos idiomas**.

## Datos del Proyecto

| Campo | Valor |
|-------|-------|
| **Local** | `$BLOG_ROOT/` |
| **GitHub** | `$BLOG_REPO` |
| **URL live** | `https://$BLOG_DOMAIN` — inglés en `/`, español en `/es/`, blog (español) en `/docs/` |
| **Deploy** | GitHub Actions (`.github/workflows/deploy.yml`, Node 22, `npm ci` + `npm run build`) — push a `master` |
| **Server local** | `npm run dev` (Vite, puerto 8080, `host: true` → también accesible por IP de la LAN) |
| **Build tool** | Vite 6, multi-page, sin frameworks JS |
| **Fuentes** | Inter (texto) + JetBrains Mono (acentos: eyebrows, tags, `$ whoami`) vía Google Fonts |
| **Iconos** | Font Awesome 6.5 (CDN cdnjs) |
| **Contacto público** | `contacto@lcampassi.com`, LinkedIn, GitHub (`D4rkDr4gon`), Sessionize |

## Estructura del Proyecto

```
$BLOG_ROOT/
├── index.html                 # Landing en INGLÉS (default, /) — solo <head> + @includes de src/sections/en
├── es/index.html              # Landing en ESPAÑOL (/es/) — @includes de src/sections/es
├── vite.config.js             # entries + plugins htmlInclude() y sitemap()
├── .github/workflows/deploy.yml
├── public/                    # Copiado tal cual a dist/
│   ├── CNAME
│   ├── robots.txt             # apunta a /sitemap.xml
│   ├── favicon.ico, favicon-192.png, apple-touch-icon.png   # generados desde profile.png
│   ├── profile.png, profile.webp                             # foto del hero
│   └── og-image.png (ES), og-image-en.png (EN)               # 1200x630 para redes
├── docs/                      # Blog (español), escaneado automáticamente por findHtmlFiles()
│   ├── index.html             # Listado + búsqueda
│   └── posts/YYYY-MM-DD-slug.html
├── src/
│   ├── sections/
│   │   ├── en/                # Partials en inglés
│   │   └── es/                # Partials en español (mismos nombres)
│   │       nav, hero, about, experience, capabilities, credentials,
│   │       talks, projects, services, contact, footer
│   ├── seo/
│   │   ├── jsonld-en.html     # JSON-LD @graph (ProfilePage, Person, Event, ProfessionalService, WebSite)
│   │   └── jsonld-es.html
│   ├── styles/
│   │   ├── index.css          # @import de los partials (landing)
│   │   ├── blog.css           # Estilos del blog (listing + posts), mismos tokens
│   │   ├── _variables.css     # Tokens de diseño claro/oscuro
│   │   ├── _reset.css         # Reset, tamaño de fuente fluido, .container, .theme-toggle
│   │   ├── _base.css          # .section, .section--alt, .eyebrow, .section-title, .reveal
│   │   ├── _components.css    # Todos los componentes de la landing
│   │   └── _media.css         # Breakpoints (960px, 680px)
│   └── scripts/
│       ├── index.js           # Landing: initTheme + initNavigation + initReveal
│       ├── _navigation.js     # Nav scrolled, menú móvil, link activo, reveal on scroll
│       ├── theme.js           # Toggle claro/oscuro (localStorage 'theme')
│       ├── blog.js            # Blog: initTheme + búsqueda (solo si existe #searchInput)
│       └── blog-search.js
└── dist/                      # Build (gitignored); incluye sitemap.xml generado
```

### Orden de secciones (ambos idiomas)

nav → `main`: hero, about, experience, capabilities, credentials, talks, projects (`section--alt`), services, contact → footer.

Los IDs están en inglés en `src/sections/en/` y en español en `src/sections/es/` (p. ej. `services` / `servicios`, `contact` / `contacto`, `projects` / `proyectos`). **Los `href` del nav deben coincidir con los IDs** (el observer del link activo depende de eso). Verificarlos con `grep -o 'id="[^"]*"' src/sections/{en,es}/*.html` antes de enlazar.

### Contenido por sección

- **hero**: `$ whoami`, nombre (h1), rol con parte resaltada en `.red`, párrafo de qué hace, CTAs (experiencia / servicios), redes, `.hero-now` (qué está estudiando/preparando ahora), foto con tag "Speaker en Ekoparty 2026".
- **about**: encabezado arriba, 3 párrafos en primera persona, `<dl class="facts">` (Rol actual, Empresa, Plataformas, Marcos, Formación).
- **experience**: timeline; rol actual en Plug-Zone (2023 — Actualidad) con `.role-company-sub`, `.role-subtitle` "Responsable de cuenta", descripción, bullets y chips.
- **capabilities**: 6 columnas `.expertise-col` en grilla de 3 (2 filas); 2 columnas ≤960px, 1 ≤680px.
- **credentials**: certificaciones (en curso marcadas), educación, idiomas.
- **talks**: Ekoparty 2026 (sesión en Sessionize + post de preparación).
- **projects**: las 10 cards de proyectos de GitHub.
- **services**: "Consultoría independiente", 4 servicios y `.services-cta` con mailto.
- **contact**: teasers de posts del blog + caja de contacto.

## Sistema de Diseño

- **Tema claro por defecto**, oscuro con toggle. Tokens en `_variables.css`:
  - Claro en `:root`; oscuro en `:root[data-theme='dark']` y en `@media (prefers-color-scheme: dark) { :root:not([data-theme='light']) }`. **Si se agrega un token, definirlo en los tres bloques.**
  - Script inline en el `<head>` aplica `localStorage.theme` antes del pintado (evita flash). No quitarlo.
- **Acento rojo**: `--red` (#e0193a claro / #ff3b58 oscuro). Superficies `--bg`, `--surface`, `--surface-2`; texto `--heading`, `--text`, `--text-dim`, `--text-muted`.
- `--photo-bg`, `--mark-bg`, `--mark-border`: fondos del avatar y del logo `lc.` (el logo es oscuro en ambos temas; en modo oscuro lleva borde para no "flotar").
- **Layout fluido a todo el ancho**: `html { font-size: clamp(15px, 0.35vw + 12.6px, 20px) }`; `.container { width: 100%; padding-inline: clamp(1rem, 5vw, 6rem) }`. Escala con la pantalla; no volver a un `max-width` fijo chico.
- Radios `--radius: 12px`, `--radius-sm: 8px`. Animaciones `.reveal` vía IntersectionObserver (solo si `html.js`).

## SEO (mantener al modificar)

- Cada landing tiene `title`, `description`, `canonical` propio, `hreflang` en/es/x-default (`/`, `/es/`, x-default `/`), Open Graph + Twitter (`og-image-en.png` / `og-image.png`), `theme-color` claro/oscuro.
- JSON-LD en `src/seo/jsonld-{en,es}.html` (incluido con `<!-- @include: -->`). Si cambia rol, empresa, certificaciones, charlas o servicios → actualizar ambos.
- `sitemap()` en `vite.config.js` genera `dist/sitemap.xml` con landings (con alternates hreflang) + blog; `lastmod` de los posts sale de la fecha del nombre de archivo.
- Cada post del blog lleva canonical, OG/Twitter, `article:published_time` y JSON-LD `BlogPosting` (ver skill `blog-writer`).
- Validar después del build que el JSON-LD parsea:
  ```bash
  python3 - <<'EOF'
  import re,json,glob
  for f in glob.glob('dist/**/*.html',recursive=True):
      for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>',open(f).read(),re.S):
          json.loads(m.group(1))
  print('ok')
  EOF
  ```

## Blog

Ver skill `blog-writer` para escribir posts. Resumen de integración:
- `docs/` se escanea solo: **no tocar `vite.config.js` para agregar posts**.
- Listing y posts usan `/src/styles/blog.css` y `/src/scripts/blog.js` (tema + búsqueda solo en el listing). Sin `<style>` inline.
- Nav del blog: `header.blog-nav` con brand → `/es/`, links Inicio / Proyectos / Blog, toggle de tema y botón Contacto (`/es/#contacto`). Footer con Inicio, Blog, Contacto e English (`/`).

## Reglas para Modificaciones

1. Contenido en `src/sections/{en,es}/*.html`, **siempre en los dos idiomas**. `index.html` y `es/index.html` solo tienen el `<head>` y los includes.
2. CSS en los partials `src/styles/_*.css`; nada inline. Respetar tokens (no colores hardcodeados).
3. Vanilla JS modules, sin frameworks.
4. No cambiar URLs de contacto sin pedido explícito.
5. Mantener coherencia entre nav, IDs y JSON-LD.
6. Antes de deployar: `npm run build` sin errores y mostrarle al usuario el resultado en local (`npm run dev`). **Commit/push solo cuando el usuario lo pide.**
7. Si el acceso por IP desde otro dispositivo no anda, es el firewall del host: darle el comando al usuario, no modificar la configuración de seguridad.

## Deploy

```bash
cd "$BLOG_ROOT"
npm run build                       # verificar
git add -A && git commit -m "..." && git push
gh run watch "$(gh run list -L1 --json databaseId -q '.[0].databaseId')" --exit-status
for u in / /es/ /docs/ /sitemap.xml /robots.txt; do curl -s -o /dev/null -w "%{http_code} $u\n" "https://$BLOG_DOMAIN$u"; done
```

- GitHub → Settings → Pages → Source: **GitHub Actions** (ya configurado). `CNAME` vive en `public/`.
- El deploy tarda ~30 s–2 min.
