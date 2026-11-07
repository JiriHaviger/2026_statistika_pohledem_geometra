"""
Generování kapitoly: autor → OJS → recenzent, mezi kroky pracuje Python (crew/pipeline.py).

Výstup jde do _drafts/<název>.qmd, ne do knihy. Report (REVIEW NOTES, diff recenzenta,
výsledek kontrol a renderu) jde do docs_for_agents/review/<slug>.md.
"""

from datetime import date

from crew import pipeline
from crew.paths import REVIEW_DIR, display_path
from crew.prompts import CHAPTER_STRUCTURE


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
# ZADÁNÍ PRO AGENTY
# =============================================================================

def content_description(style_guide: str, inputs: dict) -> str:
    return f"""
        Napiš kompletní textový obsah kapitoly: **{inputs['tema']}**.
        Kapitola bude po kontrole zařazena jako `{inputs['vystupni_soubor']}`.

        ══════════════════════════════════════
        ZÁVAZNÝ STYLE GUIDE:
        {style_guide}
        ══════════════════════════════════════

        ZÁVAZNÁ STRUKTURA KAPITOLY:
        {CHAPTER_STRUCTURE}
        ══════════════════════════════════════

        OBSAH KAPITOLY:

        Hlavní témata (rozděl do max. 5 sekcí, každá = 1 pojem):
        {inputs['klicove_pojmy']}

        Zaměření příkladů:
        {inputs['zamereni_uloh']}

        Nástroje pro kódové bloky:
        {inputs['nastroje']}

        PRAVIDLA, která NESMÍŠ porušit:
        - Začni přímo nadpisem první úrovně `# Název kapitoly` (bez YAML hlavičky a bez úvodní věty).
        - Kapitolu začni VŽDY hned pod hlavním nadpisem chytlavým motivačním odstavcem(3–5 vět). Tento odstavec musí nastínit reálný problém z praxe (např. krachující výroba, epidemie, riskantní investice), který bez [klíčová slova] neumíme vyřešit. Musí jasně odpovědět na studentskou otázku: „K čemu mi to v životě bude?".
        - Max. 5 sekcí. Pokud je pojmů více, spoj příbuzné do jedné sekce.
        - Každá sekce: [teorie] → [OJS placeholder] → [1 školský příklad tabset] → [2 self-testy tabset]
        - OJS bloky zatím vlož jako placeholder: ```{{ojs}}\n// OJS_PLACEHOLDER_SEKCE_N\n```
          (N = pořadí sekce 1, 2, 3 …; ojs_agent je doplní v dalším kroku)
        - Školský příklad: krátké čisté zadání ("Určete P(X=k), pokud X~Bin(10, 0.3)")
        - Self-test: POUZE výsledek v tabu "Výsledek", žádný postup
        - Aplikační úlohy: 2 úlohy, oblasti {inputs.get('aplikacni_oblasti', 'ekonomika/management a medicína')}
          Každá úloha má kontext (reálný příběh) + otázky a), b), c)
        - Závěr: tabulka pojmů + studentský AI prompt
        """


def ojs_description(style_guide: str, inputs: dict, chapter: str, numbers: list[int]) -> str:
    return f"""
        Pro kapitolu **{inputs['tema']}** napiš OJS (Observable JS) vizualizace do míst označených
        `// OJS_PLACEHOLDER_SEKCE_N`. Sekce s grafem jsou: {numbers}.

        ══════════════════════════════════════
        STYLE GUIDE (sekce Barevné schéma pro OJS a Responsive design):
        {style_guide}
        ══════════════════════════════════════

        TEXT KAPITOLY (graf musí ilustrovat právě pojem vysvětlený v dané sekci):
        {chapter}
        ══════════════════════════════════════

        Požadavky na každou vizualizaci:
        - Ilustruje PRÁVĚ vysvětlený pojem v dané sekci (ne obecnou grafiku).
        - Obsahuje interaktivní prvek: slider pro parametr nebo dropdown pro volbu.
        - Barvy VÝHRADNĚ z objektu `C` (modul assets/jhrules.js), žádné hex barvy ani pojmenované barvy.
        - Responsive: používej vestavěnou proměnnou `width`, žádná pevná číselná šířka.
        - Každá vizualizace jiná – nerecykluj stejný kód.

        PRAVIDLA OJS, která NESMÍŠ porušit (všechny buňky kapitoly sdílejí jeden globální prostor):
        - Názvy proměnných definovaných na začátku řádku (`x = …`, `viewof x = …`) musí být unikátní
          v CELÉ kapitole. Přidej příponu podle sekce (např. `n1`, `p1`, `chart1`, `n2`, …).
        - `import {{C, gradient, plotStyle}} from "../assets/jhrules.js"` patří POUZE do kódu sekce 1,
          do ostatních sekcí import nedávej (C, gradient i plotStyle jsou už definované).
        - Jiné importy nepoužívej. `Inputs`, `Plot` i `d3` jsou dostupné bez importu.

        FORMÁT VÝSTUPU – pouze jeden JSON objekt, žádný jiný text, žádný obalující kódový blok:
        {{"1": "<celý OJS kód sekce 1>", "2": "<celý OJS kód sekce 2>", …}}
        Klíče jsou čísla sekcí {numbers}, hodnoty jsou řetězce s kódem (nový řádek jako \\n).
        Kód nezačíná ```{{ojs}} ani nekončí ```: vkládá se do bloku automaticky.
        """


