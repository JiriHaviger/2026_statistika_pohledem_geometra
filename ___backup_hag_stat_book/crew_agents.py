import os
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"
os.environ["CREWAI_TRACING_ENABLED"] = "false"
os.environ["GEMINI_API_KEY"] = "AIzaSyDJOH9c6stLvoqtjPReMosaScFhZEN0mzM"

from pathlib import Path
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool

# ----------------- NASTAVENÍ -----------------
load_dotenv()

gemini_model = LLM(
    model="gemini/gemini-2.5-flash", # Flash je na výpadky 503 mnohem méně náchylný než "Pro"
    api_key=os.environ["GEMINI_API_KEY"],
    max_retries=5,       # Pokud Google hodí 503, CrewAI to automaticky zkusí znovu (až 5x)
)


STYLE_GUIDE_PATH = "style_guide.md"

# ----------------- NÁSTROJE -----------------
@tool("Čtečka souborů")
def read_file(file_path: str) -> str:
    """Přečte obsah souboru z disku. Vstupem je přesná cesta k souboru."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Chyba při čtení souboru {file_path}: {str(e)}"


# =============================================================================
# ŠABLONA STRUKTURY KAPITOLY  (Cognitive Load Theory)
# Toto je pevná kostra – content agent ji VŽDY dodržuje.
# Mění se pouze obsah (téma, pojmy, příklady), nikdy struktura.
# =============================================================================

CHAPTER_STRUCTURE = """
## ZÁVAZNÁ STRUKTURA KAŽDÉ KAPITOLY (Cognitive Load Theory)

# Pokyny pro začátek kapitoly:
# Hned pod hlavní nadpis kapitoly (H1 / #) vlož motivační odstavec.
# Tento odstavec nastíní reálný, praktický problém z oblasti ekonomiky, 
# managementu nebo medicíny, který bez znalosti této kapitoly nelze efektivně vyřešit.
# Odstavec musí studenta vtáhnout do děje a ukázat mu, PROČ se dané téma učí.
# Rozsah: 3–5 vět. Žádné klišé typu "V této kapitole se podíváme...".

Kapitola se skládá z maximálně 5 sekcí + závěrečného bloku.

Každá sekce pokrývá JEDEN koncept. Kratší je lepší.

---

### SEKCE  (opakuj max. 5×)

```
## N. Název sekce  ← jeden pojem / jeden krok

[TEORIE – max. 3 krátké odstavce]
Vzdušný text. Každý odstavec = jedna myšlenka. Bez zbytečných úvodů.
Geometrická nebo intuitivní interpretace pojmu.

[INTERAKTIVNÍ GRAFIKA – povinná, právě 1 na sekci]
```{ojs}
// Observable JS vizualizace ilustrující právě vysvětlený pojem.
// Slider nebo dropdown pro interakci studenta.
// Barvy VÝHRADNĚ z CSS proměnných Style Guide.
```

[ŠKOLSKÝ PŘÍKLAD – právě 1 na sekci]
Krátké, čisté zadání ve tvaru:
  "Určete P(X = k), pokud X ~ Bin(n, p) a víte, že n = 10, p = 0,3."

::: {.panel-tabset}
## Zadání
Krátké čisté zadání. Jen čísla a co se hledá, žádný příběh.

## Postup
Groebner styl – každý krok má číslo a komentář proč, ne jen výpočet:

**Krok 1: Identifikujeme parametry.**
[co je n, p, k a proč]

**Krok 2: Dosadíme do vzorce.**
[vzorec s dosazenými hodnotami]

**Krok 3: Vypočítáme.**
[výpočet]

**Výsledek: [hodnota tučně]**

## Výsledek
**Výsledek: [hodnota tučně]**
Pouze finální číslo – pro rychlou kontrolu bez čtení postupu.
:::

[SELF-TEST PŘÍKLADY – právě 2 na sekci, BEZ postupu]

::: {.panel-tabset}
## Zadání
Text pro samostatné procvičení (obměna školského příkladu).

## Výsledek
**Výsledek: [hodnota s jednotkou]**
Žádný postup. Pouze finální číslo.
:::

[AI PROMPT – právě 1 na sekci, za self-testy]
Prompt pro okamžité dovysvětlení právě probíraného pojmu.
Musí být konkrétní – obsahuje název pojmu, kontext (ekonomie/medicína)
a instrukci pro dialogický režim (AI čeká na odpověď studenta).

::: {.callout-tip collapse="true" icon=false}
## 💬 Zeptej se AI
Zkopíruj do ChatGPT / Claude / Copilota / Gemini:

> Jsi trpělivý tutor statistiky pro studenty ekonomie.
> Odpovídáš stručně (max. 3–4 věty), pak se ptáš jestli to dává smysl.
> Symboly a vzorce používáš jen když jsou nezbytné.
> Nikdy nevysvětluješ víc věcí najednou.
> Vždy ukazuješ obecný postup, ne trik platný jen pro tento příklad.
> Mluvíš česky.
>
> [Konkrétní otázka cílená na právě vysvětlený pojem –
> agent doplní podle obsahu sekce, např.:
> "Nerozumím proč u Poissonovy distribuce platí E(X) = λ = Var(X).
> Můžeš mi to ukázat na příkladu z pojišťovnictví?"]
:::
```

