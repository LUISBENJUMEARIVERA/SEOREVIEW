# seo-top1-architect

Agent Skill para auditar sitios web (repositorios locales o URLs en vivo), generar diagnósticos SEO + GEO (0–100), rescatar sitios construidos con IA (Lovable, Bolt.new, v0, React/Vite CSR SPAs) y optimizar arquitectura, código y contenido para posicionamiento **Top 1 en Google Search** y citaciones en **AI Overviews / ChatGPT / Perplexity / Claude**.

## Instalación (`skills.sh`)

```bash
npx skills add <TU_USUARIO_GITHUB>/seo-top1-architect
```

## Estructura

- `SKILL.md` — Flujo de trabajo en 5 fases (Reconocimiento, Diagnóstico 0–100, Plan Top 1, Remediación y Verificación).
- `scripts/seo_audit.py` — Auditoría automatizada sin dependencias externas (`--path` o `--url`, salida `--format json` o `--format markdown`).
- `scripts/generate_seo_assets.py` — Generador de `robots.txt`, `sitemap.xml` y `llms.txt` listos para producción.
- `references/diagnostic_rubric.md` — Rúbrica de evaluación 0–100.
- `references/ai_site_seo_checklist.md` — Playbook de rescate para sitios IA (CSR -> SSR/SSG/Pre-rendering).
- `references/schema_templates.md` — Plantillas JSON-LD (`Organization`, `WebSite`, `BlogPosting`, `FAQPage`, `BreadcrumbList`), `robots.txt` y `llms.txt`.

## Licencia

MIT
