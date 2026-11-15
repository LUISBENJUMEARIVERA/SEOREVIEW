# Plantillas Listas para Producción: JSON-LD, `robots.txt` y `llms.txt`

---

## 1. `robots.txt` (SEO + GEO Estratégico)
Permite rastreo completo de CSS/JS para Googlebot y habilita bots de búsqueda/citación de IA:

```txt
User-agent: *
Allow: /
Disallow: /api/
Disallow: /admin/
Disallow: /dashboard/

# Motores de búsqueda de IA (Recomendado permitir para citaciones GEO)
User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: PerplexityBot
Allow: /

# Opcional: Descomentar solo si deseas bloquear entrenamiento de modelos sin afectar búsqueda
# User-agent: GPTBot
# Disallow: /
# User-agent: Google-Extended
# Disallow: /

Sitemap: https://TUDOMINIO.com/sitemap.xml
```

---

## 2. `llms.txt` (Estándar GEO en `/public/llms.txt`)
```markdown
# Nombre de la Marca / Sitio

> Resumen claro de 1–2 frases sobre qué hace el sitio, a quién sirve y cuál es su propuesta de valor principal.

## Páginas Principales
- [Inicio](https://TUDOMINIO.com/): Visión general y propuesta de valor.
- [Servicios / Producto](https://TUDOMINIO.com/servicios): Descripción detallada de soluciones.
- [Precios](https://TUDOMINIO.com/precios): Planes y tarifas vigentes.
- [Blog / Recursos](https://TUDOMINIO.com/blog): Guías técnicas y estudios propios.
- [Contacto](https://TUDOMINIO.com/contacto): Canales oficiales de atención.

## Datos Clave de Entidad
- Industria: [Tu industria]
- Ubicación / Cobertura: [Ciudad, País o Global]
- Contacto oficial: [email@tudominio.com]
```

---

## 3. JSON-LD: `Organization` + `WebSite` (Home)
```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://TUDOMINIO.com/#organization",
      "name": "Nombre de la Marca",
      "url": "https://TUDOMINIO.com",
      "logo": {
        "@type": "ImageObject",
        "url": "https://TUDOMINIO.com/logo.png"
      },
      "sameAs": [
        "https://www.linkedin.com/company/tu-marca",
        "https://x.com/tu-marca"
      ]
    },
    {
      "@type": "WebSite",
      "@id": "https://TUDOMINIO.com/#website",
      "url": "https://TUDOMINIO.com",
      "name": "Nombre de la Marca",
      "publisher": {
        "@id": "https://TUDOMINIO.com/#organization"
      },
      "inLanguage": "es"
    }
  ]
}
```

---

## 4. JSON-LD: `Article` / `BlogPosting` (E-E-A-T)
```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "Título exacto del artículo (máx. 110 caracteres)",
  "description": "Resumen claro del artículo.",
  "image": "https://TUDOMINIO.com/imagen-portada.webp",
  "datePublished": "2026-01-15T09:00:00-05:00",
  "dateModified": "2026-02-01T12:00:00-05:00",
  "author": {
    "@type": "Person",
    "name": "Nombre del Autor",
    "url": "https://TUDOMINIO.com/autor/nombre-autor"
  },
  "publisher": {
    "@id": "https://TUDOMINIO.com/#organization"
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://TUDOMINIO.com/blog/slug-del-articulo"
  }
}
```

---

## 5. JSON-LD: `FAQPage` (Ideal para AI Overviews y Long-Tail)
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "¿Pregunta exacta que busca el usuario?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Respuesta directa, precisa y verificable en 40–60 palabras."
      }
    }
  ]
}
```

---

## 6. JSON-LD: `BreadcrumbList`
```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Inicio",
      "item": "https://TUDOMINIO.com/"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Categoría",
      "item": "https://TUDOMINIO.com/categoria"
    }
  ]
}
```
