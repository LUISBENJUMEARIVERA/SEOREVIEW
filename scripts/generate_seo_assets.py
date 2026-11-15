#!/usr/bin/env python3
"""
Generate production-ready robots.txt, sitemap.xml, and llms.txt in a target directory.

Usage:
  python generate_seo_assets.py --out ./public --base-url https://tusitio.com \
    --brand "Mi Marca" --summary "Descripción breve." --routes / /servicios /contacto
"""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path


def build_robots_txt(base_url: str) -> str:
    return (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /api/\n"
        "Disallow: /admin/\n\n"
        "User-agent: OAI-SearchBot\n"
        "Allow: /\n\n"
        "User-agent: ChatGPT-User\n"
        "Allow: /\n\n"
        "User-agent: Claude-SearchBot\n"
        "Allow: /\n\n"
        "User-agent: PerplexityBot\n"
        "Allow: /\n\n"
        f"Sitemap: {base_url}/sitemap.xml\n"
    )


def build_sitemap_xml(base_url: str, routes: list[str]) -> str:
    today = date.today().isoformat()
    urls = []
    for r in routes:
        clean = r if r.startswith("/") else f"/{r}"
        loc = base_url if clean == "/" else f"{base_url}{clean}"
        priority = "1.0" if clean == "/" else "0.8"
        urls.append(
            f"  <url>\n"
            f"    <loc>{loc}</loc>\n"
            f"    <lastmod>{today}</lastmod>\n"
            f"    <changefreq>weekly</changefreq>\n"
            f"    <priority>{priority}</priority>\n"
            f"  </url>"
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )


def build_llms_txt(brand: str, summary: str, base_url: str, routes: list[str]) -> str:
    links = []
    for r in routes:
        clean = r if r.startswith("/") else f"/{r}"
        loc = base_url if clean == "/" else f"{base_url}{clean}"
        label = "Inicio" if clean == "/" else clean.strip("/").replace("-", " ").title()
        links.append(f"- [{label}]({loc})")
    return (
        f"# {brand}\n\n"
        f"> {summary}\n\n"
        "## Páginas Principales\n"
        + "\n".join(links)
        + "\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Genera robots.txt, sitemap.xml y llms.txt")
    parser.add_argument("--out", type=Path, required=True, help="Carpeta de salida (ej. ./public)")
    parser.add_argument("--base-url", required=True, help="URL base sin barra final (ej. https://tusitio.com)")
    parser.add_argument("--brand", required=True, help="Nombre de la marca o sitio")
    parser.add_argument("--summary", required=True, help="Resumen de 1-2 frases para llms.txt")
    parser.add_argument("--routes", nargs="+", default=["/"], help="Lista de rutas públicas")
    args = parser.parse_args()

    base = args.base_url.rstrip("/")
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "robots.txt").write_text(build_robots_txt(base), encoding="utf-8")
    (args.out / "sitemap.xml").write_text(build_sitemap_xml(base, args.routes), encoding="utf-8")
    (args.out / "llms.txt").write_text(
        build_llms_txt(args.brand, args.summary, base, args.routes), encoding="utf-8"
    )
    print(f"Generados robots.txt, sitemap.xml y llms.txt en {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
