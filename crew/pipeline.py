"""
Deterministické kroky generování kapitoly (bez LLM, bez crewai).

Co LLM dělat nemá, dělá Python: vkládání OJS bloků, kontrola struktury a pravidel,
srovnání textu před a po recenzi, zámek proti duplicitním kapitolám a kontrolní render.
Modul lze testovat samostatně.
"""

import difflib
import json
import os
import re
import shutil
import subprocess
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

from crew.paths import DRAFTS_DIR, PROJECT_ROOT, project_path
from crew.prompts import MAX_SECTIONS, REVIEW_MARKER   # limity a značky jsou ve specifikaci
from crew.style_guide import next_fence_state

# ----------------- Konstanty -----------------

PLACEHOLDER_RE = re.compile(r"OJS_PLACEHOLDER_SEKCE_(\d+)")
OJS_OPEN_RE = re.compile(r"^\s*`{3,}\s*\{ojs\}")
OJS_BLOCK_RE = re.compile(r"^[ \t]*```\{ojs\}[^\n]*\n(.*?)^[ \t]*```[ \t]*$", re.S | re.M)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
DIV_OPEN_RE = re.compile(r"^\s*:{3,}\s*\S")
DIV_CLOSE_RE = re.compile(r"^\s*:{3,}\s*$")
# H2, které nejsou „obsahová sekce“ (aplikační úlohy, závěr)
NON_CONTENT_H2_RE = re.compile(r"aplika[cč]n|záv[eě]r|shrnut", re.I)

MAX_LENGTH_DROP = 0.15          # recenzent smí text zkrátit nejvýše o 15 %
ALLOWED_OJS_IMPORTS = {"../assets/jhrules.js"}

SKIP_DIRS = {".venv", ".git", "_book", ".quarto", "_freeze", "node_modules", "__pycache__"}


# ----------------- Slug a zámek (A5) -----------------

def chapter_slug(filename: str) -> str:
    """Název souboru bez číselného prefixu, ASCII, malými písmeny, oddělený pomlčkami."""
    stem = Path(filename).stem
    stem = unicodedata.normalize("NFKD", stem).encode("ascii", "ignore").decode().lower()
    stem = re.sub(r"^\d+[-_ ]+", "", stem)
    return re.sub(r"[^a-z0-9]+", "-", stem).strip("-")


def _significant_words(slug: str) -> set[str]:
    return {word for word in slug.split("-") if len(word) >= 5}


