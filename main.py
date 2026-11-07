"""
Generátor kapitol a audit učebnice „Statistika pohledem geometra“.

Použití (z libovolného adresáře):
    .venv\\Scripts\\python.exe main.py style [--force]
    .venv\\Scripts\\python.exe main.py chapter [--index N] [--force]
    .venv\\Scripts\\python.exe main.py audit [--force]

Těžké knihovny (CrewAI) a API klíč se načítají až uvnitř příkazů, takže zámky
a nápověda fungují i bez nich.
"""

import argparse
import shutil
import sys

from crew import pipeline, prompts
from crew import style_guide as sg
from crew.chapter import generate_chapter
from crew.paths import (
    AUDIT_REPORT_PATH,
    STYLE_GUIDE_BACKUP_PATH,
    STYLE_GUIDE_PATH,
    STYLE_GUIDE_RAW_PATH,
    display_path,
)


# =============================================================================
# FÁZE 1: GENEROVÁNÍ STYLE GUIDE
# =============================================================================

STYLE_SAMPLE_CHAPTER = "02-statistika/02_deskriptivní statistiky momenty.qmd"


def generate_style_guide() -> str:
    """
    Analýza projektu → Style Guide.
    LLM píše sekce 1–4 a 7, sekce 5 (barvy) a 6 (struktura kapitoly) vkládá Python.
    Výsledek se před uložením zkontroluje; při chybě se style_guide.md nepřepíše.
    Existující style_guide.md se před přepsáním zkopíruje do style_guide.backup.md.
    Zámek a potvrzení řeší příkaz `style` (cmd_style), ne tato funkce.
    """
    from crewai import Task, Crew, Process
    from crew.agents import project_manager
    from crew.tools import read_file

    print("📋 Generuji Style Guide – spouštím analýzu projektu...")

    task_style_guide = Task(
        description=prompts.style_guide_description(sg.PROJECT_NAME, STYLE_SAMPLE_CHAPTER),
        expected_output=(
            "Markdown se sekcemi ## 1., ## 2., ## 3., ## 4. a ## 7. (v tomto pořadí), "
            "bez úvodní věty a bez sekcí 5 a 6."
        ),
        agent=project_manager,
        tools=[read_file]
    )

    crew_init = Crew(
        agents=[project_manager],
        tasks=[task_style_guide],
        process=Process.sequential,
        verbose=True,
        max_rpm=10,
    )
    crew_init.kickoff()

    raw_output = str(task_style_guide.output.raw)

    try:
        style_guide_content = sg.assemble(sg.parse_llm_sections(raw_output))
        errors = sg.validate(style_guide_content)
    except ValueError as e:
        errors = [str(e)]
    if errors:
        STYLE_GUIDE_RAW_PATH.write_text(raw_output, encoding="utf-8")
        problems = "\n".join(f"  - {e}" for e in errors)
        raise RuntimeError(
            f"Style Guide neprošel kontrolou, {display_path(STYLE_GUIDE_PATH)} zůstává beze změny.\n"
            f"{problems}\nSurový výstup LLM: {display_path(STYLE_GUIDE_RAW_PATH)}"
        )

    if STYLE_GUIDE_PATH.exists():
        shutil.copyfile(STYLE_GUIDE_PATH, STYLE_GUIDE_BACKUP_PATH)
        print(f"💾 Původní Style Guide zálohován: {display_path(STYLE_GUIDE_BACKUP_PATH)}")
    STYLE_GUIDE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STYLE_GUIDE_PATH.write_text(style_guide_content, encoding="utf-8")
    print(f"✅ Style Guide uložen: {display_path(STYLE_GUIDE_PATH)}")
    return style_guide_content


def load_style_guide() -> str:
    print(f"✅ Style Guide nalezen – načítám z {display_path(STYLE_GUIDE_PATH)}")
    content = STYLE_GUIDE_PATH.read_text(encoding="utf-8")
    problems = sg.validate(content) + sg.check_sources(content)
    if problems:
        details = "\n".join(f"  - {p}" for p in problems)
        raise RuntimeError(
            f"Style Guide je zastaralý nebo poškozený:\n{details}\n"
            "Přegeneruj ho: python main.py style --force"
        )
    return content


# =============================================================================
# FÁZE 2: AUDIT EXISTUJÍCÍCH KAPITOL
# (generování kapitoly je v crew/chapter.py)
# =============================================================================

# Obsahové kapitoly projektu – index.qmd, references.qmd a summary.qmd jsou vynechány
AUDIT_FILES = [
    "01-pravdepodobnost/01-klasicka-prst.qmd",
    "01-pravdepodobnost/02_prst_pravidla.qmd",
    "01-pravdepodobnost/03_prst_distribuce.qmd",
    "01-pravdepodobnost/04_prst_diskretni.qmd",
    "01-pravdepodobnost/intro.qmd",
    "02-statistika/01_deskriptivní statistiky kvantily.qmd",
    "02-statistika/02_deskriptivní statistiky momenty.qmd",
    "02-statistika/03_aritmetika dat.qmd",
    "02-statistika/04_deskriptivy z tabulky.qmd",
    "02-statistika/05_analyza_rozptylu_geometricky.qmd",
]

