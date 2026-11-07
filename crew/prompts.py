"""
JEDINÉ místo se specifikací kapitoly a se všemi texty zadání pro agenty.

Počty a názvy záložek jsou konstanty nahoře. Šablona kapitoly (CHAPTER_STRUCTURE),
zadání pro autora i checklist recenzenta se z nich skládají, takže si odporovat nemohou.
Kontroly v crew/pipeline.py berou stejné konstanty.

Modul nemá závislosti na crewai ani na API klíči.
"""

import re

from crew.paths import project_path

# =============================================================================
# SPECIFIKACE (jediný zdroj pravdy)
# =============================================================================

MAX_SECTIONS = 5                   # obsahových sekcí v kapitole
SELF_TESTS_PER_SECTION = 2
AI_PROMPTS_PER_SECTION = 1
APPLICATION_TASKS = "2–3"          # aplikačních úloh v kapitole
SCHOOL_TABS = ["Zadání", "Postup", "Výsledek"]
SELFTEST_TABS = ["Zadání", "Výsledek"]
APPLICATION_TABS = ["Zadání (shrnutí)", "Řešení"]
DEFAULT_APPLICATION_AREAS = "ekonomika/management a medicína"

OJS_EXAMPLES_PATH = "docs_for_agents/ojs_vzory.qmd"


def _fill(template: str) -> str:
    """Dosadí konstanty za značky @NÁZEV@ (složené závorky v šabloně jsou obsah, ne formátování)."""
    values = {
        "MAX_SECTIONS": str(MAX_SECTIONS),
        "SELF_TESTS": str(SELF_TESTS_PER_SECTION),
        "AI_PROMPTS": str(AI_PROMPTS_PER_SECTION),
        "APPLICATION_TASKS": APPLICATION_TASKS,
        "SCHOOL_TABS": " / ".join(SCHOOL_TABS),
        "SELFTEST_TABS": " / ".join(SELFTEST_TABS),
        "APPLICATION_TABS": " / ".join(APPLICATION_TABS),
    }
    return re.sub(r"@([A-Z_]+)@", lambda m: values[m.group(1)], template)


# =============================================================================
# ŠABLONA STRUKTURY KAPITOLY  (Cognitive Load Theory)
# Pevná kostra – content agent ji VŽDY dodržuje. Mění se obsah, nikdy struktura.
# Vnější ohrady ze čtyř zpětných apostrofů obalují ukázky, které obsahují ``` uvnitř.
# =============================================================================

