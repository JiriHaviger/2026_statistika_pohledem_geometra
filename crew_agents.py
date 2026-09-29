import os
from pathlib import Path
from crewai import Task, Crew, Process

from crew.config import STYLE_GUIDE_PATH, gemini_model  # noqa: F401  (gemini_model použit přes agents)
from crew.prompts import CHAPTER_STRUCTURE
from crew.tools import read_file
from crew.agents import project_manager, content_agent, ojs_agent, reviewer_agent
from chapters import CHAPTERS


# =============================================================================
# FÁZE 1: GENEROVÁNÍ STYLE GUIDE (pouze pokud neexistuje)
# =============================================================================

def generate_style_guide() -> str:
    """
    Jednorázová analýza projektu → Style Guide.
    Spustí se pouze pokud style_guide.md neexistuje.
    """
    print("📋 Style Guide nenalezen – spouštím analýzu projektu...")

    task_style_guide = Task(
        description=f"""
        Analyzuj stávající projekt a vytvoř závazný Style Guide.

        Pomocí nástroje `read_file` prozkoumej:
        1. `_quarto.yml` – struktura, navigace, globální nastavení.
        2. `hag_custom.scss` – barvy, CSS proměnné, custom třídy.
        3. `02-statistika/01_deskriptivní statistiky kvantily.qmd` – ukázka stávajícího textu.

        Style Guide musí obsahovat tyto sekce:

        ## 1. Celkový styl
        Vzdušný styl, krátké odstavce, bezpatkové písmo, hierarchie H2/H3.

        ## 2. Dvojjazyčnost
        Příprava pro přepínač CS/EN, konzistentní struktura v obou jazycích.

        ## 3. Dark / Light mode
        Které CSS proměnné z hag_custom.scss používat v OJS a divech.

        ## 4. Responsive design
        Pravidla pro OJS vizualizace na mobilech (max-width, viewBox).

        ## 5. Barevné schéma pro OJS
        Vypiš konkrétní hex hodnoty z hag_custom.scss jako konstanty pro OJS:
        ```js
        const COLORS = {{
          primary: "#...",
          secondary: "#...",
          accent: "#...",
          // atd.
        }}
        ```

        ## 6. Struktura kapitoly
        Zkopíruj BEZE ZMĚNY tento blok:

        {CHAPTER_STRUCTURE}

        ## 7. Callout třídy
        Jak používat .callout-note, .callout-tip, .callout-warning v kontextu projektu.
        """,
        expected_output=(
            "Kompletní Style Guide v Markdown. "
            "Sekce 6 obsahuje doslovnou kopii šablony struktury kapitoly. "
            "Sekce 5 obsahuje skutečné hex hodnoty z hag_custom.scss."
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

    style_guide_content = str(task_style_guide.output.raw)

    with open(STYLE_GUIDE_PATH, "w", encoding="utf-8") as f:
        f.write(style_guide_content)
    print(f"✅ Style Guide uložen: {STYLE_GUIDE_PATH}")
    return style_guide_content


def load_style_guide() -> str:
    print(f"✅ Style Guide nalezen – načítám z {STYLE_GUIDE_PATH}")
    with open(STYLE_GUIDE_PATH, "r", encoding="utf-8") as f:
        return f.read()


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
