# Rúbrica de Diagnóstico SEO + GEO (0–100 Puntos)

Usa esta rúbrica en la **Fase 2** para puntuar objetivamente cualquier sitio web.

## Desglose de Puntuación

| Pilar | Peso | Criterios de Evaluación Top 1 |
| :--- | :---: | :--- |
| **1. Rastreo, Indexabilidad y Renderizado** | **25 pts** | • HTML inicial contiene el contenido principal (SSR/SSG/Pre-render, no `<div id="root"></div>` vacío): **10 pts**<br>• `robots.txt` válido sin bloquear recursos críticos ni bots de búsqueda/GEO: **5 pts**<br>• `sitemap.xml` presente, válido y enlazado: **5 pts**<br>• `<link rel="canonical">` correcto y sin `noindex` accidental: **5 pts** |
| **2. SEO On-Page & HTML Semántico** | **20 pts** | • `<title>` único por ruta (50–60 caracteres) con keyword principal: **5 pts**<br>• `<meta name="description">` única (140–160 caracteres) orientada a CTR: **4 pts**<br>• Exactamente un `<h1>` por página + jerarquía `H2 > H3` limpia: **5 pts**<br>• Etiquetas semánticas (`<main>`, `<header>`, `<nav>`, `<footer>`) y enlaces `<a href>` reales (cero `<div onClick>`): **4 pts**<br>• Open Graph (`og:title`, `og:description`, `og:image`) y Twitter Cards completos: **2 pts** |
| **3. Datos Estructurados (JSON-LD) & GEO** | **20 pts** | • JSON-LD válido (`Organization`/`WebSite` + tipo específico `Product`/`Article`/`Service`/`SoftwareApplication`): **10 pts**<br>• `BreadcrumbList` o `FAQPage` cuando aplica: **4 pts**<br>• `llms.txt` en la raíz con resumen limpio en Markdown: **3 pts**<br>• Bloques extractables para AI Overviews (definición directa en 30–50 palabras, listas/tablas): **3 pts** |
| **4. Core Web Vitals & Rendimiento** | **20 pts** | • **LCP ≤ 2.5s** (imagen hero optimizada WebP/AVIF + `fetchpriority="high"`, sin bloqueo de render): **7 pts**<br>• **INP < 200ms** (JS modular/code-splitting, sin tareas largas en hilo principal): **7 pts**<br>• **CLS < 0.1** (`width`/`height` o `aspect-ratio` en imágenes/medios, `font-display: swap`): **6 pts** |
| **5. E-E-A-T & Arquitectura de Contenido** | **15 pts** | • Alineación clara con intención de búsqueda y propuesta de valor única (sin texto genérico de IA): **5 pts**<br>• Señales de confianza y autoría (Sobre nosotros, Contacto, Privacidad, Autor/Experto verificable): **5 pts**<br>• Arquitectura de Topic Clusters / enlazado interno con anchor text descriptivo + `alt` en imágenes: **5 pts** |

---

## Escala de Calificación

- **90–100:** Listo para competir por el **Top 1** y citaciones en AI Overviews.
- **75–89:** Base sólida; requiere optimización quirúrgica (Schema, GEO, CWV o clusters).
- **50–74:** Problemas estructurales moderados/altos que frenan el posicionamiento.
- **0–49:** **Estado Crítico** (típico de sitios IA en CSR puro sin metadatos ni renderizado inicial). Invisible para bots de IA y penalizado en rastreo.