def audit_chapters() -> None:
    """
    Nechá reviewer_agent přečíst všechny obsahové kapitoly a vypsat:
    - duplicitní témata nebo sekce,
    - nesoulad názvu souboru s obsahem,
    - chybějící nebo neúplné části.
    Výsledek se zapíše do docs_for_agents/audit_report.md (přepíše stávající report;
    zámek a potvrzení řeší příkaz `audit`). Kapitoly se nemění.
    """
    from crewai import Task, Crew, Process
    from crew.agents import reviewer_agent
    from crew.tools import read_file

    print("🔍 Spouštím audit kapitol...\n")

    soubory_seznam = "\n".join(f"- `{f}`" for f in AUDIT_FILES)

    # ------------------------------------------------------------------
    # TASK 1: Přečíst a zmapovat všechny kapitoly
    # ------------------------------------------------------------------
    task_read = Task(
        description=f"""
        Přečti pomocí nástroje `read_file` všechny níže uvedené soubory.
        Pro každý soubor si zaznamenej:
        - název souboru,
        - hlavní nadpis (H1),
        - seznam sekcí (H2 nadpisy),
        - stručný obsah každé sekce (1–2 věty).

        Soubory ke čtení:
        {soubory_seznam}

        Výstupem je strukturovaný přehled všech kapitol – název souboru, nadpis, sekce, obsah.
        Zatím nehodnoť, jen zaznamenej fakta.
        """,
        expected_output=(
            "Strukturovaný přehled všech kapitol: pro každý soubor název, H1 nadpis, "
            "seznam H2 sekcí a stručný popis obsahu každé sekce."
        ),
        agent=reviewer_agent,
        tools=[read_file]
    )

    # ------------------------------------------------------------------
    # TASK 2: Analyzovat a vypsat nálezy
    # ------------------------------------------------------------------
    task_audit = Task(
        description=f"""
        Na základě přehledu kapitol z předchozího kroku proveď důkladnou analýzu a vypiš konkrétní nálezy.

        Hledej a popiš:

        ## 1. Duplicity
        Sekce nebo témata, která se opakují ve více kapitolách.
        Pro každou duplicitu uveď: které soubory, které sekce, co přesně se opakuje.

        ## 2. Nesoulad názvu souboru s obsahem
        Případy, kdy název souboru nebo H1 nadpis neodpovídá skutečnému obsahu.
        Navrhni lepší název.

        ## 3. Chybějící nebo neúplné části
        Kapitoly, kterým chybí očekávané části (příklady, vizualizace, závěr...).

        ## 4. Doporučení
        Ke každému nálezu navrhni konkrétní akci:
        - přejmenovat soubor / nadpis,
        - přesunout sekci z kapitoly X do kapitoly Y,
        - smazat duplicitní sekci v souboru Z,
        - doplnit chybějící část.

        Výstupem je Markdown report. Buď konkrétní – uváděj přesné názvy souborů a sekcí.
        Vyhni se obecným frázím jako "obsah je kvalitní" nebo "kapitola je dobře napsaná".
        """,
        expected_output=(
            "Markdown audit report se sekcemi: Duplicity, Nesoulad názvů, Chybějící části, Doporučení. "
            "Každý nález obsahuje konkrétní název souboru a sekce."
        ),
        agent=reviewer_agent,
    )

    crew_audit = Crew(
        agents=[reviewer_agent],
        tasks=[task_read, task_audit],
        process=Process.sequential,
        verbose=True,
        max_rpm=10,
    )
    crew_audit.kickoff()

    report = str(task_audit.output.raw)

    AUDIT_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    AUDIT_REPORT_PATH.write_text(report, encoding="utf-8")
    print(f"\n✅ Audit report uložen: {display_path(AUDIT_REPORT_PATH)}")


# =============================================================================
# PŘÍKAZOVÁ ŘÁDKA
# =============================================================================

CHAPTER_REQUIRED_KEYS = ["tema", "vystupni_soubor", "klicove_pojmy", "zamereni_uloh", "nastroje"]


def confirm_overwrite(targets: list) -> bool:
    """Vypíše, co se přepíše, a zeptá se na potvrzení. V neinteraktivním režimu odmítne."""
    print("⚠️  Tyto soubory se PŘEPÍŠÍ:")
    for target in targets:
        print(f"   - {display_path(target)}")
    return ask_yes_no("Pokračovat?")


def ask_yes_no(question: str) -> bool:
    """Zeptá se uživatele (výchozí je ne). V neinteraktivním režimu odmítne."""
    if not sys.stdin or not sys.stdin.isatty():
        print("Nelze se zeptat na potvrzení (vstup není terminál), končím beze změny.")
        return False
    try:
        answer = input(f"{question} [a/N]: ")
    except EOFError:   # např. Windows: NUL se tváří jako terminál, ale nic nepošle
        print("\nŽádná odpověď, končím beze změny.")
        return False
    return answer.strip().lower() in ("a", "ano", "y", "yes")


