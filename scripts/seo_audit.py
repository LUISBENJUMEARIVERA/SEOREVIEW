#!/usr/bin/env python3
"""
SEO Top 1 Architect — Automated SEO + GEO + AI-Site Audit Script.

Supports two modes:
  1. Local project directory (--path <dir>): Detects framework (Vite/React CSR,
     Next.js, Astro, static HTML), discovers routes, checks index.html,
     robots.txt, sitemap.xml, llms.txt, dynamic metadata, JSON-LD, <div onClick>
     anti-patterns, <img> alt/dimension attributes, and CSS font-display: swap.
  2. Live URL (--url <https://...>): Simulates Wave-1 Googlebot & AI crawlers
     (raw HTTP HTML without JS execution), checks empty CSR shell, meta tags,
     canonical, heading hierarchy, JSON-LD validity, robots.txt, sitemap.xml,
     and llms.txt.

Output formats: --format json (default) or --format markdown.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


@dataclass
class HTMLSignals:
    title: str = ""
    meta_description: str = ""
    meta_robots: str = ""
    canonical: str = ""
    lang: str = ""
    og_tags: dict[str, str] = field(default_factory=dict)
    twitter_tags: dict[str, str] = field(default_factory=dict)
    headings: list[tuple[str, str]] = field(default_factory=list)
    images: list[dict[str, str]] = field(default_factory=list)
    links: list[str] = field(default_factory=list)
    json_ld_raw: list[str] = field(default_factory=list)
    has_main: bool = False
    has_header: bool = False
    has_nav: bool = False
    has_footer: bool = False
    has_fetchpriority_high: bool = False
    visible_text_words: int = 0
    empty_root_shell: bool = False


class SEOHTMLParser(HTMLParser):
    """Lightweight HTML parser to extract SEO, semantic, CWV, and GEO signals."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.signals = HTMLSignals()
        self._in_title = False
        self._title_parts: list[str] = []
        self._active_heading: str | None = None
        self._heading_parts: list[str] = []
        self._in_json_ld = False
        self._json_ld_parts: list[str] = []
        self._skip_text_depth = 0
        self._text_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {k.lower(): (v or "") for k, v in attrs}
        t = tag.lower()

        if t == "html" and "lang" in attr_map:
            self.signals.lang = attr_map["lang"].strip()
        elif t == "title":
            self._in_title = True
            self._title_parts = []
        elif t == "meta":
            name = attr_map.get("name", "").lower()
            prop = attr_map.get("property", "").lower()
            content = attr_map.get("content", "").strip()
            if name == "description":
                self.signals.meta_description = content
            elif name == "robots":
                self.signals.meta_robots = content
            elif prop.startswith("og:"):
                self.signals.og_tags[prop] = content
            elif name.startswith("twitter:"):
                self.signals.twitter_tags[name] = content
        elif t == "link":
            rel = attr_map.get("rel", "").lower()
            if "canonical" in rel.split():
                self.signals.canonical = attr_map.get("href", "").strip()
            if attr_map.get("fetchpriority", "").lower() == "high":
                self.signals.has_fetchpriority_high = True
        elif t in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._active_heading = t
            self._heading_parts = []
        elif t == "img":
            if attr_map.get("fetchpriority", "").lower() == "high":
                self.signals.has_fetchpriority_high = True
            self.signals.images.append(
                {
                    "src": attr_map.get("src", ""),
                    "alt": "__MISSING__" if "alt" not in attr_map else attr_map.get("alt", ""),
                    "width": attr_map.get("width", ""),
                    "height": attr_map.get("height", ""),
                }
            )
        elif t == "a" and "href" in attr_map:
            self.signals.links.append(attr_map["href"].strip())
        elif t == "script":
            if attr_map.get("type", "").lower() == "application/ld+json":
                self._in_json_ld = True
                self._json_ld_parts = []
            self._skip_text_depth += 1
        elif t in ("style", "noscript", "svg"):
            self._skip_text_depth += 1
        elif t == "main":
            self.signals.has_main = True
        elif t == "header":
            self.signals.has_header = True
        elif t == "nav":
            self.signals.has_nav = True
        elif t == "footer":
            self.signals.has_footer = True

    def handle_endtag(self, tag: str) -> None:
        t = tag.lower()
        if t == "title" and self._in_title:
            self._in_title = False
            self.signals.title = " ".join("".join(self._title_parts).split())
        elif t == self._active_heading:
            text = " ".join("".join(self._heading_parts).split())
            self.signals.headings.append((t, text))
            self._active_heading = None
        elif t == "script":
            if self._in_json_ld:
                self._in_json_ld = False
                self.signals.json_ld_raw.append("".join(self._json_ld_parts).strip())
            if self._skip_text_depth > 0:
                self._skip_text_depth -= 1
        elif t in ("style", "noscript", "svg") and self._skip_text_depth > 0:
            self._skip_text_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self._title_parts.append(data)
        if self._active_heading:
            self._heading_parts.append(data)
        if self._in_json_ld:
            self._json_ld_parts.append(data)
        if self._skip_text_depth == 0:
            self._text_parts.append(data)

    def finalize(self, raw_html: str) -> HTMLSignals:
        text = " ".join("".join(self._text_parts).split())
        self.signals.visible_text_words = len(text.split()) if text else 0
        root_shell_match = re.search(
            r'<div\s+id=["\'](root|app|__next)["\']\s*>\s*</div>', raw_html, re.I
        )
        if root_shell_match and self.signals.visible_text_words < 40:
            self.signals.empty_root_shell = True
        return self.signals


