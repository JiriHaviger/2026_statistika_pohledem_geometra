"""
Audit existujících kapitol (příkaz `audit`).

Co umí spočítat Python, nepočítá LLM: seznam kapitol se čte z _quarto.yml, osnova každé
kapitoly (H1, H2, počty OJS bloků, tabsetů, slov) i deterministické nálezy vznikají bez LLM.
LLM dostane jen osnovy a posuzuje duplicity a návaznosti. Kapitoly se nemění.
Deterministická část nepotřebuje crewai ani API klíč (lze testovat samostatně).
"""

import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import yaml

from crew import pipeline, prompts
from crew.paths import AUDIT_REPORT_PATH, PROJECT_ROOT, display_path

HEX_RE = pipeline._HEX_RE
NON_ASCII_OR_SPACE_RE = re.compile(r"[^A-Za-z0-9._/\-]")
SOURCE_DIRS = ("01-pravdepodobnost", "02-statistika")   # složky s kapitolami knihy


# ----------------- Seznam kapitol z _quarto.yml -----------------

def _collect_chapters(items) -> list[str]:
    """Projde book.chapters (řetězce i části s vnořeným `chapters`)."""
    result: list[str] = []
    for item in items or []:
        if isinstance(item, str):
            result.append(item)
        elif isinstance(item, dict):
            if "file" in item:
                result.append(item["file"])
            result += _collect_chapters(item.get("chapters"))
    return result


def book_chapters() -> list[str]:
    """Kapitoly knihy v pořadí z _quarto.yml (bez index.qmd)."""
    config = yaml.safe_load((PROJECT_ROOT / "_quarto.yml").read_text(encoding="utf-8"))
    files = _collect_chapters(config.get("book", {}).get("chapters"))
    return [f for f in files if f != "index.qmd"]


# ----------------- Osnova a deterministické nálezy -----------------

@dataclass
class Outline:
    path: str
    exists: bool
    h1: list[str]
    h2: list[str]
    sections: int
    ojs_blocks: int
    tabsets: int
    words: int
    hex_colors: list[str]
    has_summary: bool


def outline_of(relative: str) -> Outline:
    path = PROJECT_ROOT / relative
    if not path.exists():
        return Outline(relative, False, [], [], 0, 0, 0, 0, [], False)
    text = path.read_text(encoding="utf-8")
    scan = pipeline.scan_chapter(text)
    hexes: set[str] = set()
    for block in scan.ojs_blocks:
        code = "\n".join(l for l in block.code.splitlines() if not l.lstrip().startswith("//"))
        hexes.update(HEX_RE.findall(code))
    h1 = scan.h1
    if not h1:   # Quarto bere za nadpis kapitoly i `title:` v hlavičce
        title = re.match(r"---\s*\n(?:.*\n)*?title:\s*[\"']?(.+?)[\"']?\s*\n(?:.*\n)*?---", text)
        if title:
            h1 = [title.group(1)]
    return Outline(
        path=relative, exists=True, h1=h1, h2=scan.h2, sections=len(scan.sections),
        ojs_blocks=len(scan.ojs_blocks), tabsets=scan.tabsets, words=len(text.split()),
        hex_colors=sorted(hexes),
        has_summary=any(re.search(r"záv[eě]r|shrnut|poznatk", h, re.I) for h in scan.h2),
    )


