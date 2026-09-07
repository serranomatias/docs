#!/usr/bin/env python3
"""Control de calidad de las páginas de docs.contactship.ai.

Uso: python3 .internal/qa/check-pages.py [--strict]

Revisa:
- que todas las páginas de docs.json existan en disco y que no haya páginas huérfanas;
- frontmatter con title y description;
- páginas de producto con import y bloque <Availability>;
- bloque de preguntas frecuentes (AccordionGroup) en páginas de producto;
- formato de los marcadores de captura;
- enlaces internos absolutos que apunten a páginas existentes;
- palabras prohibidas (proveedores internos, rutas de código, tickets, emojis, exclamaciones);
- paridad ES/EN según el mapa de docs.json.
"""
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
for argument in sys.argv[1:]:
    if argument.startswith("--root="):
        ROOT = os.path.abspath(argument.split("=", 1)[1])
STRICT = "--strict" in sys.argv

with open(os.path.join(ROOT, "docs.json"), encoding="utf-8") as fh:
    DOCS = json.load(fh)


def nav_pages(root=None):
    pages = []

    def walk(node):
        if isinstance(node, dict):
            for key in ("languages", "tabs", "groups", "pages"):
                for child in node.get(key, []):
                    if key == "pages" and isinstance(child, str):
                        pages.append(child)
                    elif isinstance(child, (dict, list)):
                        walk(child)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    walk(DOCS["navigation"] if root is None else root)
    return pages


PAGES = nav_pages()
PAGE_SET = set(PAGES)

PRODUCT_PREFIXES_ES = ("es/comenzar/", "es/agentes-de-voz/", "es/agentes-de-texto/", "es/mensajes/", "es/llamadas/",
                       "es/contactos/", "es/contact-center/", "es/enrutamiento/", "es/reportes/", "es/organizacion/",
                       "es/facturacion/", "es/integraciones/")
PRODUCT_PREFIXES_EN = ("en/get-started/", "en/voice-agents/", "en/text-agents/", "en/messages/", "en/calls/",
                       "en/contacts/", "en/contact-center/", "en/lead-routing/", "en/reports/", "en/organization/",
                       "en/billing/", "en/integrations/")
PRODUCT_PREFIXES = PRODUCT_PREFIXES_ES + PRODUCT_PREFIXES_EN
NO_AVAILABILITY = {"es/comenzar/glosario", "en/get-started/glossary", "es/comenzar/que-es-contactship",
                   "en/get-started/what-is-contactship", "es/comenzar/soporte", "en/get-started/support",
                   "es/comenzar/conceptos", "en/get-started/concepts"}

FORBIDDEN = [
    (r"\bRetell\b", "proveedor interno"), (r"\bTwilio\b", "proveedor interno"), (r"\bElevenLabs\b", "proveedor interno"),
    (r"\bSupabase\b", "proveedor interno"), (r"\bClickUp\b", "ticket interno"), (r"\bsrc/[a-zA-Z]", "ruta de código"),
    (r"\.tsx?\b", "archivo de código"), (r"[\U0001F300-\U0001FAFF☀-➿]", "emoji"),
]
EXCLAMATION = re.compile(r"[!¡]")
CAPTURE = re.compile(r"\{/\*\s*(captura|clip):\s*(images/[a-z0-9\-/]+-(es|en)\.(png|mp4))\s*\|\s*[^|]+\|\s*app:\s*[^*]+\*/\}")
CAPTURE_LOOSE = re.compile(r"\{/\*\s*(captura|clip):")
LINK = re.compile(r"\]\((/(?:es|en|api-reference)/[^)#?\s]+)")
HREF = re.compile(r"href=\"(/(?:es|en|api-reference)/[^\"#?]+)\"")

errors, warnings = [], []


def err(page, msg):
    errors.append(f"{page}: {msg}")


def warn(page, msg):
    warnings.append(f"{page}: {msg}")


def frontmatter(text):
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    fm = {}
    for line in text[3:end].splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip("'\"")
    return fm


def strip_code(text):
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"`[^`]*`", "", text)
    text = re.sub(r"\{/\*.*?\*/\}", "", text, flags=re.S)
    return text


# 1. nav vs disk
for p in sorted(PAGE_SET):
    if not os.path.exists(os.path.join(ROOT, p + ".mdx")):
        err(p, "está en docs.json pero no existe el archivo")

