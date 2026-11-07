# =============================================================================
# ŠABLONA STRUKTURY KAPITOLY  (Cognitive Load Theory)
# Toto je pevná kostra – content agent ji VŽDY dodržuje.
# Mění se pouze obsah (téma, pojmy, příklady), nikdy struktura.
# =============================================================================

CHAPTER_STRUCTURE = """
**ZÁVAZNÁ STRUKTURA KAŽDÉ KAPITOLY (Cognitive Load Theory)**

> POKYN – začátek kapitoly:
> Hned pod hlavní nadpis kapitoly (H1) vlož motivační odstavec.
> Tento odstavec nastíní reálný, praktický problém z oblasti ekonomiky,
> managementu nebo medicíny, který bez znalosti této kapitoly nelze efektivně vyřešit.
> Odstavec musí studenta vtáhnout do děje a ukázat mu, PROČ se dané téma učí.
> Rozsah: 3–5 vět. Žádné klišé typu "V této kapitole se podíváme...".

Šablony ve vnější ohradě ze čtyř zpětných apostrofů (````) se kopírují BEZ této vnější ohrady.

Kapitola se skládá z maximálně 5 sekcí + závěrečného bloku.

Každá sekce pokrývá JEDEN koncept. Kratší je lepší.

---

### SEKCE  (opakuj max. 5×)

````markdown
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
````

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

````markdown
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
````

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