def parse_html(raw_html: str) -> HTMLSignals:
    parser = SEOHTMLParser()
    parser.feed(raw_html)
    parser.close()
    return parser.finalize(raw_html)


def check_heading_hierarchy(headings: list[tuple[str, str]]) -> list[str]:
    """Detect skipped heading levels (e.g. H1 -> H3 without H2)."""
    issues: list[str] = []
    prev_level = 0
    for tag, text in headings:
        level = int(tag[1])
        if prev_level and level > prev_level + 1:
            issues.append(f"Salto de jerarquía: H{prev_level} -> H{level} ('{text[:40]}')")
        prev_level = level
    return issues


def validate_json_ld(blocks: list[str]) -> tuple[int, list[str]]:
    valid = 0
    errors: list[str] = []
    for idx, block in enumerate(blocks, 1):
        try:
            data = json.loads(block)
            if isinstance(data, dict) and ("@type" in data or "@graph" in data):
                valid += 1
            else:
                errors.append(f"JSON-LD #{idx}: falta '@type' o '@graph'")
        except json.JSONDecodeError as exc:
            errors.append(f"JSON-LD #{idx}: JSON inválido ({exc})")
    return valid, errors


def fetch_text(url: str, timeout: int = 12) -> tuple[int, str]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (compatible; SEOTop1AuditBot/1.1; +https://developers.google.com/search)"
            )
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            charset = resp.headers.get_content_charset() or "utf-8"
            return resp.status, resp.read().decode(charset, errors="replace")
    except urllib.error.HTTPError as err:
        return err.code, ""
    except Exception:
        return 0, ""