on_disk = []
for base in ("es", "en", "api-reference"):
    for dirpath, _, files in os.walk(os.path.join(ROOT, base)):
        for f in files:
            if f.endswith(".mdx"):
                rel = os.path.relpath(os.path.join(dirpath, f), ROOT)[:-4]
                on_disk.append(rel)
for p in on_disk:
    if p not in PAGE_SET:
        warn(p, "existe en disco pero no está en docs.json (página huérfana)")

# 2. per-page checks
for p in on_disk:
    path = os.path.join(ROOT, p + ".mdx")
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    fm = frontmatter(text)
    if not fm.get("title"):
        err(p, "sin title en el frontmatter")
    if not fm.get("description") and not p.startswith("api-reference/endpoint/"):
        err(p, "sin description en el frontmatter")
    is_product = p.startswith(PRODUCT_PREFIXES) and p not in NO_AVAILABILITY
    if is_product:
        if "from '/snippets/availability.mdx'" not in text:
            err(p, "falta el import de Availability")
        if "<Availability" not in text:
            err(p, "falta el bloque <Availability")
        if "<AccordionGroup" not in text:
            err(p, "falta el bloque de preguntas frecuentes (AccordionGroup)")
        lang = "es" if p.startswith("es/") else "en"
        if f'lang="{lang}"' not in text and "<Availability" in text:
            err(p, f'el bloque Availability no tiene lang="{lang}"')
    if p.startswith(PRODUCT_PREFIXES):
        loose = len(CAPTURE_LOOSE.findall(text))
        good = len(CAPTURE.findall(text))
        if loose != good:
            err(p, f"{loose - good} marcador(es) de captura con formato incorrecto")
    prose = strip_code(text)
    for pattern, label in FORBIDDEN:
        for m in re.finditer(pattern, prose):
            err(p, f"{label}: '{m.group(0)}'")
            break
    for m in EXCLAMATION.finditer(prose):
        start = max(0, m.start() - 30)
        warn(p, f"signo de exclamación: …{prose[start:m.end()+10].strip()!r}")
        break
    for m in list(LINK.finditer(text)) + list(HREF.finditer(text)):
        target = m.group(1).rstrip("/")
        if not os.path.isfile(os.path.join(ROOT, target[1:] + ".mdx")):
            err(p, f"enlace interno roto: {target}")
    if not p.startswith("api-reference/"):
        for m in re.finditer(r"\]\(((?!http|/|#|mailto)[^)]+)\)", text):
            err(p, f"enlace relativo (deben ser absolutos con /es o /en): {m.group(1)}")
    if p.startswith("es/"):
        for m in re.finditer(r"\b(usted|ustedes)\b", prose):
            warn(p, "usa 'usted'")
            break

# 3. ES/EN parity by nav position
def lang_pages(lang):
    for l in DOCS["navigation"]["languages"]:
        if l["language"] == lang:
            return nav_pages(l)
    return []


es_pages = [p for p in lang_pages("es") if p.startswith("es/")]
en_pages = [p for p in lang_pages("en") if p.startswith("en/")]
if len(es_pages) != len(en_pages):
    err("docs.json", f"paridad ES/EN: {len(es_pages)} páginas ES vs {len(en_pages)} EN")

# A menu entry or redirect is not evidence that a target file exists.
redirect_sources = set()
for redirect in DOCS.get("redirects", []):
    source, destination = redirect.get("source", ""), redirect.get("destination", "")
    if source in redirect_sources:
        err("docs.json", f"redirección duplicada: {source}")
    redirect_sources.add(source)
    if source == destination:
        err("docs.json", f"redirección a sí misma: {source}")
    if not destination.startswith("/") or not os.path.isfile(os.path.join(ROOT, destination.lstrip("/") + ".mdx")):
        err("docs.json", f"destino de redirección inexistente: {destination}")
for lang in ("es", "en"):
    entries = lang_pages(lang)
    if len(entries) != len(set(entries)):
        err("docs.json", f"páginas repetidas dentro de la navegación {lang}")

print(f"Páginas en docs.json: {len(PAGE_SET)} · en disco: {len(on_disk)}")
print(f"Errores: {len(errors)} · Avisos: {len(warnings)}")
for e in errors:
    print("ERROR", e)
if STRICT or "--warnings" in sys.argv:
    for w in warnings:
        print("AVISO", w)
sys.exit(1 if errors or (STRICT and warnings) else 0)