CHAPTER_STRUCTURE = _fill("""
**ZÁVAZNÁ STRUKTURA KAŽDÉ KAPITOLY (Cognitive Load Theory)**

> POKYN – začátek kapitoly:
> Hned pod hlavní nadpis kapitoly (H1) vlož motivační odstavec.
> Tento odstavec nastíní reálný, praktický problém z oblasti ekonomiky,
> managementu nebo medicíny, který bez znalosti této kapitoly nelze efektivně vyřešit.
> Odstavec musí studenta vtáhnout do děje a ukázat mu, PROČ se dané téma učí.
> Rozsah: 3–5 vět. Žádné klišé typu "V této kapitole se podíváme...".

Šablony ve vnější ohradě ze čtyř zpětných apostrofů (````) se kopírují BEZ této vnější ohrady.

Kapitola se skládá z nejvýše @MAX_SECTIONS@ sekcí, bloku aplikačních úloh a závěru.
Každá sekce pokrývá JEDEN koncept. Kratší je lepší.

---

### SEKCE  (opakuj nejvýše @MAX_SECTIONS@×)

````markdown
## N. Název sekce  ← jeden pojem / jeden krok

[TEORIE – max. 3 krátké odstavce]
Vzdušný text. Každý odstavec = jedna myšlenka. Bez zbytečných úvodů.

[GEOMETRICKÝ POHLED – povinný, 1 odstavec]
Co pojem znamená geometricky: těžiště, vzdálenost, projekce, plocha, úhel, vektor …
Vzor: průměr jako těžiště na houpačce. Graf v dalším bloku má tento pohled ukazovat.
Výjimka jen tehdy, když pojem geometrický význam opravdu nemá: napiš jednu větu
„Geometrický pohled: žádný, protože [důvod].“ a použij intuitivní interpretaci.

[INTERAKTIVNÍ GRAFIKA – povinná, právě 1 na sekci]
Vlož přesně tento blok, N nahraď číslem sekce (1, 2, 3 …). Graf doplní ojs_agent.
```{ojs}
// OJS_PLACEHOLDER_SEKCE_N
```

[ŠKOLSKÝ PŘÍKLAD – právě 1 na sekci]
Krátké, čisté zadání ve tvaru:
  "Určete [hledanou veličinu], pokud [zadané hodnoty]."

::: {.panel-tabset}
## Zadání
Krátké čisté zadání. Jen čísla a co se hledá, žádný příběh.

## Postup
Groebner styl – každý krok má číslo a komentář proč, ne jen výpočet:

**Krok 1: Identifikujeme zadané veličiny.**
[co je zadáno a proč na tom záleží]

**Krok 2: Zvolíme postup a dosadíme.**
[vzorec s dosazenými hodnotami]

**Krok 3: Vypočítáme.**
[výpočet]

**Výsledek: [hodnota tučně]**

## Výsledek
**Výsledek: [hodnota tučně]**
Pouze finální číslo – pro rychlou kontrolu bez čtení postupu.
:::

[SELF-TEST PŘÍKLADY – právě @SELF_TESTS@ na sekci, BEZ postupu]

::: {.panel-tabset}
## Zadání
Text pro samostatné procvičení (obměna školského příkladu).

## Výsledek
**Výsledek: [hodnota s jednotkou]**
Žádný postup. Pouze finální číslo.
:::

[AI PROMPT – právě @AI_PROMPTS@ na sekci, za self-testy]
Prompt pro okamžité dovysvětlení právě probíraného pojmu.
Musí být konkrétní – obsahuje název pojmu, kontext (ekonomie/medicína)
a instrukci pro dialogický režim (AI čeká na odpověď studenta).

::: {.callout-tip collapse="true" icon=false}
## Zeptej se AI
Zkopíruj do ChatGPT / Claude / Copilota / Gemini:

> Jsi trpělivý tutor statistiky pro studenty ekonomie.
> Odpovídáš stručně (max. 3–4 věty), pak se ptáš jestli to dává smysl.
> Symboly a vzorce používáš jen když jsou nezbytné.
> Nikdy nevysvětluješ víc věcí najednou.
> Vždy ukazuješ obecný postup, ne trik platný jen pro tento příklad.
> Mluvíš česky.
>
> [Konkrétní otázka cílená na právě vysvětlený pojem – agent doplní podle obsahu sekce
> ve tvaru: "Nerozumím, proč [konkrétní tvrzení nebo krok z této sekce].
> Můžeš mi to ukázat na příkladu z [obor]?"]
:::
````

---

### APLIKAČNÍ ÚLOHY  (samostatný blok, JEDNOU za kapitolu, za všemi sekcemi)

Nadpis bloku je `## Aplikační úlohy`.
Blok obsahuje @APPLICATION_TASKS@ delší úlohy z reálné praxe.
Oblasti: ekonomika a management, nebo medicína a veřejné zdraví.
Inspirace stylem: Elementary Linear Algebra (Anton), Grinstead & Snell.

Každá aplikační úloha má:
- **Kontext** (2–4 věty reálného příběhu, ne abstraktní zadání)
- **Více dílčích otázek** označených a), b), c) – budují na sobě
- Tabset @APPLICATION_TABS@

Příklady kontextů (agent vždy vymyslí nové, podobného duchu; nezmiňuj názvy rozdělení ani vzorců):
- Výrobní linka: kontrola kvality jedné směny a rozhodnutí o zásahu
- Klinická studie: vyhodnocení účinku léčby u skupiny pacientů
- Pojišťovna: škodní události a nastavení pojistného
- Zákaznická linka: počet hovorů za hodinu a dimenzování kapacity

Formát:

````markdown
::: {.callout-note icon=false}
## Aplikační úloha: [Název kontextu]

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
````

---

### ZÁVĚR KAPITOLY  (vždy poslední blok)

Nadpis bloku je `## Shrnutí pojmů`.
Obsahuje tabulku: | Pojem | Definice | Kdy použít |
(max. 5 řádků – jen klíčové pojmy kapitoly). Nic dalšího.

INSTRUKCE PRO AGENTA:
- Nahraď všechny [hranaté závorky] konkrétním textem pro tuto kapitolu.
- Systémové role (Jsi tutor...) NEMĚŇ – jsou záměrně obecné aby fungovaly
  v jakémkoli AI nástroji (ChatGPT, Claude, Copilot, Gemini).
- Ve výsledném .qmd nesmí zůstat žádný placeholder v [hranatých závorkách].
""")


