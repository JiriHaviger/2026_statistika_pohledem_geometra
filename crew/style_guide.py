"""
Sestavení a kontrola docs_for_agents/style_guide.md.

LLM píše jen sekce 1–4 a 7. Sekce 5 (barvy) a 6 (struktura kapitoly) vkládá Python,
aby je LLM nemohlo zkomolit. Modul záměrně neimportuje crewai ani crew.config,
takže kontrolu lze spustit i bez API klíče:

    .venv\\Scripts\\python.exe -m crew.style_guide            # zkontroluje style_guide.md
"""

import hashlib
import re
import sys
from datetime import date
from pathlib import Path

from crew.paths import project_path
from crew.prompts import CHAPTER_STRUCTURE

PROJECT_NAME = "Statistika pohledem geometra"
SCSS_PATH = "hag_custom.scss"
SOURCE_FILES = ["_quarto.yml", SCSS_PATH, "jhrules.py", "assets/jhrules.js"]   # při jejich změně je style guide zastaralý

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
    return hashlib.sha256(project_path(path).read_bytes()).hexdigest()


def next_fence_state(open_fence, line: str):
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
        open_fence, is_fence = next_fence_state(open_fence, line)
        yield line, is_fence or before is not None


def fences_balanced(text: str) -> bool:
    """True, pokud po posledním řádku nezůstal otevřený kódový blok."""
    open_fence = None
    for line in text.splitlines():
        open_fence, _ = next_fence_state(open_fence, line)
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

PYTHON_PALETTE_PATH = "jhrules.py"
OJS_MODULE_PATH = "assets/jhrules.js"

# Role barev JHRules (stručný popis do style guide)
PALETTE_ROLES = {
    "bg": "pozadí stránky a grafu (graf má průhledné pozadí)",
    "text": "běžný text, nadpisy, druhá datová řada",
    "primary": "hlavní datová barva (sloupce, křivky, prvky grafu)",
    "primary-light": "výplně, podklady, vedlejší řady téže věci",
    "primary-text": "tmavší primary jen pro odkazy a text (kontrast ≥ 4,5 : 1)",
    "accent": "NA CO SE DÍVAT: jedna věc na obrázek (zvýrazněný bod, hodnota, výsledek)",
    "context": "kontext: osy, popisky, vedlejší data",
    "context-light": "okrajové a pomocné prvky",
    "grid": "mřížka (jen vodorovná, jemná)",
    "warning": "pouze varování a chyby (tlumená bordó)",
}


def _camel_case(scss_name: str) -> str:
    first, *rest = scss_name.split("-")
    return first + "".join(part.capitalize() for part in rest)


def read_scss_colors(scss_path: str = SCSS_PATH) -> dict[str, str]:
    """Načte paletu JHRules: hex proměnné `$jh-*` ze SCSS. Klíče bez prefixu (primary-light …)."""
    colors: dict[str, str] = {}
    var_re = re.compile(r"^\$jh-([\w-]+):\s*(#[0-9a-fA-F]{6})\s*;")
    for line in project_path(scss_path).read_text(encoding="utf-8").splitlines():
        match = var_re.match(line.strip())
        if match:
            colors[match.group(1)] = match.group(2).upper()
    return colors


def read_python_palette(py_path: str = PYTHON_PALETTE_PATH) -> dict[str, str]:
    """Načte slovník C z jhrules.py (klíče s podtržítkem převede na pomlčky)."""
    source = project_path(py_path).read_text(encoding="utf-8")
    block = re.search(r"^C = dict\((.*?)\)\s*$", source, re.S | re.M)
    if not block:
        raise ValueError(f"V {py_path} nebyl nalezen slovník C.")
    pairs = re.findall(r'(\w+)="(#[0-9a-fA-F]{6})"', block.group(1))
    return {key.replace("_", "-"): value.upper() for key, value in pairs}


def check_palette_consistency() -> list[str]:
    """Paleta v SCSS (zdroj pravdy), jhrules.py a záložních hodnotách assets/jhrules.js musí souhlasit."""
    scss = read_scss_colors()
    problems = []
    py = read_python_palette()
    for name in sorted(set(scss) | set(py)):
        if scss.get(name) != py.get(name):
            problems.append(f"Barva '{name}': SCSS {scss.get(name)} × jhrules.py {py.get(name)}")
    js_source = project_path(OJS_MODULE_PATH).read_text(encoding="utf-8")
    js = {_kebab(k): v.upper() for k, v in re.findall(r'(\w+): "(#[0-9a-fA-F]{6})"', js_source)}
    for name in sorted(set(scss) | set(js)):
        if scss.get(name) != js.get(name):
            problems.append(f"Barva '{name}': SCSS {scss.get(name)} × assets/jhrules.js {js.get(name)}")
    return problems


