---
name: seo-top1-architect
license: MIT
description: >-
  Audits websites (codebases or live URLs), produces a scored SEO + GEO diagnostic
  (0-100), fixes technical/rendering/semantic/E-E-A-T/AI-crawling bottlenecks
  (especially in AI-built sites like Lovable, Bolt, v0, React/Vite SPAs), and
  redesigns architecture and content to rank Top 1 in Google Search and AI Overviews.
  Use whenever the user asks to audit, analyze, diagnose, fix, optimize, reorient,
  or design a website for SEO, Top 1 ranking, Google Search, or GEO/AI citations.
---

# SEO Top 1 Architect (SEO + GEO + Sitios IA)

Skill integral para auditar sitios web (repositorios locales o URLs en vivo), diagnosticar cuellos de botella técnicos y estratégicos, y **completar, reorientar o rediseñar** la arquitectura, el código y el contenido hacia el **posicionamiento Top 1 en Google** y citación en **AI Overviews / motores generativos (GEO)**.

---

## Flujo de Trabajo Obligatorio (5 Fases)

### Fase 1: Reconocimiento & Auditoría Técnica Automatizada
1. Identifica el objetivo de análisis:
   - **Código fuente local** (ej. proyecto React/Vite, Next.js, Astro, HTML estático)
   - **URL en vivo** (o ambos).
2. Ejecuta el script de auditoría incluido para obtener métricas reales sin adivinar (soporta `--format json` o `--format markdown`):
   ```bash
   # Para proyecto local:
   python scripts/seo_audit.py --path "<ruta_del_proyecto>" --format markdown
   # Para URL en vivo (simula Googlebot Oleada 1 y bots de IA):
   python scripts/seo_audit.py --url "https://tusitio.com" --format markdown
   ```
3. Si es un repositorio local, inspecciona también `package.json`, `index.html`, archivos de rutas/páginas, `public/robots.txt`, `public/sitemap.xml` y `public/llms.txt`.

### Fase 2: Diagnóstico Estructurado & Scorecard (0–100)
Evalúa los resultados usando la rúbrica de [diagnostic_rubric.md](./references/diagnostic_rubric.md) y presenta un **Diagnóstico Ejecutivo** con:
1. **Score Global (0–100)** desglosado en 5 pilares:
   - Rastreo & Renderizado (25 pts) — *Crítico en sitios IA (CSR vs SSR/SSG)*
   - SEO On-Page & HTML Semántico (20 pts)
   - Datos Estructurados JSON-LD & GEO (20 pts)
   - Core Web Vitals & Rendimiento (20 pts)
   - E-E-A-T, Intención & Arquitectura de Contenido (15 pts)
2. **Hallazgos clasificados por severidad**:
   - 🔴 **Bloqueantes (P0):** Ej. `<div id="root"></div>` vacío en HTML inicial (CSR puro), `noindex` accidental, bloqueo en `robots.txt`, ausencia de `<a href>`.
   - 🟠 **Altos (P1):** Títulos/descripciones duplicados o ausentes, sin canonical, múltiples `<h1>` o sin `<h1>`, sin `sitemap.xml`, sin JSON-LD.
   - 🟡 **Medios (P2):** Imágenes sin `alt`/`width`/`height`, jerarquía `H2-H3` rota, falta `llms.txt`, Open Graph incompleto.
   - 🟢 **Oportunidades Top 1 / GEO:** Respuesta directa (primeras 30–50 palabras), Topic Clusters, tablas comparativas, Schema avanzado.

### Fase 3: Plan de Reorientación y Diseño Top 1
Antes de editar código masivamente, define (y valida con el usuario si hay cambios estructurales mayores como migración de framework):
1. **Decisión de Renderizado (Sitios IA):** Si es una SPA CSR (`Vite + React` de Lovable/Bolt/v0), aplica la guía [ai_site_seo_checklist.md](./references/ai_site_seo_checklist.md):
   - *Opción A (Óptima):* Migrar a SSR/SSG (Next.js App Router, Astro o React Router v7 Framework Mode).
   - *Opción B (Rescate rápido sin reescribir):* Pre-renderizado estático (`vite-ssg` / `vite-plugin-prerender`) o Edge Pre-rendering para bots + `react-helmet-async` para metadatos por ruta.
2. **Arquitectura de Silos & Intención de Búsqueda:** Mapeo de URL limpia, keyword principal, intención (informacional/comercial/transaccional) y enlazado interno con `href` reales.
3. **Estrategia E-E-A-T & GEO:** Señales de autoría real, datos verificables, estructura extractable para AI Overviews.

### Fase 4: Implementación Quirúrgica (Completar / Reorientar / Rediseñar)
Ejecuta las mejoras directamente en el código del proyecto usando las plantillas de [schema_templates.md](./references/schema_templates.md):
1. **Metadatos dinámicos por ruta:** `<title>` único (50–60 chars), `<meta name="description">` (140–160 chars), `<link rel="canonical">`, Open Graph y Twitter Cards.
2. **HTML Semántico & Enlazado:** Un solo `<h1>` por vista, `<main>`, `<header>`, `<nav>`, `<article>`, `<footer>`; reemplazar cualquier `<div onClick>` de navegación por `<a href>` o `<Link to>`.
3. **Infraestructura de Rastreo & GEO:**
   - Usa el generador automático cuando falten archivos base:
     ```bash
     python scripts/generate_seo_assets.py --out ./public --base-url "https://tusitio.com" --brand "Marca" --summary "Resumen." --routes / /servicios /contacto
     ```
   - Verifica que `robots.txt` permita JS/CSS, `Googlebot`, `OAI-SearchBot`, `Claude-SearchBot` y `PerplexityBot`.
   - Asegúrate de que `sitemap.xml` incluya solo URLs canónicas `200 OK` y que `llms.txt` resuma el sitio en Markdown limpio.
4. **Datos Estructurados JSON-LD:** Inyectar Schema válido (`Organization`, `WebSite`, `Article`/`Product`/`Service`, `FAQPage`, `BreadcrumbList`) acorde al contenido visible.
5. **Core Web Vitals (LCP ≤ 2.5s, INP < 200ms, CLS < 0.1):**
   - `width` y `height` explícitos en imágenes/iframes, `fetchpriority="high"` en imagen hero, `loading="lazy"` debajo del fold, `font-display: swap`, code-splitting.
6. **Reorientación Editorial Top 1:** Reescribir hero, encabezados y bloques de contenido con respuesta directa inicial, datos concretos, FAQ y cero relleno genérico de IA (*Scaled Content Abuse*).

### Fase 5: Verificación & Validación Final
1. Re-ejecuta `python scripts/seo_audit.py` sobre el proyecto (y sobre la URL si se desplegó o levantó servidor local).
2. Verifica que el build de producción compile sin errores (`npm run build` / `pnpm build`).
3. Entrega al usuario:
   - Comparativa **Antes vs. Después** del Scorecard (0–100).
   - Lista exacta de archivos creados/modificados.
   - Pasos finales externos recomendados (enviar `sitemap.xml` a Google Search Console, probar en *Rich Results Test* y *PageSpeed Insights*).