---

### APLIKAČNÍ ÚLOHY  (samostatný blok, JEDNOU za kapitolu, za všemi sekcemi)

Tento blok obsahuje 2–3 delší úlohy z reálné praxe.
Oblasti: ekonomika a management, nebo medicína a veřejné zdraví.
Inspirace stylem: Elementary Linear Algebra (Anton), Grinstead & Snell.

Každá aplikační úloha má:
- **Kontext** (2–4 věty reálného příběhu, ne abstraktní zadání)
- **Více dílčích otázek** označených a), b), c) – budují na sobě
- Tabset Zadání / Řešení

Příklady kontextů (agent vždy vymyslí nové, podobného duchu):
- Výrobní linka: počet vadných kusů za směnu ~ Poisson(λ)
- Klinická studie: pravděpodobnost vedlejšího účinku u n pacientů ~ Bin(n, p)
- Pojišťovna: počet škodních událostí za rok, nastavení pojistného
- Zákaznická linka: počet hovorů za hodinu, dimenzování kapacity

Formát:

::: {.callout-note icon=false}
## 🏭 Aplikační úloha: [Název kontextu]

[2–4 věty kontextu]

**a)** ...
**b)** ...
**c)** ...
:::

::: {.panel-tabset}
## Zadání (shrnutí)
Stručné shrnutí všech otázek a), b), c).

## Řešení
Řešení každé podotázky zvlášť, s komentářem k interpretaci výsledku.
:::

---

### ZÁVĚR KAPITOLY  (vždy poslední blok)

#### Shrnutí pojmů
Tabulka: | Pojem | Definice | Kdy použít |
(max. 5 řádků – jen klíčové pojmy kapitoly)

#### Pracuj s AI

Tři připravené prompty pro různé potřeby – student zkopíruje a vloží do
ChatGPT / Claude / Copilota / jiného AI nástroje.

Každý prompt začíná **systémovou rolí** která nastaví AI jako konkrétní typ tutora,
pak teprve přichází samotná otázka. Student roli nekrátí ani neupravuje.

**Něco mi nešlo – chci dovysvětlit:**
> Jsi trpělivý tutor statistiky. Vysvětluješ studentům ekonomie.
> Pravidla, která vždy dodržuješ:
> – Odpovídáš stručně (max. 3–4 věty), pak se zeptáš jestli to dává smysl.
> – Matematické symboly a vzorce používáš jen když jsou nezbytné,
>   jinak raději slovní popis nebo číselný příklad.
> – Nikdy nevysvětluješ víc věcí najednou.
> – Pokud si nejsi jistý co student nechápe, nejdřív se zeptej.
> – Vždy ukazuješ OBECNÝ postup který funguje pro libovolný příklad,
>   ne trik nebo zkratku platnou jen pro toto konkrétní zadání.
>   Pokud existuje více postupů, řekni to a drž se obecného.
> – Mluvíš česky.
>
> Moje otázka: Nerozumím [konkrétní pojem z kapitoly].
> Můžeš mi to vysvětlit na příkladu z [obor]?

**Chci si procvičit:**
> Jsi tutor statistiky, který procvičuje studenty formou dialogu.
> Pravidla, která vždy dodržuješ:
> – Dáš mi jedno zadání, počkáš na mou odpověď, pak opravíš nebo potvrdíš.
> – Nápovědu dáváš jen když o ni požádám slovem "nápověda".
> – Zadání jsou krátká a numerická (ne dlouhé příběhy).
> – Obtížnost postupně zvyšuješ – začínáš snadno.
> – Mluvíš česky.
>
> Téma: [konkrétní pojem z kapitoly]. Začni prvním příkladem.

**Chci jít do hloubky:**
> Jsi tutor statistiky, který propojuje teorii s praxí.
> Pravidla, která vždy dodržuješ:
> – Začínáš vždy reálnou situací z praxe, vzorec přichází až potom.
> – Používáš konkrétní čísla, ne obecné proměnné (raději n=50 než "nějaké n").
> – Vždy ukazuješ OBECNÝ postup který funguje pro libovolný příklad.
>   Pokud existuje elegantnější zkratka jen pro tento případ, zmíníš ji,
>   ale jako doplněk – ne jako hlavní postup.
> – Po každém celku se zeptáš jestli chci pokračovat nebo se vrátit.
> – Mluvíš česky.
>
> Zajímá mě: jak se [konkrétní pojem] používá v praxi v [obor]?
> Ukaž mi reálný příklad s čísly.

