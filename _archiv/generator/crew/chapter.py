"""
Generování kapitoly: autor → OJS → recenzent, mezi kroky pracuje Python (crew/pipeline.py).

Výstup jde do _drafts/<název>.qmd, ne do knihy. Report (REVIEW NOTES, diff recenzenta,
výsledek kontrol a renderu) jde do docs_for_agents/review/<slug>.md.
"""

from datetime import date

from crew import pipeline, prompts
from crew.paths import REVIEW_DIR, display_path


def task_text(instructions: str, style_guide: str | None = None, chapter: str | None = None) -> str:
    """Zadání úkolu: nejdřív podklady (style guide, text kapitoly), potom pokyny z prompts.py."""
    parts = []
    if style_guide:
        parts.append(f"══ ZÁVAZNÝ STYLE GUIDE ══\n{style_guide}")
    if chapter:
        parts.append(f"══ TEXT KAPITOLY ══\n{chapter}")
    parts.append(instructions)
    return "\n\n".join(parts)


def run_single_task(agent, description: str, expected_output: str, tools=None) -> str:
    """Spustí jednoho agenta s jedním úkolem a vrátí jeho surový výstup."""
    from crewai import Task, Crew, Process

    kwargs = {"tools": tools} if tools else {}
    task = Task(description=description, expected_output=expected_output, agent=agent, **kwargs)
    Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=True, max_rpm=10).kickoff()
    return str(task.output.raw)


def _save_failure(slug: str, step: str, raw: str) -> str:
    """Při chybě uloží surový výstup LLM, aby šel prohlédnout; vrací cestu pro výpis."""
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    path = REVIEW_DIR / f"{slug}.{step}.failed.md"
    path.write_text(raw, encoding="utf-8")
    return display_path(path)


# =============================================================================
# REPORT
# =============================================================================

def _fenced(text: str, language: str = "") -> str:
    return f"````{language}\n{text}\n````"


def build_report(slug, inputs, draft_path, *, review_notes, review_errors, review_warnings,
                 review_rejected, findings, render_ok, render_log, diff) -> str:
    mark = lambda ok: "✅" if ok else "❌"
    lines = [
        f"# Report generování: {inputs['tema']}",
        "",
        f"- Datum: {date.today().isoformat()}",
        f"- Draft: `{display_path(draft_path)}`",
        f"- Cílové místo v knize: `{inputs['vystupni_soubor']}` (přesune autor po kontrole)",
        "",
        "## Výsledek kontrol",
        "",
        f"- {mark(not review_rejected)} Recenze zachovala strukturu"
        + ("" if not review_rejected else " – **recenze zamítnuta, v draftu je verze PŘED recenzí**"),
        f"- {mark(not findings)} Statické kontroly ({len(findings)} nálezů)",
        f"- {mark(render_ok)} Kontrolní render (`quarto render`)",
        "",
    ]
    if review_errors or review_warnings:
        lines += ["### Srovnání struktury před a po recenzi", ""]
        lines += [f"- ❌ {e}" for e in review_errors] + [f"- ⚠️ {w}" for w in review_warnings] + [""]
    if findings:
        lines += ["### Nálezy statických kontrol (v draftu zůstaly)", ""] + [f"- {f}" for f in findings] + [""]
    lines += ["## Render", "", _fenced(render_log or "(bez výstupu)"), ""]
    lines += ["## REVIEW NOTES (od recenzenta)", "", review_notes or "_Recenzent žádné poznámky nevrátil._", ""]
    lines += ["## Změny recenzenta (diff)", "", _fenced(diff or "(beze změn)", "diff"), ""]
    return "\n".join(lines)


# =============================================================================
# HLAVNÍ POSTUP
# =============================================================================