def review_checklist() -> str:
    """Checklist recenzenta, odvozený ze stejných konstant jako šablona."""
    return _fill("""
        STRUKTURA:
        ☐ Nejvýše @MAX_SECTIONS@ sekcí? (pokud více, slučte)
        ☐ Každá sekce má: teorie → geometrický pohled → OJS → školský příklad → @SELF_TESTS@ self-testy → @AI_PROMPTS@ AI prompt?
        ☐ Každá sekce má geometrický pohled, nebo větu „Geometrický pohled: žádný, protože …“?
        ☐ Aplikační úlohy (@APPLICATION_TASKS@) jsou samostatný blok `## Aplikační úlohy` za sekcemi?
        ☐ Závěr `## Shrnutí pojmů` obsahuje jen tabulku (max. 5 řádků)?

        PŘÍKLADY:
        ☐ Školský příklad: krátké čisté zadání + tabset @SCHOOL_TABS@?
        ☐ Self-testy: tabset @SELFTEST_TABS@, BEZ postupu v záložce Výsledek?
        ☐ Aplikační úlohy: reálný kontext + otázky a)/b)/c) + tabset @APPLICATION_TABS@?

        OJS:
        ☐ Každá sekce má právě 1 OJS blok (ne placeholder)?
        ☐ OJS bloky berou barvy z objektu C (žádné hex barvy)?
        ☐ OJS bloky jsou interaktivní (slider/dropdown) a ukazují geometrický pohled sekce?

        MATEMATIKA:
        ☐ Vzorce jsou správně (LaTeX syntax pro Quarto)?
        ☐ Číselné výsledky v příkladech jsou správné (přepočítané nástrojem calc, ne z hlavy)?

        STYL:
        ☐ Odstavce krátké (max 3–4 věty)?
        ☐ Žádné zbytečné úvody ("V této sekci si ukážeme...")?
        ☐ Nadpisy callout a záložek bez emoji?
        """)


# =============================================================================
# ZADÁNÍ PRO AGENTY
# =============================================================================

REVIEW_MARKER = "=== REVIEW NOTES ==="


