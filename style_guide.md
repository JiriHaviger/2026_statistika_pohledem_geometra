```js
const COLORS = {
  primary: "#0085CC",
  secondary: "#666666",
  grayLight: "#B0B0B0",
  light: "#F8F9FA",
  dark: "#1A1A1A",
  warning: "#8b0512",
  warningDark: "#6f040f" // Ztmaveno o 10% z $warning
}
``````
## N. Název sekce ← jeden pojem / jeden krok

[TEORIE – max. 3 krátké odstavce]
Vzdušný text. Každý odstavec = jedna myšlenka. Bez zbytečných úvodů.
Geometrická nebo intuitivní interpretace pojmu.

[INTERAKTIVNÍ GRAFIKA – povinná, právě 1 na sekci]
``````

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
```Následuje závazný Style Guide pro projekt Havi Notes.

---

## 1. Celkový styl

Projekt Havi Notes se drží vzdušného a přehledného stylu, zaměřeného na snadnou čitelnost a efektivní předávání informací.

*   **Odstavce**: Využívejte krátké odstavce. Každý odstavec by měl ideálně prezentovat jednu myšlenku nebo koncept. Vyhněte se zbytečným úvodům a dlouhým souvětím.
*   **Písmo**: Celý projekt používá bezpatkové písmo pro moderní a čistý vzhled.
*   **Hierarchie nadpisů**: Pro strukturování obsahu se používá jasná hierarchie nadpisů `H2` a `H3`.
    *   `H1` je vyhrazen pro název knihy/kapitoly.
    *   `H2` značí hlavní sekce kapitoly.
    *   `H3` se používá pro podsekce v rámci H2.
*   **Tučný text**: Používejte s rozvahou pro zdůraznění klíčových pojmů.
*   **Vzdušnost**: Udržujte dostatečné mezery mezi odstavci, obrázky a kódem pro lepší vizuální oddělení a snížení kognitivní zátěže.

## 2. Dvojjazyčnost

Projekt je navržen s ohledem na budoucí podporu dvojjazyčnosti (Čeština/Angličtina).

*   **Jazyk projektu**: Primárním jazykem je čeština (`lang: cs` v `_quarto.yml`).
*   **Struktura**: Pro každou kapitolu zajistěte konzistentní strukturu a pořadí sekcí v obou jazykových verzích, pokud budou zavedeny. To usnadní budoucí implementaci přepínače jazyků.
*   **Texty**: Veškerý text by měl být připraven k snadnému překladu. Vyhněte se idiomatickým výrazům, které nemají přímý ekvivalent v angličtině, nebo je objasněte.

## 3. Dark / Light mode

Pro projekt je definováno světlé téma (`light: [cosmo, hag_custom.scss]`). Pro zajištění konzistence je nutné správně využívat definované CSS proměnné.

*   **Primární proměnné**:
    *   `$light` (`#F8F9FA`): Používat pro světlé pozadí prvků (např. `.callout-note`, `.definition-box`).
    *   `$dark` (`#1A1A1A`): Používat pro tmavý text (např. nadpisy v boxech, obecný text, pokud není definována jiná barva).
*   **OJS a Divy**: Při tvorbě vlastních `<div>` prvků nebo při definování barev v Observable JS (OJS) vizualizacích, které nejsou přímo řízeny CSS, používejte konkrétní hex hodnoty z bodu 5. Pro budoucí podporu dark mode v OJS je potřeba buď implementovat logiku uvnitř OJS, která reaguje na systémové nastavení uživatele, nebo dynamicky měnit barvy na základě kontextu z Quarto. Prozatím se držte hex hodnot.

## 4. Responsive design

OJS vizualizace musí být optimalizovány pro zobrazení na různých zařízeních, včetně mobilních telefonů.