def iter_qmd_files():
    """Všechny .qmd v projektu mimo prostředí, build a cache (včetně _drafts)."""
    for folder, dirs, files in os.walk(PROJECT_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            if name.endswith(".qmd"):
                yield Path(folder) / name


@dataclass
class Conflicts:
    target: Path | None                  # soubor kapitoly v knize už existuje
    draft: Path | None                   # draft se stejným názvem už existuje
    same_slug: list[Path] = field(default_factory=list)   # jiný soubor se stejným slugem
    similar: list[Path] = field(default_factory=list)     # jiný soubor se sdíleným slovem v názvu

    @property
    def blocking(self) -> bool:
        """Tohle nepřepíše ani --force: kapitola v knize nebo duplicitní slug."""
        return bool(self.target or self.same_slug)


def draft_path_for(output_file: str) -> Path:
    return DRAFTS_DIR / project_path(output_file).name


def find_conflicts(output_file: str) -> Conflicts:
    target = project_path(output_file)
    draft = draft_path_for(output_file)
    slug = chapter_slug(target.name)
    words = _significant_words(slug)
    result = Conflicts(target=target if target.exists() else None,
                       draft=draft if draft.exists() else None)
    for path in iter_qmd_files():
        if path in (target, draft):
            continue
        other = chapter_slug(path.name)
        if other == slug:
            result.same_slug.append(path)
        elif words & _significant_words(other):
            result.similar.append(path)
    return result


# ----------------- Úprava výstupu LLM -----------------

def strip_outer_fence(text: str) -> str:
    """Odstraní obalující ```markdown … ``` kolem celého výstupu (pokud tam je)."""
    lines = text.strip().splitlines()
    if len(lines) > 2 and re.fullmatch(r"`{3,}\s*(markdown|md|qmd)?\s*", lines[0]) \
            and re.fullmatch(r"`{3,}\s*", lines[-1]):
        return "\n".join(lines[1:-1])
    return text.strip()


def clean_chapter_output(raw: str) -> str:
    """Odřízne úvodní větu LLM (vše před YAML hlavičkou nebo prvním nadpisem) a obal."""
    text = strip_outer_fence(raw)
    lines = text.splitlines()
    start = next((i for i, line in enumerate(lines)
                  if line.strip() == "---" or line.startswith("# ")), None)
    if start is None:
        raise ValueError("Výstup neobsahuje ani YAML hlavičku, ani nadpis první úrovně.")
    body = lines[start:]
    # Úvodní věta a pak ```markdown … ```: ořízli jsme začátek, zbývá ještě zavírací ohrada
    opened_before = any(re.fullmatch(r"`{3,}\s*(markdown|md|qmd)?\s*", line) for line in lines[:start])
    if opened_before and body and re.fullmatch(r"`{3,}\s*", body[-1]):
        body = body[:-1]
    return "\n".join(body).strip() + "\n"


def split_review_output(raw: str) -> tuple[str, str]:
    """Rozdělí odpověď recenzenta na (kapitola, poznámky). Poznámky jsou za řádkem REVIEW_MARKER."""
    parts = re.split(rf"^{re.escape(REVIEW_MARKER)}\s*$", raw, maxsplit=1, flags=re.M)
    chapter = clean_chapter_output(parts[0])
    notes = parts[1].strip() if len(parts) > 1 else ""
    return chapter, notes


# ----------------- OJS bloky (A4) -----------------

def placeholder_numbers(markdown: str) -> list[int]:
    return sorted({int(n) for n in PLACEHOLDER_RE.findall(markdown)})


def check_placeholder_numbers(numbers: list[int]) -> None:
    """Placeholdery musí být 1..k bez děr a k nejvýše MAX_SECTIONS."""
    if not numbers:
        raise ValueError("V textu kapitoly není žádný OJS_PLACEHOLDER_SEKCE_N.")
    if numbers != list(range(1, len(numbers) + 1)):
        raise ValueError(f"Placeholdery nejsou souvislá řada 1..k: {numbers}")
    if len(numbers) > MAX_SECTIONS:
        raise ValueError(f"Kapitola má {len(numbers)} sekcí s grafem, maximum je {MAX_SECTIONS}.")


def _strip_code_fence(code: str) -> str:
    lines = code.strip().splitlines()
    if lines and re.match(r"`{3,}", lines[0]):
        lines = lines[1:]
    if lines and re.fullmatch(r"`{3,}\s*", lines[-1]):
        lines = lines[:-1]
    return "\n".join(lines).strip("\n")


def parse_ojs_json(raw: str, expected: list[int]) -> dict[int, str]:
    """Z odpovědi ojs_agenta vytáhne {číslo sekce: kód}. Klíče musí přesně odpovídat `expected`."""
    match = re.search(r"\{.*\}", raw, re.S)
    if not match:
        raise ValueError("Odpověď ojs_agenta neobsahuje JSON objekt.")
    try:
        data = json.loads(match.group(0))
    except json.JSONDecodeError as e:
        raise ValueError(f"Odpověď ojs_agenta není platný JSON: {e}") from e
    blocks: dict[int, str] = {}
    for key, value in data.items():
        try:
            number = int(key)
        except ValueError as e:
            raise ValueError(f"Klíč '{key}' není číslo sekce.") from e
        code = _strip_code_fence(str(value))
        if not code.strip():
            raise ValueError(f"OJS kód sekce {number} je prázdný.")
        blocks[number] = code
    if sorted(blocks) != expected:
        raise ValueError(f"Sekce v JSON {sorted(blocks)} neodpovídají placeholderům {expected}.")
    return blocks


def insert_ojs(markdown: str, blocks: dict[int, str]) -> str:
    """Nahradí každý blok s OJS_PLACEHOLDER_SEKCE_N kódem sekce N. Po vložení nesmí nic zůstat."""
    used: set[int] = set()

    def replace(match: re.Match) -> str:
        found = PLACEHOLDER_RE.search(match.group(1))
        if not found:
            return match.group(0)            # jiný OJS blok necháme být
        number = int(found.group(1))
        if number not in blocks:
            raise ValueError(f"Pro placeholder sekce {number} není OJS kód.")
        used.add(number)
        code = blocks[number]
        if not code.lstrip().startswith("//|"):
            code = "//| echo: false\n" + code
        return "```{ojs}\n" + code + "\n```"

    result = OJS_BLOCK_RE.sub(replace, markdown)
    if PLACEHOLDER_RE.search(result):
        raise ValueError(f"Po vložení zůstal placeholder: {placeholder_numbers(result)} "
                         "(nejspíš není v samostatném bloku ```{ojs}).")
    unused = sorted(set(blocks) - used)
    if unused:
        raise ValueError(f"OJS kód sekcí {unused} nemá v textu kam vložit.")
    return result


# ----------------- Struktura kapitoly -----------------

@dataclass
class OjsBlock:
    code: str
    section: int | None      # index obsahové sekce (od 0), None = mimo obsahovou sekci
    start_line: int


@dataclass
class ChapterScan:
    h1: list[str] = field(default_factory=list)
    h2: list[str] = field(default_factory=list)          # H2 mimo kód a mimo ::: divy
    sections: list[str] = field(default_factory=list)    # H2, které jsou obsahové sekce
    ojs_blocks: list[OjsBlock] = field(default_factory=list)
    tabsets: int = 0
    length: int = 0


def scan_chapter(markdown: str) -> ChapterScan:
    """Projde kapitolu a ignoruje nadpisy uvnitř bloků kódu a ::: divů
    (záložky tabsetu a titulky calloutů se píšou jako ## uvnitř divu)."""
    scan = ChapterScan(length=len(markdown))
    open_fence = None
    div_depth = 0
    current_block: list[str] | None = None
    block_start = 0
    current_section: int | None = None

    for number, line in enumerate(markdown.splitlines(), start=1):
        before = open_fence
        open_fence, is_fence = next_fence_state(open_fence, line)
        if is_fence:
            if before is None:                       # otevření bloku
                if OJS_OPEN_RE.match(line):
                    current_block, block_start = [], number
            elif current_block is not None:          # zavření OJS bloku
                scan.ojs_blocks.append(OjsBlock("\n".join(current_block), current_section, block_start))
                current_block = None
            continue
        if before is not None:                       # uvnitř kódu
            if current_block is not None:
                current_block.append(line)
            continue
        if DIV_OPEN_RE.match(line):
            div_depth += 1
            if "panel-tabset" in line:
                scan.tabsets += 1
            continue
        if DIV_CLOSE_RE.match(line):
            div_depth = max(0, div_depth - 1)
            continue
        heading = HEADING_RE.match(line)
        if heading and div_depth == 0:
            level, text = len(heading.group(1)), heading.group(2)
            if level == 1:
                scan.h1.append(text)
            elif level == 2:
                scan.h2.append(text)
                if NON_CONTENT_H2_RE.search(text):
                    current_section = None
                else:
                    scan.sections.append(text)
                    current_section = len(scan.sections) - 1
    return scan


# ----------------- Kontroly OJS kódu (A6) -----------------

_NAME_RE = re.compile(r"^(?:viewof\s+|mutable\s+)?([A-Za-z_$][\w$]*)\s*=(?![=>])")
_FUNC_RE = re.compile(r"^(?:async\s+)?(?:function\*?|class)\s+([A-Za-z_$][\w$]*)")
_IMPORT_RE = re.compile(r"import\s*\{([^}]*)\}\s*from\s*[\"']([^\"']+)[\"']", re.S)
_HEX_RE = re.compile(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b")
_WIDTH_RE = re.compile(r"\bwidth\s*:\s*\d{2,}")


def ojs_defined_names(code: str) -> list[str]:
    """Jména, která buňka definuje v globálním prostoru stránky (jen na začátku řádku;
    uvnitř { … } bloků jsou proměnné lokální). Zahrnuje i jména z `import {…} from`."""
    names: list[str] = []
    for line in code.splitlines():
        if line.startswith("//") or line[:1].isspace():
            continue
        for regex in (_NAME_RE, _FUNC_RE):
            match = regex.match(line)
            if match:
                names.append(match.group(1))
                break
    for imported, _source in _IMPORT_RE.findall(code):
        for part in imported.split(","):
            part = part.strip()
            if part:
                names.append(part.split(" as ")[-1].strip())
    return names


_INLINE_RE = re.compile(r"\$\{([^{}]+)\}")
# Jména, která jsou v OJS vždy k dispozici (JavaScript a vestavěné proměnné Quarto/Observable)
JS_BUILTINS = {
    "Math", "Number", "String", "Array", "Object", "JSON", "Intl", "Date", "parseFloat", "parseInt",
    "isNaN", "Infinity", "NaN", "d3", "Plot", "Inputs", "htl", "html", "md", "tex", "width", "DOM",
    "Generators", "Mutable", "require", "FileAttachment", "true", "false", "null", "undefined",
    "typeof", "new", "in", "of",
}


def inline_ojs_names(markdown: str) -> list[str]:
    """Jména proměnných, které text používá v inline OJS `${…}`. Kód v zpětných apostrofech
    (dokumentace) a bloky kódu se přeskakují. `${a+b}^2$` v matematice by se hlásilo omylem
    (Pandoc ho bere jako matematiku); takový zápis je vzácný a nález je jen upozornění."""
    names: set[str] = set()
    open_fence = None
    for line in markdown.splitlines():
        before = open_fence
        open_fence, is_fence = next_fence_state(open_fence, line)
        if is_fence or before is not None:
            continue
        line = re.sub(r"`[^`]*`", "", line)
        for match in _INLINE_RE.finditer(line):
            expression = re.sub(r"\"[^\"]*\"|'[^']*'", "", match.group(1))
            for name in re.findall(r"(?<![\w$.])([A-Za-z_$][\w$]*)", expression):
                if name not in JS_BUILTINS:
                    names.add(name)
    return sorted(names)


def check_chapter(markdown: str) -> list[str]:
    """Statické kontroly kapitoly. Vrací seznam nálezů (prázdný = v pořádku)."""
    problems: list[str] = []
    scan = scan_chapter(markdown)

    open_fence = None
    for line in markdown.splitlines():
        open_fence, _ = next_fence_state(open_fence, line)
    if open_fence is not None:
        problems.append("Kapitola končí uvnitř nezavřeného bloku kódu (nevyvážené ohrady ```).")
    if PLACEHOLDER_RE.search(markdown):
        problems.append(f"Zůstal OJS placeholder u sekcí {placeholder_numbers(markdown)}.")
    if "REVIEW NOTES" in markdown:
        problems.append("V textu kapitoly zůstala poznámka REVIEW NOTES (patří do reportu).")
    if len(scan.h1) != 1:
        problems.append(f"Kapitola má {len(scan.h1)} nadpisů první úrovně, má mít právě 1.")
    if len(scan.sections) > MAX_SECTIONS:
        problems.append(f"Kapitola má {len(scan.sections)} obsahových sekcí, maximum je {MAX_SECTIONS}.")
    for index, title in enumerate(scan.sections):
        count = sum(1 for block in scan.ojs_blocks if block.section == index)
        if count != 1:
            problems.append(f"Sekce „{title}“ má {count} OJS bloků, má mít právě 1.")
    stray = [b.start_line for b in scan.ojs_blocks if b.section is None]
    if stray:
        problems.append(f"OJS blok mimo obsahovou sekci (řádky {stray}).")

    # Všechny OJS buňky stránky sdílejí jeden globální prostor
    owners: dict[str, list[int]] = {}
    for number, block in enumerate(scan.ojs_blocks, start=1):
        for name in ojs_defined_names(block.code):
            owners.setdefault(name, []).append(number)
    for name, cells in owners.items():
        if len(cells) > 1:
            problems.append(f"Proměnná „{name}“ je definována víckrát (OJS buňky {cells}); "
                            "názvy musí být v celé kapitole unikátní.")
    undefined = [name for name in inline_ojs_names(markdown) if name not in owners]
    if undefined:
        problems.append(f"Text používá v ${{…}} proměnné {undefined}, které žádná OJS buňka nedefinuje "
                        "(na stránce by se zobrazila chyba).")

    for number, block in enumerate(scan.ojs_blocks, start=1):
        for _names, source in _IMPORT_RE.findall(block.code):
            if source not in ALLOWED_OJS_IMPORTS:
                problems.append(f"OJS buňka {number}: nepovolený import z „{source}“ "
                                f"(povoleno: {', '.join(sorted(ALLOWED_OJS_IMPORTS))}).")
        code_lines = [l for l in block.code.splitlines() if not l.lstrip().startswith("//")]
        code = "\n".join(code_lines)
        hexes = sorted(set(_HEX_RE.findall(code)))
        if hexes:
            problems.append(f"OJS buňka {number}: pevné barvy {hexes}; použij paletu C z modulu.")
        if _WIDTH_RE.search(code):
            problems.append(f"OJS buňka {number}: pevná číselná width; použij vestavěné `width`.")
    return problems


# ----------------- Srovnání před a po recenzi (A4) -----------------

def compare_structure(before: str, after: str) -> tuple[list[str], list[str]]:
    """Vrací (chyby, upozornění). Chyba = recenze zničila strukturu (text se nepřijme);
    upozornění = struktura se rozšířila (zapíše se do reportu)."""
    a, b = scan_chapter(before), scan_chapter(after)
    errors: list[str] = []
    warnings: list[str] = []

    if len(b.ojs_blocks) != len(a.ojs_blocks):
        errors.append(f"Počet OJS bloků: {len(a.ojs_blocks)} → {len(b.ojs_blocks)}.")
    for label, old, new in (("nadpisů H2", len(a.h2), len(b.h2)),
                            ("záložek (tabsetů)", a.tabsets, b.tabsets)):
        if new < old:
            errors.append(f"Počet {label} klesl: {old} → {new}.")
        elif new > old:
            warnings.append(f"Počet {label} vzrostl: {old} → {new}.")
    if b.length < a.length * (1 - MAX_LENGTH_DROP):
        errors.append(f"Text se zkrátil o víc než {MAX_LENGTH_DROP:.0%}: {a.length} → {b.length} znaků.")
    return errors, warnings


def unified_diff(before: str, after: str) -> str:
    diff = difflib.unified_diff(before.splitlines(), after.splitlines(),
                                "před recenzí", "po recenzi", lineterm="")
    return "\n".join(diff)


# ----------------- Kontrolní render (A6) -----------------

def render_draft(path: Path, timeout: int = 300) -> tuple[bool, str]:
    """Spustí `quarto render <draft> --to html`, vrátí (úspěch, konec logu).
    Vzniklé html a složku *_files hned smaže. Pozor: draft ve složce _drafts se renderuje
    mimo knihu (bez motivu knihy), kontroluje se tedy syntaxe a OJS, ne vzhled."""
    quarto = shutil.which("quarto")
    if not quarto:
        return False, "Quarto nebylo nalezeno v PATH, render se nespustil."
    html = path.with_suffix(".html")
    files = path.parent / f"{path.stem}_files"
    try:
        result = subprocess.run(
            [quarto, "render", str(path), "--to", "html"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=timeout, cwd=PROJECT_ROOT,
        )
        log = "\n".join((result.stdout + "\n" + result.stderr).strip().splitlines()[-40:])
        return result.returncode == 0, log
    except subprocess.TimeoutExpired:
        return False, f"Render překročil limit {timeout} s a byl přerušen."
    finally:
        html.unlink(missing_ok=True)
        shutil.rmtree(files, ignore_errors=True)