def style_guide_description(project_name: str, sample_chapter: str) -> str:
    return f"""
        Analyzuj stávající projekt „{project_name}“ (Quarto kniha, česky) a napiš části
        závazného Style Guide pro autory nových kapitol.

        Pomocí nástroje `read_file` prozkoumej:
        1. `_quarto.yml` – struktura, navigace, globální nastavení.
        2. `hag_custom.scss` – barvy, proměnné, vlastní třídy, callouty.
        3. `{sample_chapter}` – ukázka stávajícího textu a stylu.

        Napiš PRÁVĚ tyto sekce, s přesně těmito nadpisy a v tomto pořadí:

        ## 1. Celkový styl
        Vzdušný styl, krátké odstavce, bezpatkové písmo, hierarchie H2/H3.
        Kniha se jmenuje „pohledem geometra“: každý pojem se vysvětluje i geometricky
        (těžiště, vzdálenost, projekce, plocha, úhel …), viz vzor houpačky s těžištěm.

        ## 2. Dvojjazyčnost
        Příprava pro přepínač CS/EN, konzistentní struktura v obou jazycích.

        ## 3. Dark / Light mode
        Fakta: `_quarto.yml` definuje světlé i tmavé téma, ale obě zatím používají stejný
        základ (cosmo + hag_custom.scss), takže tmavý režim zatím není skutečně tmavý.
        Právě se ladí jen světlý režim, tmavý přijde později.
        Popiš, jak psát divy a OJS grafy, aby fungovaly na světlém i tmavém pozadí
        (barvy z proměnných motivu, ne napevno).
        Barvy projektu jsou paleta JHRules ($jh-* v `hag_custom.scss`, CSS proměnné `--jh-*`).
        V OJS se berou z modulu `assets/jhrules.js` (`import {{C}} from "../assets/jhrules.js"`, cesta relativní k souboru kapitoly).
        Konkrétní hex hodnoty NEUVÁDĚJ (jsou v sekci 5, kterou doplní program).

        ## 4. Responsive design
        Pravidla pro OJS vizualizace na mobilech (šířka z vestavěné proměnné `width`,
        čitelné písmo, ovládací prvky vhodné pro dotyk).

        ## 7. Callout třídy
        Jak používat .callout-note, .callout-tip, .callout-warning v kontextu projektu.
        Nezmiňuj konkrétní hex barvy ani jména SCSS proměnných palety (paletu popisuje sekce 5).

        Sekce 5 (barvy) a 6 (struktura kapitoly) NEPIŠ – doplní je program.

        Závazné jednotné konvence (řiď se jimi, i když se ve stávajících kapitolách liší):
        - Nadpisy: H1 název kapitoly, H2 sekce, H3 podsekce. H4 a hlubší se nepoužívají.
        - Titulek calloutu i záložky se píše jako nadpis druhé úrovně (`## Titulek`) na prvním
          řádku uvnitř calloutu, shodně se šablonou v sekci 6. Titulky jsou bez emoji.
        - Nové soubory kapitol se jmenují ASCII kebab-case bez diakritiky a mezer
          (např. `06-spojita-rozdeleni.qmd`); starší názvy se přejmenují později.

        Formát výstupu:
        - Začni přímo nadpisem `## 1. Celkový styl`. Žádná úvodní věta, žádný obalující kódový blok.
        - Pokud uvnitř ukázky potřebuješ kódový blok (např. ```{{ojs}}), dej vnější ukázku
          do ohrady ze ČTYŘ zpětných apostrofů (````markdown … ````).
        - Projekt se jmenuje výhradně „{project_name}“.
        """