def _kebab(camel: str) -> str:
    return re.sub(r"[A-Z]", lambda m: "-" + m.group(0).lower(), camel)


def build_colors_section(scss_path: str = SCSS_PATH) -> str:
    colors = read_scss_colors(scss_path)
    if not colors:
        raise ValueError(f"V {scss_path} nebyla nalezena žádná paleta ($jh-*).")
    rows = [f"| `C.{_camel_case(n)}` | `{v}` | {PALETTE_ROLES.get(n, '')} |" for n, v in colors.items()]
    return "\n".join([
        f"Paleta JHRules je převzatá z `{scss_path}` (proměnné `$jh-*`), což je jediný zdroj pravdy.",
        "V OJS se barvy **nikdy nepíší napevno**, berou se z modulu, který je čte z CSS:",
        "",
        "```js",
        'import {C, gradient, plotStyle} from "../assets/jhrules.js"',
        "```",
        "",
        "- Cesta je **relativní k souboru kapitoly** (`../assets/…`). Absolutní `/assets/…` Quarto odmítne.",
        "- Import patří **jen do jedné (první) OJS buňky kapitoly**. Jinak se `C` definuje víckrát a stránka se rozbije.",
        "",
        "| Konstanta | Hodnota | Použití |",
        "|---|---|---|",
        *rows,
        "",
        "Úplná pravidla stylu JHRules: `docs_for_agents/jhrules/README.md`.",
        "",
        "Principy:",
        "",
        "- Čistý design: bílé pozadí, tlumeně tmavě šedý text (ne čistá černá), žádné rámečky, stíny ani přechody.",
        "- Jedna akcentová barva: `primary` nese veškerý důraz a nemusí se šetřit.",
        "- Výjimka je výjimka: `accent` zvýrazňuje jen jeden prvek (bod, sloupec, výsledek).",
        "- Kontext ustupuje: osy, popisky a potlačená data jsou šedé (`context`, `contextLight`).",
        "- Zvýraznění místo duhy: víc kategorií = jedna `primary` a zbytek `contextLight`, případně plynulé stupňování `gradient(n)`.",
        "",
        "Grafy:",
        "",
        "- Bez horní a pravé osy. Mřížka žádná nebo jemná (`C.grid`), jen ve směru čtení hodnot.",
        "- Legendy bez rámečku, raději přímé popisky u čar.",
        "- Hlavní řada `C.primary`, srovnávací `C.text` nebo `C.context`, potlačené `C.contextLight`.",
        "- Společný styl: `Plot.plot({ style: plotStyle, ... })` (průhledné pozadí, Arial, 12 px).",
        "- Popisky obrázků jsou v barvě `context` (13 px), text je v Arialu, kód v monospace.",
        "- Přístupnost: `primary` a `accent` mají na bílé kontrast jen kolem 4 : 1. Text v těchto barvách patří "
        "tučně nebo od 18 px. Odkazy mají tmavší `C.primaryText`. `context` je jen pro popisky os, ne pro hlavní text.",
        "",
        "Python (matplotlib, plotly): `from jhrules import C, use_matplotlib, use_plotly`. "
        "Animace (manim): bílé pozadí, objekty a rovnice `text`, hlavní objekt `primary`, "
        "pomocné konstrukce `context` nebo `contextLight`, jeden klíčový moment `accent`.",
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
        "  GENEROVÁNO automaticky (python main.py style --force). Needitovat ručně.",
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
    errors += check_palette_consistency()
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


def refresh(text: str) -> str:
    """Bez LLM: ponechá LLM sekce (1–4, 7) a znovu vloží sekce 5 a 6 a hlavičku se sha256.
    Hodí se po změně SCSS, kdy se nezměnil význam textů, jen zdrojové soubory."""
    sections = split_sections(text)
    return assemble({n: sections[n] for n in LLM_SECTIONS})


if __name__ == "__main__":
    if "--refresh" in sys.argv:   # python -m crew.style_guide --refresh
        target = project_path("docs_for_agents/style_guide.md")
        target.write_text(refresh(target.read_text(encoding="utf-8")), encoding="utf-8")
        print(f"🔄 Sekce 5, 6 a hlavička obnoveny v {target}")
        sys.argv.remove("--refresh")
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else project_path("docs_for_agents/style_guide.md")
    content = path.read_text(encoding="utf-8")
    found = validate(content) + check_sources(content)
    for problem in found:
        print(f"❌ {problem}")
    if not found:
        print(f"✅ {path} prošel kontrolou.")
    sys.exit(1 if found else 0)