def audit_live_url(url: str) -> dict[str, Any]:
    parsed = urllib.parse.urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}"

    status, html = fetch_text(url)
    if status == 0 or not html:
        return {"mode": "url", "url": url, "error": f"No se pudo obtener HTML (HTTP {status})"}

    sig = parse_html(html)
    valid_ld, ld_errors = validate_json_ld(sig.json_ld_raw)
    hierarchy_issues = check_heading_hierarchy(sig.headings)

    robots_status, robots_txt = fetch_text(f"{base}/robots.txt")
    sitemap_status, sitemap_xml = fetch_text(f"{base}/sitemap.xml")
    llms_status, llms_txt = fetch_text(f"{base}/llms.txt")

    h1s = [text for tag, text in sig.headings if tag == "h1"]
    imgs_missing_alt = [i["src"] for i in sig.images if i["alt"] == "__MISSING__"]
    imgs_missing_dims = [i["src"] for i in sig.images if not i["width"] or not i["height"]]

    findings: list[dict[str, str]] = []
    score = 100

    if sig.empty_root_shell:
        score -= 25
        findings.append(
            {
                "severity": "P0-BLOQUEANTE",
                "area": "Renderizado CSR",
                "detail": "HTML inicial es un cascarón vacío (<div id='root'></div>). Invisible para bots de IA y penalizado en Oleada 1.",
            }
        )
    if "noindex" in sig.meta_robots.lower():
        score -= 25
        findings.append(
            {
                "severity": "P0-BLOQUEANTE",
                "area": "Indexabilidad",
                "detail": f"Meta robots contiene 'noindex': {sig.meta_robots}",
            }
        )
    if not sig.title:
        score -= 10
        findings.append({"severity": "P1-ALTO", "area": "Title", "detail": "Falta etiqueta <title>."})
    elif not (30 <= len(sig.title) <= 65):
        score -= 3
        findings.append(
            {
                "severity": "P2-MEDIO",
                "area": "Title",
                "detail": f"Longitud de <title> ({len(sig.title)} chars) fuera del rango óptimo 50–60.",
            }
        )

    if not sig.meta_description:
        score -= 8
        findings.append(
            {"severity": "P1-ALTO", "area": "Meta Description", "detail": "Falta meta description."}
        )
    if not sig.canonical:
        score -= 6
        findings.append(
            {"severity": "P1-ALTO", "area": "Canonical", "detail": "Falta <link rel='canonical'>."}
        )
    if len(h1s) == 0:
        score -= 8
        findings.append({"severity": "P1-ALTO", "area": "H1", "detail": "No hay ningún <h1> en el HTML inicial."})
    elif len(h1s) > 1:
        score -= 4
        findings.append({"severity": "P2-MEDIO", "area": "H1", "detail": f"Múltiples <h1> ({len(h1s)})."})

    for issue in hierarchy_issues[:3]:
        score -= 2
        findings.append({"severity": "P2-MEDIO", "area": "Jerarquía H1-H6", "detail": issue})

    if valid_ld == 0:
        score -= 10
        findings.append(
            {"severity": "P1-ALTO", "area": "JSON-LD", "detail": "Sin datos estructurados Schema.org válidos."}
        )
    for err in ld_errors:
        score -= 3
        findings.append({"severity": "P2-MEDIO", "area": "JSON-LD", "detail": err})

    if robots_status != 200 or not robots_txt.strip():
        score -= 5
        findings.append({"severity": "P1-ALTO", "area": "robots.txt", "detail": "Falta /robots.txt (HTTP != 200)."})
    if sitemap_status != 200 or "<urlset" not in sitemap_xml.lower():
        score -= 5
        findings.append({"severity": "P1-ALTO", "area": "sitemap.xml", "detail": "Falta /sitemap.xml válido."})
    if llms_status != 200 or not llms_txt.strip():
        score -= 3
        findings.append({"severity": "P2-MEDIO", "area": "GEO / llms.txt", "detail": "Falta /llms.txt para agentes de IA."})

    if imgs_missing_alt:
        score -= 4
        findings.append(
            {
                "severity": "P2-MEDIO",
                "area": "Accesibilidad/SEO Imágenes",
                "detail": f"{len(imgs_missing_alt)} imágenes sin atributo alt.",
            }
        )
    if imgs_missing_dims:
        score -= 3
        findings.append(
            {
                "severity": "P2-MEDIO",
                "area": "CWV / CLS",
                "detail": f"{len(imgs_missing_dims)} imágenes sin width/height explícitos.",
            }
        )

    return {
        "mode": "url",
        "url": url,
        "http_status": status,
        "score": max(0, score),
        "signals": {
            "title": sig.title,
            "title_length": len(sig.title),
            "meta_description_length": len(sig.meta_description),
            "canonical": sig.canonical,
            "lang": sig.lang,
            "h1_count": len(h1s),
            "h1_texts": h1s,
            "heading_hierarchy_issues": len(hierarchy_issues),
            "visible_words_raw_html": sig.visible_text_words,
            "empty_root_shell": sig.empty_root_shell,
            "json_ld_valid_count": valid_ld,
            "og_tags_count": len(sig.og_tags),
            "twitter_tags_count": len(sig.twitter_tags),
            "robots_txt_http": robots_status,
            "sitemap_xml_http": sitemap_status,
            "llms_txt_http": llms_status,
        },
        "findings": findings,
    }


