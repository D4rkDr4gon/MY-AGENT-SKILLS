---
name: blog-writer
description: Use when the user asks to write, update, or edit a blog post for lcampassi.com/docs. Covers research, drafting, revision rounds, index updates, and deployment.
---

# blog-writer

Skill para escribir posts del blog de [lcampassi.com/docs](https://lcampassi.com/docs). Garantiza consistencia en tono, estructura, nivel técnico y estilo editorial.

## Datos del Proyecto

| Campo | Valor |
|-------|-------|
| **URL** | `https://lcampassi.com/docs/` |
| **Local** | `/files/my-web/docs/` |
| **Posts** | `/files/my-web/docs/posts/` |
| **Blog index** | `/files/my-web/docs/index.html` |
| **Portfolio** | `/files/my-web/index.html` |
| **GitHub** | `D4rkDr4gon/D4rkDr4gon.github.io` |
| **CNAME** | `lcampassi.com` (custom domain, archivo en `public/CNAME`) |
| **Deploy** | GitHub Actions — push a master → build Vite → GitHub Pages |
| **Server local** | `npm run dev` (Vite, http://localhost:8080) |
| **Build tool** | **Vite 6** — dev server con HMR, production builds con hashing |
| **Framework** | None — HTML plano + Vite, sin CMS, sin backend |
| **CSS** | `src/styles/blog.css` (compartido por listing + todos los posts) |
| **JS** | `src/scripts/blog.js` + `src/scripts/blog-search.js` (solo listing) |
| **Fuentes** | JetBrains Mono via Google Fonts |
| **Iconos** | Font Awesome 6.5 (CDN) |

## Stack Técnico

- **Vite 6**: build tool multi-page. Escanea `docs/` recursivamente via `findHtmlFiles()` en `vite.config.js`. Cada `.html` en `docs/` es una entry de Vite. **No hay que tocar `vite.config.js` al agregar posts.**
- **CSS compartido**: todos los HTML del blog (listing + posts) importan `/src/styles/blog.css`. En producción, Vite transforma la ruta a un hash (`/assets/blog-xxx.css`).
- **Sin CSS inline**: ninguna página del blog debe tener `<style>` inline. Todo via `blog.css`.
- **Sin JS en posts individuales**: solo el listing (`docs/index.html`) importa `blog.js`. Los posts no necesitan JavaScript.
- **Post template**: la clase del nav es `blog-nav` (no `post-nav`), con wrapper `nav-links`.

## Fuentes de Verdad

Antes de escribir CUALQUIER post, consultar estas fuentes para verificar datos técnicos y personales. **No inventar ni asumir.**

| Tema | Fuente |
|------|--------|
| **Arquitectura del sistema (Arch Linux)** | `~/dotfiles/docs/` — documentación real de la máquina |
| **Configuración de dotfiles** | `~/dotfiles/` — los archivos mismos |
| **Herramientas, scripts, automatización** | `~/dotfiles/`, `~/code/`, `~/MY-AGENT-SKILLS/` |
| **IAM, NetIQ, papers técnicos** | `/files/Personal-Vault/Manuales/` — vault de Obsidian |
| **Proyectos, agentes, skills** | `~/MY-AGENT-SKILLS/SKILLS/` — las skills mismas |
| **Historial de decisiones del blog** | `~/.config/opencode/projects/` — anchored summaries de sesiones previas |
| **Datos personales (setup, hardware, OS)** | Preguntar al usuario directamente si no está en las fuentes |

## Voice & Tone

- **Voz**: primera persona ("descubrí", "trabajo", "implementé"). Nunca "nosotros" corporativo ni tercera persona.
- **Tono**: técnico pero accesible. Como si se lo explicaras a un colega en una charla de café. Nada de jerga innecesaria, pero sin simplificar de más.
- **Actitud**: directo, sin vueltas. Arrancá con el problema, no con introducciones genéricas. Mostrá entusiasmo genuino por el tema.
- **Longitud**: entre 800 y 2000 palabras. Ni micro-post ni ensayo académico.

## Estructura de cada post

```
Título: directo, sin clickbait. Que describa exactamente de qué trata.
Tag: una palabra en minúscula (presentación, iam, infra, blue-team, dfir, automation, homelab, opinión, etc.)

Body:

1. Hook inicial (1-2 párrafos)
   - Arrancá con el problema, la pregunta o la situación que motivó el post.
   - Nada de "en el mundo actual..." ni "la tecnología avanza...".

2. Desarrollo (3-5 secciones con headers h2)
   - Cada sección cubre un aspecto concreto.
   - Usá ejemplos reales, anécdotas, comandos, fragmentos de código si aplica.
   - Si mostrás código, que sea breve y comentado.
   - Incluí blockers o lecciones aprendidas (lo que salió mal es tan valioso como lo que salió bien).

3. Cierre (1-2 párrafos)
   - Conclusión concisa. Dejá una idea, pregunta o reflexión.
   - No pongas "en conclusión" ni "para finalizar". Cerra natural.

4. (opcional) Referencias o lecturas recomendadas
```

## Nivel técnico

- **Público objetivo**: profesionales de ciberseguridad, sysadmins, devs con interés en seguridad.
- **Asume que el lector**: sabe qué es Linux, conoce conceptos básicos de redes y seguridad, usa terminal.
- **No asume que el lector**: es experto en el tema específico del post. Explicá conceptos clave sin sobre-explicar.
- **Código**: incluí comandos reales, configuraciones, scripts. Siempre con sintaxis clara y comentarios.

## Reglas de formato

- Usar el template HTML de los posts existentes en `/files/my-web/docs/posts/` (mismo navbar, footer, colores, tipografía).
- Fecha en el nombre del archivo: `YYYY-MM-DD-titulo-en-ingles.html`
- Tags en minúscula, una palabra.
- Código: `<pre><code>` con sintaxis limpia.
- Links: solo a recursos de alta calidad (docs oficiales, papers, repos). Nada de blogs de SEO.
- NO usar emojis.
- NO usar "click aquí" o "leé más".
- NO empezar con frases hechas.
- **Idioma**: escribir en español argentino correcto — usar ñ, tildes, diéresis, puntuación adecuada. No omitir acentos ni reemplazar ñ por n por "simplicidad".

## Metadata del post

Cada post debe tener:

- `<title>` con formato: `Título del post — lcampassi`
- `<meta name="description">` con resumen de 1-2 líneas para SEO

## Proceso de escritura completo

### 1. Investigación

- Consultar las **fuentes de verdad** según el tema del post
- Si el post se basa en un paper o documento del vault, leerlo completo antes de escribir
- Si menciona herramientas específicas, verificar que existan y tengan el nombre correcto
- Si menciona datos personales (setup laboral, OS, hardware), confirmar con el usuario o fuente de verdad

### 2. Borrador inicial

- Escribir siguiendo la estructura definida arriba
- Usar el template HTML existente como base
- Dejar los datos verificados, no placeholders

### 3. Primera corrección del usuario

- El usuario va a leer el borrador y corregir **datos personales**:
  - Nombres de productos, empresas, tecnologías
  - Detalles de su setup (hardware, SO, herramientas)
  - Experiencias personales (qué hace, qué usó, qué aprendió)
- Tomar cada corrección y aplicarla **sin discutir** — el usuario es la fuente de verdad sobre su propia experiencia

### 4. Correcciones adicionales (iterar hasta aprobación)

- Si el usuario pide más cambios, aplicarlos
- Pueden haber múltiples rondas
- Cada ronda: aplicar cambios, confirmar, esperar feedback

### 5. Actualizar el blog index

**IMPORTANTE**: después de crear un post, hay que agregar su card en `/files/my-web/docs/index.html`.

Cada post tiene una card con esta estructura (copiar el patrón de las existentes):

```html
<article class="post-card">
  <div class="post-meta">
    <time datetime="YYYY-MM-DD">YYYY-MM-DD</time>
    <span class="tag">tag</span>
  </div>
  <h2><a href="posts/YYYY-MM-DD-slug.html">Título del post</a></h2>
  <p class="post-excerpt">Resumen de 1-2 líneas que enganche.</p>
</article>
```

### Regla de ordenamiento del index

El blog index tiene UN orden fijo que no se negocia:

1. **Primero**: `Bienvenidos al blog` (pinneado, siempre en la posición #1)
2. **Del más nuevo al más viejo**: el resto de los posts ordenados cronológicamente descendente (más reciente primero)

Ejemplo con 10 posts:
```
Post 1  → Bienvenidos al blog           (pinneado, siempre acá)
Post 2  → (post nuevo, el más reciente)
Post 3  → Linux mutó
Post 4  → IAM Zero Trust
Post 5  → dotfiles
Post 6  → MY-AGENT-SKILLS
Post 7  → IAM Governance
Post 8  → Ekoparty
Post 9  → Obsidian
Post 10 → Trabajo IAM NetIQ
```

Al agregar un post nuevo, insertarlo en la posición #2 (después de Bienvenidos), y renumerar los siguientes.

### 6. Pre-deploy checklist

- [ ] Datos verificados contra fuentes de verdad (vault, dotfiles, skills)
- [ ] El usuario aprobó el contenido final
- [ ] El título es claro y describe el contenido
- [ ] El hook inicial arranca directo al tema
- [ ] Cada sección tiene un h2 descriptivo
- [ ] Si hay código, tiene comentarios que explican qué hace
- [ ] No hay jerga vacía ni buzzwords sin sustento
- [ ] El cierre es natural, no forzado
- [ ] La fecha y tag son correctos
- [ ] Todos los links funcionan
- [ ] El HTML valida sin errores (sin tags sin cerrar, sin atributos rotos)
- [ ] La card en el blog index está en la posición correcta (Post 1 = Bienvenidos pinneado, Post 2 = post nuevo)
- [ ] El nav del post usa clase `blog-nav` (no `post-nav`) y wrapper `nav-links`
- [ ] No hay CSS inline (`<style>` blocks) — todo via `blog.css`
- [ ] No hay `<script>` tag en posts individuales (solo el listing necesita JS)
- [ ] El link a CSS es `/src/styles/blog.css` (Vite lo transforma en build)
- [ ] Preview local funciona (`npm run dev` y abrir http://localhost:8080/docs/)

### 7. Deploy

```bash
cd /files/my-web
npm run build           # Build producción a dist/
npm run preview         # Preview local (opcional, puede colgarse)
git add -A && git commit -m "blog: add post TITULO" && git push
```

**Importante**: el deploy usa GitHub Actions. No depende de "auto-deploy desde master branch". El Action buildéa con Vite y deploya `dist/`. Esperar ~1-2 min para que se refleje en https://lcampassi.com/docs/.

No es necesario correr `npm run build` manualmente antes del push (el Action lo hace), pero es buena práctica para verificar que no haya errores.

> ⚠️ `npm run preview` puede colgarse después de un tiempo. Usar `npm run dev` para sesiones largas de testing.

## Post-template (HTML)

Usar siempre la misma estructura que los posts existentes. Copiar de `/files/my-web/docs/posts/` un post existente como base. La estructura incluye:

- Nav fijo con clase `blog-nav` (no `post-nav`), brand `lc.`, wrapper `nav-links` con links a home, blog
- Header con fecha, tag, título, reading time
- Contenido con `.post-content` (párrafos, h2, h3, listas, código, blockquotes)
- Footer minimal con clase `post-footer`

El `<head>` debe importar:
```html
<link rel="stylesheet" href="/src/styles/blog.css" />
```

No necesita `<script>` ni CSS inline. El nav usa la estructura:
```html
<nav class="blog-nav">
  <div class="container">
    <div class="nav-inner">
      <div class="brand"><a href="/">lc<span>.</span></a></div>
      <div class="nav-links">
        <a href="/"><i class="fas fa-arrow-left"></i> home</a>
        <a href="/docs/">blog</a>
        <a href="/" class="btn-blog">contact</a>
      </div>
    </div>
  </div>
</nav>
```

No cambiar el sistema de diseño (colores, tipografía, espaciado) a menos que el usuario lo pida explícitamente.

## Temas prohibidos

- No mencionar nombres de clientes en posts laborales
- No publicar información confidencial de empresas donde el usuario trabaja o trabajó
- No hacer afirmaciones técnicas sin verificar contra fuentes de verdad