def content_description(inputs: dict) -> str:
    """Zadání pro autora textu. Strukturu kapitoly nepřikládá znovu: je v sekci 6 style guide,
    který agent dostane jako součást úkolu (viz chapter.py)."""
    areas = inputs.get("aplikacni_oblasti", DEFAULT_APPLICATION_AREAS)
    return f"""
        Napiš kompletní textový obsah kapitoly: **{inputs['tema']}**.
        Kapitola bude po kontrole zařazena jako `{inputs['vystupni_soubor']}`.

        OBSAH KAPITOLY:

        Hlavní témata (rozděl do nejvýše {MAX_SECTIONS} sekcí, každá = 1 pojem):
        {inputs['klicove_pojmy']}

        Zaměření příkladů:
        {inputs['zamereni_uloh']}

        Nástroje pro kódové bloky:
        {inputs['nastroje']}

        PRAVIDLA, která NESMÍŠ porušit:
        - Dodrž přesně strukturu kapitoly ze sekce 6 style guide (nahoře v zadání).
        - Začni přímo nadpisem první úrovně `# Název kapitoly` (bez YAML hlavičky a bez úvodní věty).
        - Hned pod nadpisem je chytlavý motivační odstavec (3–5 vět) o reálném problému z praxe,
          který bez tohoto tématu neumíme vyřešit. Odpovídá na otázku: „K čemu mi to v životě bude?".
        - Nejvýše {MAX_SECTIONS} sekcí. Pokud je pojmů více, spoj příbuzné do jedné sekce.
        - KAŽDÁ sekce má geometrický pohled (těžiště, vzdálenost, projekce, plocha, úhel …),
          nebo větu s odůvodněnou výjimkou, přesně jak určuje šablona.
        - OJS bloky vlož jako placeholder přesně podle šablony (`// OJS_PLACEHOLDER_SEKCE_N`,
          N = pořadí sekce 1, 2, 3 …). ojs_agent je doplní v dalším kroku.
        - Aplikační úlohy ({APPLICATION_TASKS}), oblasti: {areas}.
        - Závěr je jen tabulka pojmů.

        ČÍSLA (nejčastější zdroj chyb, buď pečlivý):
        - VŠECHNY číselné výsledky (školský příklad, self-testy, aplikační úlohy, čísla v textu)
          spočítej nástrojem `calc` (krátký Python; numpy jako `np`, scipy.stats jako `stats`;
          výsledky vypiš příkazem print()). Nikdy je nepočítej z hlavy ani je neodhaduj.
        - Do kapitoly piš hodnoty přesně podle výstupu nástroje. Zaokrouhluj až při zápisu,
          na rozumný počet míst, s desetinnou čárkou.
        - Číslo, které vychází z dat zobrazených v grafu sekce, nepiš ručně, aby text nemohl
          nesouhlasit s grafem. Napiš inline výraz, např. `${{mean1.toFixed(2).replace(".", ",")}}`.
          Název proměnné je anglický, ASCII a končí číslem sekce (`mean1`, `sd2` …); graf té sekce
          ji definuje. Používej střídmě, jen pro čísla z dat grafu. Matematiku v `$…$` tím nerozbiješ.
        """


def ojs_examples() -> str:
    """Vzorové OJS buňky (docs_for_agents/ojs_vzory.qmd) bez YAML hlavičky."""
    text = project_path(OJS_EXAMPLES_PATH).read_text(encoding="utf-8")
    return re.sub(r"\A---\n.*?\n---\n", "", text, count=1, flags=re.S).strip()