def detect_stack(root: Path) -> str:
    pkg_path = root / "package.json"
    if not pkg_path.exists():
        return "static-html-or-other"
    try:
        pkg = json.loads(pkg_path.read_text(encoding="utf-8", errors="replace"))
    except json.JSONDecodeError:
        return "unknown-node"
    deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
    if "next" in deps:
        return "nextjs"
    if "astro" in deps:
        return "astro"
    if "vite" in deps and "react" in deps:
        return "vite-react-spa"
    if "vite" in deps:
        return "vite-other"
    return "node-custom"


def discover_routes(root: Path, stack: str) -> list[str]:
    routes: set[str] = set()
    skip_dirs = {"node_modules", ".git", "dist", "build", ".next", ".venv"}

    if stack == "nextjs":
        for p in root.rglob("page.*"):
            if any(part in skip_dirs for part in p.parts):
                continue
            rel = str(p.parent.relative_to(root)).replace("\\", "/")
            rel = re.sub(r"^(src/)?app", "", rel) or "/"
            routes.add(rel if rel.startswith("/") else f"/{rel}")
    elif stack == "astro":
        pages_dir = root / "src" / "pages"
        if pages_dir.exists():
            for p in pages_dir.rglob("*.astro"):
                rel = "/" + str(p.relative_to(pages_dir)).replace("\\", "/")
                rel = re.sub(r"/index\.astro$|\.astro$", "", rel) or "/"
                routes.add(rel)
    else:
        for p in root.rglob("*.tsx"):
            if any(part in skip_dirs for part in p.parts):
                continue
            txt = p.read_text(encoding="utf-8", errors="replace")
            for m in re.findall(r'<Route\b[^>]*path\s*=\s*["\']([^"\']+)["\']', txt):
                routes.add(m)
    return sorted(routes)


