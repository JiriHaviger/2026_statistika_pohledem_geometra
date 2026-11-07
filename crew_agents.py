import os
import shutil
from pathlib import Path
from crewai import Task, Crew, Process

from crew.config import STYLE_GUIDE_PATH
from crew.prompts import CHAPTER_STRUCTURE
from crew.tools import read_file
from crew import style_guide as sg
from crew.agents import project_manager, content_agent, ojs_agent, reviewer_agent
from chapters import CHAPTERS


# =============================================================================
# FÁZE 1: GENEROVÁNÍ STYLE GUIDE (pouze pokud neexistuje)
# =============================================================================

STYLE_SAMPLE_CHAPTER = "02-statistika/02_deskriptivní statistiky momenty.qmd"
STYLE_GUIDE_BACKUP_PATH = "docs_for_agents/style_guide.backup.md"
STYLE_GUIDE_RAW_PATH = "docs_for_agents/style_guide.raw.md"   # surový výstup LLM při chybě


def generate_style_guide() -> str:
    """
    Analýza projektu → Style Guide.
    LLM píše sekce 1–4 a 7, sekce 5 (barvy) a 6 (struktura kapitoly) vkládá Python.
    Výsledek se před uložením zkontroluje; při chybě se style_guide.md nepřepíše.
    Existující style_guide.md se před přepsáním zkopíruje do style_guide.backup.md.
    """
    print("📋 Generuji Style Guide – spouštím analýzu projektu...")

    task_style_guide = Task(
        description=f"""
        Analyzuj stávající projekt „{sg.PROJECT_NAME}“ (Quarto kniha, česky) a napiš části
        závazného Style Guide pro autory nových kapitol.

        Pomocí nástroje `read_file` prozkoumej:
        1. `_quarto.yml` – struktura, navigace, globální nastavení.
        2. `hag_custom.scss` – barvy, proměnné, vlastní třídy, callouty.
        3. `{STYLE_SAMPLE_CHAPTER}` – ukázka stávajícího textu a stylu.

        Napiš PRÁVĚ tyto sekce, s přesně těmito nadpisy a v tomto pořadí:

        ## 1. Celkový styl
        Vzdušný styl, krátké odstavce, bezpatkové písmo, hierarchie H2/H3.

        ## 2. Dvojjazyčnost
        Příprava pro přepínač CS/EN, konzistentní struktura v obou jazycích.

        ## 3. Dark / Light mode
        Fakta: `_quarto.yml` definuje světlé i tmavé téma, ale obě zatím používají stejný
        základ (cosmo + hag_custom.scss), takže tmavý režim zatím není skutečně tmavý.
        Popiš, jak psát divy a OJS grafy, aby fungovaly na světlém i tmavém pozadí
        (barvy z proměnných motivu, ne napevno).

        ## 4. Responsive design
        Pravidla pro OJS vizualizace na mobilech (šířka z vestavěné proměnné `width`,
        čitelné písmo, ovládací prvky vhodné pro dotyk).

        ## 7. Callout třídy
        Jak používat .callout-note, .callout-tip, .callout-warning v kontextu projektu.

        Sekce 5 (barvy) a 6 (struktura kapitoly) NEPIŠ – doplní je program.

        Formát výstupu:
        - Začni přímo nadpisem `## 1. Celkový styl`. Žádná úvodní věta, žádný obalující kódový blok.
        - Pokud uvnitř ukázky potřebuješ kódový blok (např. ```{{ojs}}), dej vnější ukázku
          do ohrady ze ČTYŘ zpětných apostrofů (````markdown … ````).
        - Projekt se jmenuje výhradně „{sg.PROJECT_NAME}“.
        """,
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
        Path(STYLE_GUIDE_RAW_PATH).write_text(raw_output, encoding="utf-8")
        problems = "\n".join(f"  - {e}" for e in errors)
        raise RuntimeError(
            f"Style Guide neprošel kontrolou, {STYLE_GUIDE_PATH} zůstává beze změny.\n"
            f"{problems}\nSurový výstup LLM: {STYLE_GUIDE_RAW_PATH}"
        )

    if Path(STYLE_GUIDE_PATH).exists():
        shutil.copyfile(STYLE_GUIDE_PATH, STYLE_GUIDE_BACKUP_PATH)
        print(f"💾 Původní Style Guide zálohován: {STYLE_GUIDE_BACKUP_PATH}")
    Path(STYLE_GUIDE_PATH).write_text(style_guide_content, encoding="utf-8")
    print(f"✅ Style Guide uložen: {STYLE_GUIDE_PATH}")
    return style_guide_content


def load_style_guide() -> str:
    print(f"✅ Style Guide nalezen – načítám z {STYLE_GUIDE_PATH}")
    content = Path(STYLE_GUIDE_PATH).read_text(encoding="utf-8")
    problems = sg.validate(content) + sg.check_sources(content)
    if problems:
        details = "\n".join(f"  - {p}" for p in problems)
        raise RuntimeError(
            f"Style Guide je zastaralý nebo poškozený:\n{details}\n"
            "Přegeneruj ho (generate_style_guide). Přepínač --force přibude v bloku A3."
        )
    return content


# =============================================================================
# FÁZE 2: GENEROVÁNÍ KAPITOLY
# =============================================================================

def generate_chapter(style_guide: str, inputs: dict) -> None:
    """
    0. zkontroluje jestli kapitola již exsituje – pokud ano, přeskočí generování
    Generuje kapitolu ve třech krocích:
    1. content_agent  → text + příklady + aplikační úlohy
    2. ojs_agent      → OJS bloky pro každou sekci
    3. reviewer_agent → kontrola a finální verze
    """
    output_path = inputs['vystupni_soubor']

    # --- BEZPEČNOSTNÍ ZÁMEK: Ochrana hotových kapitol ---
    if Path(output_path).exists():
        print(f"🛑 Kapitola '{inputs['tema']}' již existuje ({output_path}). SKÁČU JÍ, aby nedošlo k přepsání!")
        return  # Ukončí funkci dříve, než se vůbec spustí CrewAI

    print(f"\n📝 Generuji kapitolu: {inputs['tema']}...")

    # ------------------------------------------------------------------
    # TASK 1: Textový obsah
    # ------------------------------------------------------------------
    task_content = Task(
        description=f"""
        Napiš kompletní textový obsah kapitoly: **{inputs['tema']}**.
        Výstupní soubor: `{inputs['vystupni_soubor']}`.

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
        - Kapitolu začni VŽDY hned pod hlavním nadpisem chytlavým motivačním odstavcem(3–5 vět). Tento odstavec musí nastínit reálný problém z praxe (např. krachující výroba, epidemie, riskantní investice), který bez [klíčová slova] neumíme vyřešit. Musí jasně odpovědět na studentskou otázku: „K čemu mi to v životě bude?".
        - Max. 5 sekcí. Pokud je pojmů více, spoj příbuzné do jedné sekce.
        - Každá sekce: [teorie] → [OJS placeholder] → [1 školský příklad tabset] → [2 self-testy tabset]
        - OJS bloky zatím vlož jako placeholder: ```{{ojs}}\n// OJS_PLACEHOLDER_SEKCE_N\n```
          (ojs_agent je doplní v dalším kroku)
        - Školský příklad: krátké čisté zadání ("Určete P(X=k), pokud X~Bin(10, 0.3)")
        - Self-test: POUZE výsledek v tabu "Výsledek", žádný postup
        - Aplikační úlohy: 2 úlohy, oblasti {inputs.get('aplikacni_oblasti', 'ekonomika/management a medicína')}
          Každá úloha má kontext (reálný příběh) + otázky a), b), c)
        - Závěr: tabulka pojmů + studentský AI prompt
        """,
        expected_output=(
            "Kompletní Quarto Markdown kapitoly. "
            "OJS bloky jako placeholdery. "
            "Struktura: max 5 sekcí, aplikační úlohy, závěr s tabulkou a AI promptem."
        ),
        agent=content_agent
    )

    # ------------------------------------------------------------------
    # TASK 2: OJS vizualizace
    # ------------------------------------------------------------------
    task_ojs = Task(
        description=f"""
        Dostaneš hotový textový obsah kapitoly **{inputs['tema']}**.
        Tvůj úkol: nahraď každý `// OJS_PLACEHOLDER_SEKCE_N` funkční OJS vizualizací.

        ══════════════════════════════════════
        STYLE GUIDE (sekce Barevné schéma pro OJS a Responsive design):
        {style_guide}
        ══════════════════════════════════════

        Požadavky na každou vizualizaci:
        - Ilustruje PRÁVĚ vysvětlený pojem v dané sekci (ne obecnou grafiku).
        - Obsahuje interaktivní prvek: slider pro parametr nebo dropdown pro volbu distribuce.
        - Barvy VÝHRADNĚ z COLORS konstant ze Style Guide.
        - Responsive: používej `width` z OJS, ne pevné px.
        - Každá vizualizace jiná – nerecykluj stejný kód.

        Příklady vhodných vizualizací pro diskrétní distribuce:
        - Sekce Binomická: slider n a p → sloupcový graf PMF + zvýraznění P(X=k)
        - Sekce Poissonova: slider λ → PMF graf + zobrazení střední hodnoty
        - Sekce Geometrická: slider p → graf "čekání na první úspěch"
        - Sekce CDF: interaktivní výpočet P(X ≤ x) s vizuálním zvýrazněním plochy

        Výstupem je CELÝ obsah kapitoly s doplněnými OJS bloky (ne jen OJS bloky samotné).
        """,
        expected_output=(
            "Kompletní Quarto Markdown kapitoly s funkčními OJS vizualizacemi "
            "místo placeholderů. Každá vizualizace je interaktivní a tematicky relevantní."
        ),
        agent=ojs_agent
    )

    # ------------------------------------------------------------------
    # TASK 3: Review
    # ------------------------------------------------------------------
    task_review = Task(
        description=f"""
        Zkontroluj a oprav finální verzi kapitoly **{inputs['tema']}**.

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
        ☐ OJS bloky používají COLORS z Style Guide?
        ☐ OJS bloky jsou interaktivní (slider/dropdown)?

        MATEMATIKA:
        ☐ Vzorce jsou správně (LaTeX syntax pro Quarto)?
        ☐ Číselné výsledky v příkladech jsou správné?

        STYL:
        ☐ Odstavce krátké (max 3–4 věty)?
        ☐ Žádné zbytečné úvody ("V této sekci si ukážeme...")?

        Výstupem je OPRAVENÁ finální verze celé kapitoly.
        Na konec přidej sekci `<!-- REVIEW NOTES -->` se seznamem provedených oprav.
        """,
        expected_output=(
            "Finální opravená verze Quarto Markdown kapitoly. "
            "Na konci souboru sekce <!-- REVIEW NOTES --> se seznamem oprav."
        ),
        output_file=inputs['vystupni_soubor'],
        agent=reviewer_agent
    )

    crew_chapter = Crew(
        agents=[content_agent, ojs_agent, reviewer_agent],
        tasks=[task_content, task_ojs, task_review],
        process=Process.sequential,
        verbose=True,
        max_rpm=10,
    )
    crew_chapter.kickoff()

    # Uložení finální verze (reviewer je poslední)
    output_path = inputs['vystupni_soubor']
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(str(task_review.output.raw))
        print(f"✅ Kapitola uložena: {output_path}")
    except Exception as e:
        print(f"❌ Chyba při zápisu kapitoly: {e}")


# =============================================================================
# FÁZE 3: AUDIT EXISTUJÍCÍCH KAPITOL
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

AUDIT_REPORT_PATH = "docs_for_agents/audit_report.md"


def audit_chapters() -> None:
    """
    Nechá reviewer_agent přečíst všechny obsahové kapitoly a vypsat:
    - duplicitní témata nebo sekce,
    - nesoulad názvu souboru s obsahem,
    - chybějící nebo neúplné části.
    Výsledek se zapíše do docs_for_agents/audit_report.md. Nic se nepřepisuje.
    """
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

    with open(AUDIT_REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\n✅ Audit report uložen: {AUDIT_REPORT_PATH}")


# =============================================================================
# HLAVNÍ LOGIKA
# =============================================================================

if __name__ == "__main__":
    print("🚀 Spouštím CrewAI generátor učebnice...\n")

    # Fáze 1: Style Guide (pouze jednou)
    if Path(STYLE_GUIDE_PATH).exists():
        style_guide = load_style_guide()
    else:
        style_guide = generate_style_guide()

    # Fáze 2: Kapitoly ke generování
    # Seznam kapitol je definován v chapters.py – přidávej je tam.
    # for chapter_inputs in CHAPTERS:
    #    generate_chapter(style_guide, chapter_inputs)

    # Fáze 3: Audit (odkomentuj pro spuštění, generování kapitol pak zakomentuj)
    audit_chapters()

    print("\n🎉 Hotovo!")
