"""
Sestavení a kontrola docs_for_agents/style_guide.md.

LLM píše jen sekce 1–4 a 7. Sekce 5 (barvy) a 6 (struktura kapitoly) vkládá Python,
aby je LLM nemohlo zkomolit. Modul záměrně neimportuje crewai ani crew.config,
takže kontrolu lze spustit i bez API klíče:

    .venv\\Scripts\\python.exe -m crew.style_guide            # zkontroluje style_guide.md
"""

import colorsys
import hashlib
import re
import sys
from datetime import date
from pathlib import Path

from crew.prompts import CHAPTER_STRUCTURE

PROJECT_NAME = "Statistika pohledem geometra"
SCSS_PATH = "hag_custom.scss"
SOURCE_FILES = ["_quarto.yml", SCSS_PATH]   # při jejich změně je style guide zastaralý

LLM_SECTIONS = [1, 2, 3, 4, 7]
SECTION_TITLES = {
    1: "Celkový styl",
    2: "Dvojjazyčnost",
    3: "Dark / Light mode",
    4: "Responsive design",
    5: "Barevné schéma pro OJS",
    6: "Struktura kapitoly",
    7: "Callout třídy",
}

FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")
SECTION_RE = re.compile(r"^## (\d+)\.\s")
HASH_LINE_RE = re.compile(r"^\s+(\S+): ([0-9a-f]{64})\s*$")


# ----------------- Pomocné funkce -----------------