*   **`max-width: 100%`**: Vždy zajistěte, aby šířka OJS grafiky nepřesáhla šířku rodičovského kontejneru. Místo pevného `width` v pixelech v OJS bloku preferujte `width: auto` nebo `max-width: 100%` v rodičovském CSS, pokud je to možné. Pokud je nutné specifikovat šířku přímo v OJS, zvažte `responsive: true` pro Observable Plot (pokud je k dispozici) nebo použití dynamického `width` na základě `window.innerWidth`.
*   **`viewBox` pro SVG**: Pro komplexní SVG grafiky (které generuje i Observable Plot) je doporučeno správně nastavit atribut `viewBox`. To umožní SVG se škálovat bez deformace obsahu. Quarto a Observable Plot se o toto většinou postarají automaticky, ale při ručních úpravách na to myslete.
*   **Interaktivní prvky**: Slidery a dropdowny v OJS by měly být dostatečně velké a přehledné pro dotykové ovládání na mobilních zařízeních.
*   **Zjednodušení na mobilech**: Zvažte, zda některé složité vizualizace nemohou být pro mobilní zobrazení zjednodušeny nebo zda je nutné omezit množství zobrazovaných dat.

## 5. Barevné schéma pro OJS

Následující hex hodnoty z `hag_custom.scss` musí být používány jako konstanty v Observable JS vizualizacích pro zajištění konzistentního barevného schématu.



## 6. Struktura kapitoly

## ZÁVAZNÁ STRUKTURA KAŽDÉ KAPITOLY (Cognitive Load Theory)

Kapitola se skládá z maximálně 5 sekcí + závěrečného bloku.
Každá sekce pokrývá JEDEN koncept. Kratší je lepší.

---

### SEKCE (opakuj max. 5×)

{ojs}
// Observable JS vizualizace ilustrující právě vysvětlený pojem.
// Slider nebo dropdown pro interakci studenta.
// Barvy VÝHRADNĚ z CSS proměnných Style Guide.


---

### APLIKAČNÍ ÚLOHY (samostatný blok, JEDNOU za kapitolu, za všemi sekcemi)

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

### ZÁVĚR KAPITOLY (vždy poslední blok)

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

## 7. Callout třídy

Pro zvýraznění důležitých informací se používají Quarto callouty s vlastními styly definovanými v `hag_custom.scss`.

*   **`::: {.callout-note}`**:
    *   Používá se pro obecné poznámky, vysvětlení nebo dodatečné informace.
    *   Vizualně má levý okraj v barvě `$secondary` (`#666666`) a pozadí v barvě `$light` (`#F8F9FA`).
    *   Příklad použití:
        ```markdown
        ::: {.callout-note}
        Toto je důležitá poznámka.
        :::
        ```
*   **`::: {.callout-tip}`**:
    *   Určeno pro tipy, rady nebo užitečné triky.
    *   Vizualně má levý okraj v barvě `$primary` (`#0085CC`).
    *   Může být použit s atributem `collapse="true"` pro skládací obsah a `icon=false` pro odstranění výchozí ikony, jak je vidět v šabloně pro AI prompt.
    *   Příklad použití:
        ```markdown
        ::: {.callout-tip collapse="true" icon=false}
        ## 💬 Zeptej se AI
        Zde je tip pro práci s AI.
        :::
        ```
*   **`::: {.callout-warning}`**:
    *   Pro upozornění na potenciální problémy, chyby nebo důležité věci, které vyžadují pozornost.
    *   Vizualně má levý okraj v barvě `$warning-dark` (`#6f040f`) a lehce tónované pozadí (`rgba($warning-dark, 0.1)`).
    *   Příklad použití:
        ```markdown
        ::: {.callout-warning}
        Pozor na zaokrouhlování v tomto kroku.
        :::
        ```
*   **Atributy `collapse="true"` a `icon=false`**:
    *   `collapse="true"`: Umožňuje sbalit/rozbalit obsah calloutu.
    *   `icon=false`: Odstraní výchozí ikonu Quarto calloutu. V projektu jsou ikony potlačeny globálně v CSS pro konzistentní vzhled a nahrazeny případnými vlastními ikonami v nadpisu (např. 💬 nebo 🏭).
*   **Styly `callout-style-simple` a `callout-style-minimal`**: Tyto styly jsou definovány v `hag_custom.scss` pro další vizuální úpravy calloutů, jako je odstranění rámečků nebo skrytí nadpisu. Používejte je podle potřeby pro jemnější kontrolu vzhledu.