def cmd_style(args) -> int:
    if STYLE_GUIDE_PATH.exists():
        if not args.force:
            problems = sg.validate(STYLE_GUIDE_PATH.read_text(encoding="utf-8"))
            problems += sg.check_sources(STYLE_GUIDE_PATH.read_text(encoding="utf-8"))
            if problems:
                print(f"🛑 {display_path(STYLE_GUIDE_PATH)} existuje, ale je zastaralý nebo poškozený:")
                for p in problems:
                    print(f"   - {p}")
                print("Přegenerování: python main.py style --force")
                return 1
            print(f"✅ {display_path(STYLE_GUIDE_PATH)} existuje a je aktuální. Nic se nemění "
                  "(přegenerování: --force).")
            return 0
        if not confirm_overwrite([STYLE_GUIDE_PATH, STYLE_GUIDE_BACKUP_PATH]):
            return 1
    generate_style_guide()
    return 0


def cmd_chapter(args) -> int:
    from chapters import CHAPTERS

    if not CHAPTERS:
        print("Seznam kapitol v chapters.py je prázdný – přidej položku podle vzoru v souboru.")
        return 1

    if args.index is None:
        print("Kapitoly v chapters.py (použij --index N):")
        for number, chapter in enumerate(CHAPTERS, start=1):
            output_file = chapter.get("vystupni_soubor")
            state = ""
            if output_file:
                found = pipeline.find_conflicts(output_file)
                if found.blocking:
                    state = "  [v projektu už je]"
                elif found.draft:
                    state = "  [draft existuje]"
            print(f"  {number}. {chapter.get('tema', '?')} → {output_file or '?'}{state}")
        return 0

    if not 1 <= args.index <= len(CHAPTERS):
        print(f"Index musí být 1 až {len(CHAPTERS)}.")
        return 1
    inputs = CHAPTERS[args.index - 1]

    missing = [key for key in CHAPTER_REQUIRED_KEYS if not inputs.get(key)]
    if missing:
        print(f"V položce {args.index} v chapters.py chybí povinné klíče: {', '.join(missing)}")
        return 1

    # Zámek (kontroluje se před načtením CrewAI):
    # - kapitola v knize nebo jiný soubor se stejným názvem (bez číselného prefixu): nikdy se nepřepíše
    # - draft v _drafts/: přepíše se jen s --force a po potvrzení
    # - podobný název (společné slovo): jen upozornění a potvrzení
    conflicts = pipeline.find_conflicts(inputs["vystupni_soubor"])
    if conflicts.blocking:
        existing = [conflicts.target] if conflicts.target else conflicts.same_slug
        print(f"🛑 Kapitola '{inputs['tema']}' už v projektu je: "
              f"{', '.join(display_path(p) for p in existing)}. Kapitola v knize se nepřepisuje.")
        return 1
    if conflicts.similar:
        print("⚠️  V projektu jsou kapitoly s podobným názvem (možné překrytí tématu):")
        for path in conflicts.similar:
            print(f"   - {display_path(path)}")
        if not ask_yes_no("Generovat přesto?"):
            return 1
    if conflicts.draft:
        if not args.force:
            print(f"🛑 Draft {display_path(conflicts.draft)} už existuje. Nepřepisuji (přepsání: --force).")
            return 1
        if not confirm_overwrite([conflicts.draft]):
            return 1

    style_guide = load_style_guide()
    generate_chapter(style_guide, inputs, force=args.force)
    return 0


def cmd_audit(args) -> int:
    if AUDIT_REPORT_PATH.exists():
        if not args.force:
            print(f"🛑 {display_path(AUDIT_REPORT_PATH)} již existuje. Nepřepisuji (přepsání: --force).")
            return 1
        if not confirm_overwrite([AUDIT_REPORT_PATH]):
            return 1
    audit_chapters()
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generátor kapitol a audit učebnice „Statistika pohledem geometra“.")
    commands = parser.add_subparsers(dest="command", required=True)

    style = commands.add_parser("style", help="zkontroluje nebo (s --force) přegeneruje style guide")
    style.add_argument("--force", action="store_true", help="přegenerovat i když existuje (záloha .backup.md)")
    style.set_defaults(handler=cmd_style)

    chapter = commands.add_parser("chapter", help="vygeneruje kapitolu z chapters.py (bez --index vypíše seznam)")
    chapter.add_argument("--index", type=int, help="pořadí kapitoly v chapters.py (od 1)")
    chapter.add_argument("--force", action="store_true", help="přepsat existující soubor kapitoly")
    chapter.set_defaults(handler=cmd_chapter)

    audit = commands.add_parser("audit", help="audit existujících kapitol do audit_report.md")
    audit.add_argument("--force", action="store_true", help="přepsat existující audit_report.md")
    audit.set_defaults(handler=cmd_audit)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.handler(args)


if __name__ == "__main__":
    sys.exit(main())