def review_description(inputs: dict, chapter: str, findings: list[str]) -> str:
    findings_text = "\n".join(f"- {f}" for f in findings) if findings else "- žádné"
    return f"""
        Zkontroluj a oprav finální verzi kapitoly **{inputs['tema']}**.

        AUTOMATICKY NALEZENÉ PROBLÉMY (oprav je):
        {findings_text}

        Checklist – ověř každý bod:

        STRUKTURA:
        ☐ Max. 5 sekcí? (pokud více, slučte)
        ☐ Každá sekce má: teorie → OJS → školský příklad → 2 self-testy?
        ☐ Aplikační úlohy jsou odděleny jako samostatný blok za sekcemi?
        ☐ Závěr obsahuje tabulku pojmů a studentský AI prompt?

        PŘÍKLADY:
        ☐ Školský příklad: krátké čisté zadání + tabset Zadání/Řešení?
        ☐ Self-testy: tabset Zadání/Výsledek, BEZ postupu v záložce Výsledek?
        ☐ Aplikační úlohy: reálný kontext + otázky a)/b)/c) + tabset?

        OJS:
        ☐ Každá sekce má právě 1 OJS blok (ne placeholder)?
        ☐ OJS bloky berou barvy z objektu C (žádné hex barvy)?
        ☐ OJS bloky jsou interaktivní (slider/dropdown)?

        MATEMATIKA:
        ☐ Vzorce jsou správně (LaTeX syntax pro Quarto)?
        ☐ Číselné výsledky v příkladech jsou správné?

        STYL:
        ☐ Odstavce krátké (max 3–4 věty)?
        ☐ Žádné zbytečné úvody ("V této sekci si ukážeme...")?

        PRAVIDLA ÚPRAV:
        - OJS bloky nepřepisuj, pokud nejsou prokazatelně chybné; nepřidávej ani neodebírej sekce.
        - Text nezkracuj.

        FORMÁT VÝSTUPU:
        1. Nejdřív CELÁ opravená kapitola (čisté Quarto Markdown, bez obalujícího kódového bloku,
           bez jakýchkoli poznámek v textu).
        2. Pak samostatný řádek přesně `{pipeline.REVIEW_MARKER}` a pod ním seznam provedených oprav.

        ══════════════════════════════════════
        KAPITOLA K REVIZI:
        {chapter}
        """


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
        content_agent, content_description(style_guide, inputs),
        "Kompletní Quarto Markdown kapitoly. OJS bloky jako placeholdery. "
        "Struktura: max 5 sekcí, aplikační úlohy, závěr s tabulkou a AI promptem.")
    try:
        chapter = pipeline.clean_chapter_output(raw_content)
        numbers = pipeline.placeholder_numbers(chapter)
        pipeline.check_placeholder_numbers(numbers)
    except ValueError as e:
        raise RuntimeError(f"Text kapitoly je nepoužitelný: {e}\n"
                           f"Surový výstup: {_save_failure(slug, 'content', raw_content)}") from e

    # 2) OJS: agent vrací jen JSON, vkládá Python
    raw_ojs = run_single_task(
        ojs_agent, ojs_description(style_guide, inputs, chapter, numbers),
        'Jediný JSON objekt {"1": "<kód>", "2": "<kód>", …} s OJS kódem pro každou sekci s grafem.')
    try:
        with_ojs = pipeline.insert_ojs(chapter, pipeline.parse_ojs_json(raw_ojs, numbers))
    except ValueError as e:
        raise RuntimeError(f"OJS kód se nepodařilo vložit: {e}\n"
                           f"Surový výstup: {_save_failure(slug, 'ojs', raw_ojs)}") from e

    # 3) Recenze: dostane i automaticky nalezené problémy
    raw_review = run_single_task(
        reviewer_agent, review_description(inputs, with_ojs, pipeline.check_chapter(with_ojs)),
        f"Celá opravená kapitola, pak řádek {pipeline.REVIEW_MARKER} a seznam oprav.")
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