def deterministic_findings(outlines: list[Outline]) -> list[str]:
    """Nálezy, které nepotřebují LLM. Každý nález je jedna řádka s názvem souboru."""
    findings: list[str] = []
    listed = {o.path for o in outlines}

    for o in outlines:
        if not o.exists:
            findings.append(f"`{o.path}` je v `_quarto.yml`, ale soubor neexistuje.")
            continue
        if NON_ASCII_OR_SPACE_RE.search(o.path):
            findings.append(f"`{o.path}`: název souboru obsahuje diakritiku nebo mezeru.")
        if len(o.h1) != 1:
            findings.append(f"`{o.path}`: {len(o.h1)} nadpisů první úrovně (má být 1).")
        if o.sections > prompts.MAX_SECTIONS:
            findings.append(f"`{o.path}`: {o.sections} obsahových sekcí (doporučené maximum "
                            f"{prompts.MAX_SECTIONS}).")
        if o.ojs_blocks == 0:
            findings.append(f"`{o.path}`: žádný OJS blok (chybí interaktivní vizualizace).")
        if not o.has_summary:
            findings.append(f"`{o.path}`: chybí závěr nebo shrnutí (H2 se slovem „závěr“, „shrnutí“ nebo „poznatky“).")
        if o.hex_colors:
            findings.append(f"`{o.path}`: pevné barvy v OJS {o.hex_colors}.")

    # Soubory ve složkách s kapitolami, které kniha nezahrnuje
    for folder in SOURCE_DIRS:
        for path in sorted((PROJECT_ROOT / folder).glob("*.qmd")):
            relative = path.relative_to(PROJECT_ROOT).as_posix()
            if relative not in listed:
                findings.append(f"`{relative}` není v `_quarto.yml` (kniha ho nevykreslí).")
    return findings


def outline_text(o: Outline) -> str:
    """Osnova jedné kapitoly jako Markdown pro LLM."""
    if not o.exists:
        return f"### `{o.path}`\n(soubor neexistuje)"
    lines = [f"### `{o.path}`", f"- H1: {'; '.join(o.h1) or '(chybí)'}",
             f"- Počet slov: {o.words}, OJS bloků: {o.ojs_blocks}, tabsetů: {o.tabsets}",
             "- Sekce (H2):"]
    lines += [f"  - {h}" for h in o.h2]
    return "\n".join(lines)


# ----------------- Report -----------------

def strip_intro(text: str) -> str:
    """Odřízne úvodní větu LLM před prvním nadpisem."""
    lines = text.strip().splitlines()
    for index, line in enumerate(lines):
        if line.startswith("#"):
            return "\n".join(lines[index:]).strip()
    return text.strip()


def build_report(outlines: list[Outline], findings: list[str], recommendations: str) -> str:
    findings_text = "\n".join(f"- {f}" for f in findings) or "- žádné"
    table = ["| Soubor | Sekcí | OJS | Tabsetů | Slov |", "|---|---|---|---|---|"]
    table += [f"| `{o.path}` | {o.sections} | {o.ojs_blocks} | {o.tabsets} | {o.words} |"
              for o in outlines if o.exists]
    return "\n".join([
        "# Audit kapitol",
        "",
        f"Vygenerováno: {date.today().isoformat()}. Seznam kapitol je z `_quarto.yml`, obsah kapitol "
        "se nezměnil. Zprávu **nepředávat agentům jako podklad k úpravám**, slouží autorovi "
        "k rozhodnutí.",
        "",
        "## Osnova (spočítáno Pythonem)",
        "",
        *table,
        "",
        "## Deterministické nálezy",
        "",
        findings_text,
        "",
        "## Doporučení (LLM, posuzuje jen duplicity a návaznosti podle osnov)",
        "",
        recommendations,
        "",
    ])


def audit_chapters() -> None:
    """Spočítá osnovy a nálezy, LLM posoudí duplicity a návaznosti, uloží report."""
    from crew.chapter import run_single_task
    from crew.agents import reviewer_agent

    print("🔍 Spouštím audit kapitol...\n")
    outlines = [outline_of(f) for f in book_chapters()]
    findings = deterministic_findings(outlines)
    print(f"Deterministické nálezy: {len(findings)}")

    raw = run_single_task(
        reviewer_agent,
        prompts.audit_description("\n\n".join(outline_text(o) for o in outlines), findings),
        "Markdown se sekcemi ## Duplicity, ## Návaznosti a ## Doporučení, bez úvodní věty.")

    report = build_report(outlines, findings, strip_intro(raw))
    AUDIT_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    AUDIT_REPORT_PATH.write_text(report, encoding="utf-8")
    print(f"\n✅ Audit report uložen: {display_path(AUDIT_REPORT_PATH)}")


if __name__ == "__main__":
    # Bez LLM: vypíše osnovy a deterministické nálezy
    chapters = [outline_of(f) for f in book_chapters()]
    for item in chapters:
        print(outline_text(item), "\n")
    print("NÁLEZY:")
    for finding in deterministic_findings(chapters):
        print(" -", finding)