def audit_local_path(target: Path) -> dict[str, Any]:
    if not target.exists():
        return {"mode": "path", "path": str(target), "error": "La ruta no existe."}

    stack = detect_stack(target)
    discovered_routes = discover_routes(target, stack)
    findings: list[dict[str, str]] = []
    score = 100

    index_candidates = [target / "index.html", target / "public" / "index.html"]
    index_file = next((p for p in index_candidates if p.exists()), None)
    if index_file:
        raw_html = index_file.read_text(encoding="utf-8", errors="replace")
        index_signals = parse_html(raw_html)
        if stack == "vite-react-spa" and index_signals.empty_root_shell:
            score -= 22
            findings.append(
                {
                    "severity": "P0-BLOQUEANTE",
                    "area": "Arquitectura IA / CSR",
                    "detail": "Proyecto Vite+React SPA con index.html vacío (<div id='root'></div>). Requiere SSR/SSG o pre-rendering.",
                }
            )
        if not index_signals.title:
            score -= 8
            findings.append({"severity": "P1-ALTO", "area": "Title", "detail": "index.html sin <title>."})
        if not index_signals.meta_description:
            score -= 6
            findings.append(
                {"severity": "P1-ALTO", "area": "Meta Description", "detail": "index.html sin meta description."}
            )
        if not index_signals.json_ld_raw:
            score -= 8
            findings.append(
                {"severity": "P1-ALTO", "area": "JSON-LD", "detail": "Sin Schema.org JSON-LD detectado en index.html."}
            )

    has_robots = any((target / p).exists() for p in ("public/robots.txt", "robots.txt", "app/robots.ts"))
    has_sitemap = any(
        (target / p).exists() for p in ("public/sitemap.xml", "sitemap.xml", "app/sitemap.ts")
    )
    has_llms = any((target / p).exists() for p in ("public/llms.txt", "llms.txt"))

    if not has_robots:
        score -= 6
        findings.append({"severity": "P1-ALTO", "area": "robots.txt", "detail": "Falta robots.txt (o app/robots.ts)."})
    if not has_sitemap:
        score -= 6
        findings.append({"severity": "P1-ALTO", "area": "sitemap.xml", "detail": "Falta sitemap.xml (o app/sitemap.ts)."})
    if not has_llms:
        score -= 3
        findings.append({"severity": "P2-MEDIO", "area": "GEO / llms.txt", "detail": "Falta public/llms.txt."})

    div_onclick_hits = 0
    img_without_alt_hits = 0
    has_dynamic_head = False
    has_font_swap = False
    code_exts = {".tsx", ".jsx", ".ts", ".js", ".astro", ".html"}
    skip_dirs = {"node_modules", ".git", "dist", "build", ".next", ".venv"}

    for file_path in target.rglob("*"):
        if any(part in skip_dirs for part in file_path.parts):
            continue
        if not file_path.is_file():
            continue
        suffix = file_path.suffix.lower()
        if suffix in (".css", ".scss"):
            css = file_path.read_text(encoding="utf-8", errors="replace")
            if "font-display" in css and "swap" in css:
                has_font_swap = True
        elif suffix in code_exts:
            content = file_path.read_text(encoding="utf-8", errors="replace")
            if re.search(r"<(div|span)\b[^>]*onClick\s*=\s*\{[^}]*navigate\(", content):
                div_onclick_hits += 1
            for img_tag in re.findall(r"<img\b[^>]*>", content, flags=re.I):
                if "alt=" not in img_tag.lower():
                    img_without_alt_hits += 1
            if "react-helmet" in content or "generateMetadata" in content or "export const metadata" in content:
                has_dynamic_head = True
            if "display=swap" in content:
                has_font_swap = True

    if div_onclick_hits > 0:
        score -= 8
        findings.append(
            {
                "severity": "P0-BLOQUEANTE",
                "area": "Enlazado Interno",
                "detail": f"Se detectaron {div_onclick_hits} archivos usando <div/span onClick={{navigate(...)}}> en lugar de <Link>/<a href>.",
            }
        )
    if img_without_alt_hits > 0:
        score -= 4
        findings.append(
            {
                "severity": "P2-MEDIO",
                "area": "Imágenes",
                "detail": f"Se detectaron {img_without_alt_hits} etiquetas <img> sin atributo alt.",
            }
        )
    if stack == "vite-react-spa" and not has_dynamic_head:
        score -= 8
        findings.append(
            {
                "severity": "P1-ALTO",
                "area": "Metadatos por Ruta",
                "detail": "SPA React sin react-helmet-async ni gestión dinámica de <head> por ruta.",
            }
        )

    return {
        "mode": "path",
        "path": str(target),
        "stack_detected": stack,
        "discovered_routes": discovered_routes,
        "score": max(0, score),
        "checks": {
            "robots_txt": has_robots,
            "sitemap_xml": has_sitemap,
            "llms_txt": has_llms,
            "dynamic_head_detected": has_dynamic_head,
            "font_display_swap_detected": has_font_swap,
            "div_onclick_navigation_files": div_onclick_hits,
            "img_without_alt_count": img_without_alt_hits,
        },
        "findings": findings,
    }


def format_markdown(result: dict[str, Any]) -> str:
    if "error" in result:
        return f"## Error de Auditoría\n\n- **Objetivo:** `{result.get('url') or result.get('path')}`\n- **Detalle:** {result['error']}"

    target = result.get("url") or result.get("path")
    lines = [
        f"## Diagnóstico SEO + GEO (`{target}`)",
        "",
        f"**Score Técnico Preliminar:** `{result['score']}/100`",
        "",
        "### Hallazgos",
    ]
    if not result["findings"]:
        lines.append("- Sin hallazgos técnicos críticos detectados.")
    else:
        for f in result["findings"]:
            lines.append(f"- **[{f['severity']}] {f['area']}:** {f['detail']}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Auditoría SEO + GEO + Sitios IA")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--path", type=Path, help="Ruta local del proyecto web")
    group.add_argument("--url", type=str, help="URL en vivo a auditar (https://...)")
    parser.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="json",
        help="Formato de salida (default: json)",
    )
    args = parser.parse_args()

    result = audit_local_path(args.path) if args.path else audit_live_url(args.url)
    if args.format == "markdown":
        print(format_markdown(result))
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