def ojs_description(inputs: dict, numbers: list[int], inline_names: list[str] | None = None) -> str:
    names = ", ".join(inline_names) if inline_names else "žádné"
    return f"""
        Pro kapitolu **{inputs['tema']}** napiš OJS (Observable JS) vizualizace do míst označených
        `// OJS_PLACEHOLDER_SEKCE_N`. Sekce s grafem jsou: {numbers}.
        Text kapitoly a style guide jsou v zadání výše.

        PROMĚNNÉ, KTERÉ TEXT POUŽÍVÁ V INLINE VÝRAZECH `${{…}}` (musíš je definovat přesně pod
        těmito názvy): {names}
        Definuj každou v kódu sekce, ke které se text vztahuje, jako `name = výraz` a počítej ji
        z dat grafu (např. `mean1 = d3.mean(data1)`). Text pak ukazuje stejné číslo jako graf.

        Požadavky na každou vizualizaci:
        - Ilustruje PRÁVĚ vysvětlený pojem v dané sekci a ukazuje její GEOMETRICKÝ POHLED
          (těžiště, vzdálenost, plocha …). Žádná obecná grafika.
        - Obsahuje interaktivní prvek: slider pro parametr nebo dropdown pro volbu.
        - Každá vizualizace jiná – nerecykluj stejný kód.

        PRAVIDLA OJS, která NESMÍŠ porušit (všechny buňky kapitoly sdílejí jeden globální prostor):
        - Proměnné se definují na začátku řádku jako `x = …`, `viewof x = …` nebo `function f() {{…}}`.
          `const` a `let` jen uvnitř bloku `{{ … }}`.
        - Názvy definované na začátku řádku musí být unikátní v CELÉ kapitole. Přidej příponu
          podle sekce (`n1`, `chart1`, `n2`, `chart2` …), vzory níže to ukazují.
        - `import {{C, gradient, plotStyle}} from "../assets/jhrules.js"` patří POUZE do kódu sekce 1.
          Do ostatních sekcí import nedávej (C, gradient i plotStyle jsou tam už definované).
          Jiné importy nepoužívej. `Inputs`, `Plot` i `d3` jsou dostupné bez importu.
        - Barvy VÝHRADNĚ z objektu `C` (žádné hex ani pojmenované barvy). Akcent (`C.accent`)
          nejvýše na JEDEN prvek grafu, hlavní data `C.primary`, kontext `C.context` / `C.contextLight`.
        - Šířka grafu je vestavěná proměnná `width` (`Plot.plot({{width, …}})`), nikdy pevné číslo.
          Výšku odvoď rozumně (cca 250 px, u úzkých grafů méně). Použij `style: plotStyle`.
        - Bez horní a pravé osy, mřížka jen vodorovná pro čtení hodnot z osy y (`y: {{grid: true}}`),
          bez rámečku legendy, raději přímé popisky.
        - Popisky os česky a krátké. Ovládací prvky mají krátký `label`.

        VZOROVÉ BUŇKY (techniku převezmi, téma ne; všechny jsou z jedné stránky,
        proto mají různé přípony názvů):
        {ojs_examples()}

        FORMÁT VÝSTUPU – pouze jeden JSON objekt, žádný jiný text, žádný obalující kódový blok:
        {{"1": "<celý OJS kód sekce 1>", "2": "<celý OJS kód sekce 2>", …}}
        Klíče jsou čísla sekcí {numbers}, hodnoty jsou řetězce s kódem (nový řádek jako \\n).
        Kód nezačíná ```{{ojs}} ani nekončí ```: vkládá se do bloku automaticky.
        """


def review_description(inputs: dict, findings: list[str]) -> str:
    findings_text = "\n".join(f"- {f}" for f in findings) if findings else "- žádné"
    return f"""
        Zkontroluj a oprav finální verzi kapitoly **{inputs['tema']}** (text je v zadání výše).

        AUTOMATICKY NALEZENÉ PROBLÉMY (oprav je):
        {findings_text}

        Checklist – ověř každý bod:

        {review_checklist()}

        ČÍSLA:
        - Přepočítej KAŽDÝ číselný výsledek v kapitole (školské příklady, self-testy, aplikační
          úlohy, čísla v textu) nezávisle nástrojem `calc`. Z hlavy nepočítej.
        - Nesouhlasí-li hodnota, oprav ji a zapiš do REVIEW NOTES původní i opravenou hodnotu.
        - Inline výrazy `${{…}}` v textu musí odkazovat na proměnné, které OJS buňky definují.

        PRAVIDLA ÚPRAV:
        - OJS bloky nepřepisuj, pokud nejsou prokazatelně chybné; nepřidávej ani neodebírej sekce.
        - Text nezkracuj.

        FORMÁT VÝSTUPU:
        1. Nejdřív CELÁ opravená kapitola (čisté Quarto Markdown, bez obalujícího kódového bloku,
           bez jakýchkoli poznámek v textu).
        2. Pak samostatný řádek přesně `{REVIEW_MARKER}` a pod ním seznam provedených oprav.
        """