def generate_chapter(style_guide: str, inputs: dict, force: bool = False) -> None:
    """
    1. content_agent  → text + příklady + aplikační úlohy (OJS jako placeholdery)
    2. ojs_agent      → JSON {sekce: kód}; Python vloží kód do textu
    3. reviewer_agent → opravená kapitola + poznámky; Python zkontroluje, že nic nezničil
    4. zápis do _drafts/, statické kontroly, kontrolní render, report v docs_for_agents/review/
    Zámek a potvrzení přepsání řeší příkaz `chapter`; tady je pojistka.
    """
    from crew.agents import content_agent, ojs_agent, reviewer_agent
    from crew.tools import calc

    output_file = inputs["vystupni_soubor"]
    draft_path = pipeline.draft_path_for(output_file)
    slug = pipeline.chapter_slug(draft_path.name)

    # --- BEZPEČNOSTNÍ ZÁMEK ---
    conflicts = pipeline.find_conflicts(output_file)
    if conflicts.blocking:
        existing = [conflicts.target] if conflicts.target else conflicts.same_slug
        print(f"🛑 Kapitola '{inputs['tema']}' už v projektu je: "
              f"{', '.join(display_path(p) for p in existing)}. Nepřepisuji.")
        return
    if conflicts.draft and not force:
        print(f"🛑 Draft {display_path(conflicts.draft)} už existuje. Nepřepisuji (přepsání: --force).")
        return

    print(f"\n📝 Generuji kapitolu: {inputs['tema']} → {display_path(draft_path)}")

    # 1) Text kapitoly
    raw_content = run_single_task(
        content_agent, task_text(prompts.content_description(inputs), style_guide=style_guide),
        "Kompletní Quarto Markdown kapitoly podle šablony ze style guide. "
        "OJS bloky jako placeholdery, aplikační úlohy, závěr s tabulkou pojmů. "
        "Všechna čísla spočítaná nástrojem calc.",
        tools=[calc])
    try:
        chapter = pipeline.clean_chapter_output(raw_content)
        numbers = pipeline.placeholder_numbers(chapter)
        pipeline.check_placeholder_numbers(numbers)
    except ValueError as e:
        raise RuntimeError(f"Text kapitoly je nepoužitelný: {e}\n"
                           f"Surový výstup: {_save_failure(slug, 'content', raw_content)}") from e

    # 2) OJS: agent vrací jen JSON, vkládá Python
    raw_ojs = run_single_task(
        ojs_agent,
        task_text(prompts.ojs_description(inputs, numbers, pipeline.inline_ojs_names(chapter)),
                  style_guide=style_guide, chapter=chapter),
        'Jediný JSON objekt {"1": "<kód>", "2": "<kód>", …} s OJS kódem pro každou sekci s grafem.')
    try:
        with_ojs = pipeline.insert_ojs(chapter, pipeline.parse_ojs_json(raw_ojs, numbers))
    except ValueError as e:
        raise RuntimeError(f"OJS kód se nepodařilo vložit: {e}\n"
                           f"Surový výstup: {_save_failure(slug, 'ojs', raw_ojs)}") from e

    # 3) Recenze: dostane i automaticky nalezené problémy
    raw_review = run_single_task(
        reviewer_agent,
        task_text(prompts.review_description(inputs, pipeline.check_chapter(with_ojs)),
                  style_guide=style_guide, chapter=with_ojs),
        f"Celá opravená kapitola, pak řádek {prompts.REVIEW_MARKER} a seznam oprav.",
        tools=[calc])
    review_errors: list[str] = []
    review_warnings: list[str] = []
    review_notes = ""
    final = with_ojs
    try:
        reviewed, review_notes = pipeline.split_review_output(raw_review)
        review_errors, review_warnings = pipeline.compare_structure(with_ojs, reviewed)
        if not review_errors:
            final = reviewed
    except ValueError as e:
        review_errors.append(str(e))
    review_rejected = bool(review_errors)
    if review_rejected:
        print(f"⚠️  Recenze zamítnuta: {'; '.join(e.rstrip('.') for e in review_errors)}. "
              f"Surový výstup: {_save_failure(slug, 'review', raw_review)}")

    # 4) Zápis draftu, kontroly, render, report
    draft_path.parent.mkdir(parents=True, exist_ok=True)
    draft_path.write_text(final, encoding="utf-8")
    print(f"✅ Draft uložen: {display_path(draft_path)}")

    findings = pipeline.check_chapter(final)
    render_ok, render_log = pipeline.render_draft(draft_path)
    report = build_report(
        slug, inputs, draft_path, review_notes=review_notes, review_errors=review_errors,
        review_warnings=review_warnings, review_rejected=review_rejected, findings=findings,
        render_ok=render_ok, render_log=render_log, diff=pipeline.unified_diff(with_ojs, final))
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REVIEW_DIR / f"{slug}.md"
    report_path.write_text(report, encoding="utf-8")
    print(f"📋 Report: {display_path(report_path)}  "
          f"(kontroly: {'v pořádku' if not findings else str(len(findings)) + ' nálezů'}, "
          f"render: {'OK' if render_ok else 'SELHAL'})")