INSTRUKCE PRO AGENTA:
- Nahraď všechny [hranaté závorky] konkrétním textem pro tuto kapitolu.
- Systémové role (Jsi tutor...) NEMĚŇ – jsou záměrně obecné aby fungovaly
  v jakémkoli AI nástroji (ChatGPT, Claude, Copilot, Gemini).
- Ve výsledném .qmd nesmí zůstat žádný placeholder v [hranatých závorkách].
"""


# ----------------- AGENTI -----------------
project_manager = Agent(
    role="Projektový manažer a stylový strážce",
    goal="Udržovat konzistentní styl, strukturu i barevné schéma celé učebnice.",
    backstory="Jsi velmi pečlivý koordinátor vzdělávacího projektu.",
    llm=gemini_model,
    verbose=True
)

content_agent = Agent(
    role="Autor statistiky a lineární algebry",
    goal="Psát kvalitní obsah v češtině podle přesných pravidel.",
    backstory=(
        "Zkušený lektor statistiky. Tvůj styl je inspirován Grinstead & Snell "
        "(Introductory Probability) a Anton (Elementary Linear Algebra): "
        "jasné definice, krátké odstavce, reálné příklady z ekonomiky a medicíny."
    ),
    llm=gemini_model,
    verbose=True
)

ojs_agent = Agent(
    role="Specialista na Observable JS",
    goal="Vytvářet interaktivní prvky s konzistentním barevným schématem.",
    backstory="Expert na Observable JS a data vizualizace.",
    llm=gemini_model,
    verbose=True
)

reviewer_agent = Agent(
    role="Recenzent a finální editor",
    goal="Kontrolovat dodržení všech pravidel včetně barevné konzistence.",
    backstory="Přísný matematik a editor.",
    llm=gemini_model,
    verbose=True
)


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
"""
    Generuje kapitolu pouze v případě, že výsledný soubor ještě neexistuje.
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
        - Kapitolu začni VŽDY hned pod hlavním nadpisem chytlavým motivačním odstavcem(3–5 vět). Tento odstavec musí nastínit reálný problém z praxe (např. krachující výroba, epidemie, riskantní investice), který bez [klíčová slova] neumíme vyřešit. Musí jasně odpovědět na studentskou otázku: „K čemu mi to v životě bude?“.
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
    # Přidávej další kapitoly jako položky seznamu.
    # `aplikacni_oblasti` je nepovinné – výchozí hodnota je "ekonomika/management a medicína"
    chapters = [
        {
            "tema": "Diskrétní pravděpodobnostní rozdělení",
            "vystupni_soubor": "02-statistika/05_diskretni_distribuce.qmd",
            "klicove_pojmy": """
                1. Binomická distribuce – model opakovaných pokusů s dvěma výsledky
                2. Poissonova distribuce – model vzácných událostí v čase nebo prostoru
                3. Geometrická distribuce – model čekání na první úspěch
                4. Kumulativní distribuční funkce (CDF) – výpočet P(X ≤ x)
                5. Střední hodnota a rozptyl – interpretace parametrů rozdělení
            """,
            "zamereni_uloh": """
                - Výpočet P(X = k) z PMF
                - Výpočet P(X ≤ k) a P(X > k) z CDF
                - Určení kvantilu: najdi k tak, aby P(X ≤ k) ≥ p
                - Výpočet E(X) a Var(X) ze zadaných parametrů
                - Rozhodnutí, které rozdělení použít v dané situaci
            """,
            "nastroje": "R (dbinom, dpois, dgeom, pbinom), Python (scipy.stats), Excel (BINOM.DIST)",
            "aplikacni_oblasti": "pojišťovnictví/management výroby a epidemiologie/klinické studie",
        },
        # Příklad další kapitoly – odkomentuj a uprav:
        # {
        #     "tema": "Spojitá pravděpodobnostní rozdělení",
        #     "vystupni_soubor": "02-statistika/06_spojita_rozdeleni.qmd",
        #     "klicove_pojmy": "Normální rozdělení, Exponenciální rozdělení, ...",
        #     "zamereni_uloh": "...",
        #     "nastroje": "R, Python, Excel",
        #     "aplikacni_oblasti": "finance/řízení zásob a medicína",
        # },
    ]

    for chapter_inputs in chapters:
        generate_chapter(style_guide, chapter_inputs)

    print("\n🎉 Hotovo!")