def file_sha256(path: str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _next_fence_state(open_fence, line: str):
    """Stav po řádku `line`. open_fence je None (mimo blok) nebo (znak, délka) otevřené ohrady.
    Vrací (nový_stav, je_řádek_ohrada)."""
    match = FENCE_RE.match(line)
    if not match:
        return open_fence, False
    marker, rest = match.group(1), match.group(2)
    if open_fence is None:
        return (marker[0], len(marker)), True
    # Ohradu zavře jen stejný znak, alespoň stejná délka a nic za ní
    if marker[0] == open_fence[0] and len(marker) >= open_fence[1] and not rest.strip():
        return None, True
    return open_fence, False   # např. ``` uvnitř bloku ````: je to jen obsah


def iter_lines_with_fence_state(text: str):
    """Vrací (řádek, je_uvnitř_kódového_bloku). Řádky ohrad samotné se počítají jako uvnitř."""
    open_fence = None
    for line in text.splitlines():
        before = open_fence
        open_fence, is_fence = _next_fence_state(open_fence, line)
        yield line, is_fence or before is not None


def fences_balanced(text: str) -> bool:
    """True, pokud po posledním řádku nezůstal otevřený kódový blok."""
    open_fence = None
    for line in text.splitlines():
        open_fence, _ = _next_fence_state(open_fence, line)
    return open_fence is None


def split_sections(text: str) -> dict[int, str]:
    """Rozdělí text podle číslovaných nadpisů '## N. ...' mimo kódové bloky.
    Vrací {N: obsah sekce bez nadpisu}."""
    sections: dict[int, list[str]] = {}
    current = None
    for line, inside in iter_lines_with_fence_state(text):
        match = None if inside else SECTION_RE.match(line)
        if match:
            current = int(match.group(1))
            if current in sections:
                raise ValueError(f"Sekce {current} je v textu dvakrát.")
            sections[current] = []
        elif current is not None:
            sections[current].append(line)
    return {n: "\n".join(lines).strip() for n, lines in sections.items()}


def section_order(text: str) -> list[int]:
    order = []
    for line, inside in iter_lines_with_fence_state(text):
        match = None if inside else SECTION_RE.match(line)
        if match:
            order.append(int(match.group(1)))
    return order


# ----------------- Sekce 5: barvy ze SCSS -----------------

def _darken(hex_color: str, percent: float) -> str:
    """Stejně jako Sass darken(): sníží HSL světlost o `percent` procentních bodů."""
    r, g, b = (int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    l = max(0.0, l - percent / 100)
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return "#" + "".join(f"{round(c * 255):02x}" for c in (r, g, b))


def _lighten(hex_color: str, percent: float) -> str:
    return _darken(hex_color, -percent) if percent else hex_color


def _camel_case(scss_name: str) -> str:
    first, *rest = scss_name.split("-")
    return first + "".join(part.capitalize() for part in rest)


def read_scss_colors(scss_path: str = SCSS_PATH) -> dict[str, str]:
    """Načte barevné proměnné ze sekce scss:defaults (hex, darken(), lighten())."""
    colors: dict[str, str] = {}
    var_re = re.compile(r"^\$([\w-]+):\s*([^;]+);")
    func_re = re.compile(r"(darken|lighten)\(\$([\w-]+),\s*([\d.]+)%\)")
    for line in Path(scss_path).read_text(encoding="utf-8").splitlines():
        match = var_re.match(line.strip())
        if not match:
            continue
        name, value = match.group(1), match.group(2).strip()
        if re.fullmatch(r"#[0-9a-fA-F]{6}", value):
            colors[name] = value.upper()
            continue
        func = func_re.fullmatch(value)
        if func and func.group(2) in colors:
            base = colors[func.group(2)]
            amount = float(func.group(3))
            new = _darken(base, amount) if func.group(1) == "darken" else _lighten(base, amount)
            colors[name] = new.upper()
    return colors


def build_colors_section(scss_path: str = SCSS_PATH) -> str:
    colors = read_scss_colors(scss_path)
    if not colors:
        raise ValueError(f"V {scss_path} nebyla nalezena žádná barva.")
    width = max(len(_camel_case(n)) for n in colors)
    lines = [f'  {_camel_case(n) + ":":<{width + 1}} "{v}",   // ${n}' for n, v in colors.items()]
    return "\n".join([
        f"Hodnoty jsou automaticky převzaté z `{scss_path}` (sekce `scss:defaults`).",
        "Dočasné řešení: později je nahradí sdílený modul, který čte barvy přímo z CSS",
        "(viz `docs_for_agents/zadani_revize.md`, B2 a B3).",
        "",
        "```js",
        "COLORS = ({",
        *lines,
        "})",
        "```",
    ])


# ----------------- Výstup LLM -----------------

def clean_llm_output(raw: str) -> str:
    """Odřízne úvodní větu LLM (vše před prvním nadpisem) a případný obalující ```markdown blok."""
    lines = raw.strip().splitlines()
    start = next((i for i, line in enumerate(lines) if line.startswith("#")), None)
    if start is None:
        raise ValueError("Výstup LLM neobsahuje žádný nadpis.")
    wrapped = any(FENCE_RE.match(line) for line in lines[:start])
    body = lines[start:]
    if wrapped and body and FENCE_RE.match(body[-1]) and not FENCE_RE.match(body[-1]).group(2).strip():
        body = body[:-1]
    return "\n".join(body).strip()


def parse_llm_sections(raw: str) -> dict[int, str]:
    sections = split_sections(clean_llm_output(raw))
    missing = [n for n in LLM_SECTIONS if not sections.get(n)]
    if missing:
        raise ValueError(f"Výstupu LLM chybí (nebo jsou prázdné) sekce: {missing}")
    extra = sorted(set(sections) - set(LLM_SECTIONS))
    if extra:
        print(f"⚠️  LLM vrátilo i sekce {extra} – zahazuji je (vkládá je Python).")
    return {n: sections[n] for n in LLM_SECTIONS}


# ----------------- Sestavení -----------------

def build_header() -> str:
    hashes = "\n".join(f"    {path}: {file_sha256(path)}" for path in SOURCE_FILES)
    return "\n".join([
        "<!--",
        "  GENEROVÁNO automaticky (crew_agents.py, generate_style_guide). Needitovat ručně.",
        "  Sekce 5 a 6 vkládá Python (crew/style_guide.py), ostatní píše LLM.",
        f"  Datum: {date.today().isoformat()}",
        "  Zdroje (sha256):",
        hashes,
        "-->",
    ])


def assemble(llm_sections: dict[int, str]) -> str:
    fixed = {5: build_colors_section(), 6: CHAPTER_STRUCTURE.strip()}
    parts = [build_header(), "", f"# Style Guide: {PROJECT_NAME}", ""]
    for n in range(1, 8):
        body = fixed.get(n) or llm_sections[n]
        parts += [f"## {n}. {SECTION_TITLES[n]}", "", body, ""]
    return "\n".join(parts)


# ----------------- Kontroly -----------------

def validate(text: str) -> list[str]:
    """Vrátí seznam chyb (prázdný = v pořádku)."""
    errors = []
    body_lines = [l for l in text.split("-->", 1)[-1].splitlines() if l.strip()]
    if not body_lines or not body_lines[0].startswith("# "):
        errors.append("Za hlavičkou nenásleduje nadpis H1.")
    if not fences_balanced(text):
        errors.append("Kódové bloky nejsou správně uzavřené (nesouladné ohrady).")
    order = section_order(text)
    if order != list(range(1, 8)):
        errors.append(f"Sekce nejsou 1–7 v daném pořadí, nalezeno: {order}")
    try:
        sections = split_sections(text)
    except ValueError as e:
        return errors + [str(e)]
    if not sections.get(5):
        errors.append("Sekce 5 je prázdná.")
    elif sections[5] != build_colors_section():
        errors.append("Sekce 5 neodpovídá barvám v hag_custom.scss.")
    if sections.get(6) != CHAPTER_STRUCTURE.strip():
        errors.append("Sekce 6 není přesnou kopií CHAPTER_STRUCTURE z crew/prompts.py.")
    if "Havi Notes" in text:
        errors.append("Text obsahuje starý název „Havi Notes“.")
    return errors


def check_sources(text: str) -> list[str]:
    """Porovná sha256 v hlavičce se současnými zdrojovými soubory. Vrátí seznam neshod."""
    stored = {}
    header = text.split("-->", 1)[0] if text.lstrip().startswith("<!--") else ""
    for line in header.splitlines():
        match = HASH_LINE_RE.match(line)
        if match:
            stored[match.group(1)] = match.group(2)
    if not stored:
        return ["Style guide nemá hlavičku se sha256 zdrojů (starý formát)."]
    problems = []
    for path in SOURCE_FILES:
        if stored.get(path) != file_sha256(path):
            problems.append(f"{path} se od vygenerování style guide změnil.")
    return problems


if __name__ == "__main__":
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "docs_for_agents/style_guide.md")
    content = path.read_text(encoding="utf-8")
    found = validate(content) + check_sources(content)
    for problem in found:
        print(f"❌ {problem}")
    if not found:
        print(f"✅ {path} prošel kontrolou.")
    sys.exit(1 if found else 0)
