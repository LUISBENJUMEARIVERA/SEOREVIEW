# Playbook de Rescate SEO para Sitios Construidos con IA

Aplica esta guía cuando detectes proyectos generados con **Lovable, Bolt.new, v0, Replit, Cursor o plantillas Vite + React**.

---

## 1. Diagnóstico del Stack Generado por IA

| Stack detectado | Problema típico | Solución recomendada |
| :--- | :--- | :--- |
| **Vite + React (CSR SPA)** | `index.html` solo tiene `<div id="root"></div>`. Bots de IA y Oleada 1 ven página en blanco. Metadatos idénticos en todas las rutas. | **Ideal:** Migrar a Next.js App Router, Astro o React Router v7 Framework Mode.<br>**Rescate rápido:** `vite-ssg` / pre-rendering en build + `react-helmet-async` + `vite-plugin-sitemap`. |
| **Next.js (App Router)** | Uso excesivo de `'use client'` en páginas completas, anulando SSR. Falta `generateMetadata`, `sitemap.ts` o `robots.ts`. | Mover fetching y layout a **Server Components**, exportar `metadata` / `generateMetadata` por ruta, crear `app/sitemap.ts` y `app/robots.ts`. |
| **Astro / HTML Estático** | Buen HTML inicial, pero suele faltar JSON-LD, canonicals, `sitemap` o imágenes sin `width`/`height` / formato moderno. | Integrar `@astrojs/sitemap`, componente `<SEO />` en `<head>`, `<Image />` de Astro y bloques JSON-LD. |

---

## 2. Correcciones Obligatorias en Vite + React (Si no se migra de framework)

### A. Metadatos dinámicos con `react-helmet-async`
Envuelve la app en `<HelmetProvider>` y crea un componente reutilizable `<SeoHead />`:
```tsx
import { Helmet } from 'react-helmet-async';

interface SeoHeadProps {
  title: string;
  description: string;
  canonicalUrl: string;
  ogImage?: string;
  type?: 'website' | 'article';
  jsonLd?: Record<string, unknown>;
}

export function SeoHead({
  title,
  description,
  canonicalUrl,
  ogImage = '/og-default.jpg',
  type = 'website',
  jsonLd,
}: SeoHeadProps) {
  return (
    <Helmet>
      <title>{title}</title>
      <meta name="description" content={description} />
      <link rel="canonical" href={canonicalUrl} />
      <meta property="og:type" content={type} />
      <meta property="og:title" content={title} />
      <meta property="og:description" content={description} />
      <meta property="og:url" content={canonicalUrl} />
      <meta property="og:image" content={ogImage} />
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content={title} />
      <meta name="twitter:description" content={description} />
      {jsonLd && (
        <script type="application/ld+json">{JSON.stringify(jsonLd)}</script>
      )}
    </Helmet>
  );
}
```

### B. Pre-renderizado estático en build (para eliminar el cascarón vacío)
Para sitios informativos/landing/blogs en Vite, configura pre-rendering de rutas públicas (ej. con `vite-plugin-prerender` o un script post-build con Playwright/Puppeteer que guarde el HTML renderizado de cada ruta en `dist/<ruta>/index.html`).
* **Verificación:** Al abrir `dist/index.html` o hacer `curl` en producción, el `<h1>` y los párrafos principales deben estar presentes en el HTML crudo.

### C. Corrección de Navegación (Anti-patrón común de IA)
* ❌ **Prohibido:** `<div onClick={() => navigate('/servicios')} className="cursor-pointer">...</div>`
* ❌ **Prohibido:** `<button onClick={() => navigate('/contacto')}>Contacto</button>`
* ✅ **Correcto:** `<Link to="/servicios">Servicios</Link>` o `<a href="/servicios">Servicios</a>`

### D. Rescate de Core Web Vitals en Sitios IA
1. **LCP:** En `index.html`, añade `<link rel="preload" as="image" href="/hero.webp" fetchpriority="high" />` si hay imagen hero. Usa WebP/AVIF.
2. **CLS:** Toda etiqueta `<img>` debe llevar `width` y `height` (o clases Tailwind `aspect-[16/9]` / `w-full h-auto` con dimensiones intrínsecas).
3. **INP:** Usa `React.lazy()` + `Suspense` para rutas secundarias y modales pesados; evita animar propiedades que disparen reflow (`top`, `left`, `width`, `height`) — usa solo `transform` y `opacity`.
