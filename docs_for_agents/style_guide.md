<!--
  GENEROVÁNO automaticky (crew_agents.py, generate_style_guide). Needitovat ručně.
  Sekce 5 a 6 vkládá Python (crew/style_guide.py), ostatní píše LLM.
  Datum: 2026-11-07
  Zdroje (sha256):
    _quarto.yml: 9da063e7ec705f7d1ef052b5b3dab668cfda562d91a416f47e153745349cfcd7
    hag_custom.scss: 94badb07f51809d0ca3ac61c377873c19a6003abd37d00c90abe0c1214cc4a13
-->

# Style Guide: Statistika pohledem geometra

## 1. Celkový styl

Učebnice **Statistika pohledem geometra** má vzdušný, pracovní a vizuální styl. Čtenář má pojmy nejdřív vidět a hrát si s nimi. Vzorce a odvození přicházejí až potom.

### Písmo a vzhled

- Základem je motiv Bootswatch **cosmo**. Ten používá bezpatkové písmo.
- `hag_custom.scss` nepřepisuje rodinu písma. Autoři v kapitolách nenastavují vlastní `font-family`, ani v HTML, ani v CSS, ani v OJS.
- Základní velikost je `$font-size-base: 1rem`. Nadpisy mají `$headings-font-weight: 600`.
- Nadpisy H1, H2 a H3 jsou v primární modré (`$primary`, `#0085CC`) a mají vlevo 4px modrý pruh. Pruh a barvu nepřepisujeme lokálními styly.

### Vzdušnost a odstavce

- Odstavec má 2 až 5 vět a vyjadřuje jednu myšlenku.
- Delší výklad dělíme otázkou, příkladem, vizualizací nebo calloutem. Dlouhé „zdi textu“ se nepíší.
- Klíčový pojem se při prvním výskytu zvýrazní tučně (`**průměr**`). Anglický ekvivalent se uvede kurzívou v závorce nebo za čárkou, např. `***mean absolute deviance, MAD***` nebo `*sd (standard deviation)*`.
- Důležité upozornění v řádku označíme třídou `.highlight-warning`. Důležitý pojem v řádku označíme třídou `.highlight-key` nebo `.highlight-term`. Zvýraznění nepřehánějte, stačí 1 až 2 na obrazovku.
- Vzorce uvnitř textu píšeme jako `$\bar{x}$`. Klíčové vzorce dáváme na samostatný řádek jako `$$ … $$`. Víceřádková odvození píšeme v prostředí `align`.

### Hierarchie nadpisů

- **H1** je jen jeden na kapitolu, a to její název (např. `# Momentové statistiky`).
- **H2** jsou hlavní části kapitoly, např. „Momentová míra polohy“ nebo „Momentové míry variability“.
- **H3** jsou podčásti uvnitř H2, např. „Šikmost“ nebo „Špičatost“.
- H4 a hlubší úrovně nepoužíváme. Pokud je potřebujete, rozdělte text jinak nebo použijte callout.
- Nadpisy začínají velkým písmenem (i H3, např. „Šikmost“, ne „šikmost“). Jsou krátké, věcné a bez tečky na konci.
- Nečíslovanou část označíme `{.unnumbered}`, jako např. „Klíčové poznatky“ na konci kapitoly.

### Jazyk a jednotný pravopis

- Píšeme česky (`lang: cs`), s vykáním nebo s neutrálním „my“ („Pojďme se podívat…“). Styl držíme jednotný v celé knize.
- Před odevzdáním zkontrolujte překlepy a diakritiku. Ve stávajícím textu se občas vyskytují, např. „proměné“ nebo „viualizace“. Do nových kapitol je nepřenášejte.
- Název projektu je vždy **Statistika pohledem geometra**. Žádné zkratky ani varianty.

### Vizualizace jako součást výkladu

- Každý nový pojem, pokud to jde, doprovází obrázek nebo interaktivní OJS graf. Graf má popisky os česky a v kódu se označuje `//| echo: false`.
- Důležité grafy mají `//| label: fig-…` a popisek pod obrázkem. Ten patří do fenced divu `::: {#fig-…}` jako poslední odstavec.
- Technická pravidla pro vzhled grafů najdete v sekcích 3 a 4.

## 2. Dvojjazyčnost

Kniha je zatím česky (`lang: cs` v `_quarto.yml`). Přepínač CS/EN zatím neexistuje. Nové kapitoly se ale musí psát tak, aby se anglická verze dala doplnit bez přestavby kapitoly.

### Zásady

- Česká a anglická verze mají **stejnou strukturu**. Mají stejný počet a pořadí nadpisů H2/H3, stejné obrázky, stejné callouty a stejné vzorce.
- Texty nemají být ve dvou verzích odlišně dlouhé ani odlišně členěné. Pokud do jedné verze přidáte odstavec nebo callout, doplňte ho i do druhé.
- Matematická notace je v obou jazycích stejná (`\bar{x}`, `sd`, `var`, `skew`, `kurt`). Většina zkratek je už anglická, takže se nemusí překládat.
- Při prvním výskytu uvádějte české pojmy společně s anglickým ekvivalentem, např. `**směrodatná odchylka** (*standard deviation, sd*)`. Překladový slovník pojmů tím vzniká přímo v textu.
- Identifikátory (`#sec-…`, `#fig-…`, `label:`) píšeme bez diakritiky a bez mezer, jazykově neutrálně, např. `#sec-momenty-polohy` nebo `fig-teziste-vizualizace`. Odkazy tak fungují v obou verzích.
- Nové soubory pojmenovávejte bez diakritiky a bez mezer, např. `06_nazev_kapitoly.qmd`. Starší názvy s mezerami a diakritikou se kvůli přepínači zatím nepřejmenovávají.

### Příprava textů v OJS grafech

Všechny popisky v grafech (osy, legendy, tlačítka, `Inputs`) patří do jednoho slovníku na začátku buňky. V kódu pak nejsou žádné „volné“ české řetězce.

````markdown
```{ojs}
//| echo: false
lang = "cs"   // později bude hodnota z přepínače CS/EN

t = ({
  cs: { x: "Hodnota (poloha na páce) →", mean: "Těžiště (průměr)", n: "Počet bins" },
  en: { x: "Value (position on the lever) →", mean: "Centre of mass (mean)", n: "Number of bins" }
})[lang]

viewof binCount = Inputs.range([2, 200], {value: 20, step: 1, label: t.n})
```
````

### Příprava textu kapitoly

Pro dlouhé pasáže připravujeme obsah do párových bloků. Každý blok má stejnou vnitřní strukturu:

````markdown
::: {.lang-cs}
## Momentová míra polohy

Slovo **moment** pochází z fyziky, kde popisuje situaci na páce.
:::

::: {.lang-en}
## Moment-based measure of location

The word **moment** comes from physics, where it describes a lever.
:::
````

Třídy `.lang-cs` a `.lang-en` zatím nemají žádné pravidlo ve `hag_custom.scss`. Až se přepínač zavede, určí podle nich, co se zobrazí. Do té doby se vyplňuje jen česká verze. Anglický blok může zůstat prázdný nebo označený `TODO`, ale musí být připravený.

## 3. Dark / Light mode

### Současný stav

`_quarto.yml` definuje světlé i tmavé téma:

```yaml
theme:
  light: [cosmo, hag_custom.scss]
  dark:  [cosmo, hag_custom.scss]
```

Obě témata používají stejný základ (`cosmo` a `hag_custom.scss`). Tmavý režim proto **zatím není skutečně tmavý**. Přepínač může existovat, ale paleta se téměř nezmění. Nové kapitoly se musí psát tak, aby fungovaly po doplnění skutečného tmavého motivu bez přepisování.

### Základní pravidlo

**Žádné napevno zadané barvy pozadí a textu.** Barvy se mají brát z proměnných motivu (Bootstrap CSS proměnné `--bs-*`, případně `currentColor`). Žádná z nich se při přepnutí režimu nemění na tvrdou hodnotu, vše se přepočítá samo.

Některé stávající prvky tuto zásadu porušují. Například `.definition-box` má pevné `background-color: $light` a `.callout-note` má `background-color: $light !important`. Tmavý režim se z toho po aktivaci musí opravit v SCSS, ne v kapitolách. Autoři kapitol tedy používají tyto třídy, ale nepřidávají k nim vlastní barvy.

### Zásady pro HTML a `div`

- Používejte třídy z `hag_custom.scss` (`.definition-box`, `.example-box`, `.highlight-key`, callouty), ne inline styly.
- Nepoužívejte `style="color: black"`, `style="background: #fff"`, `style="background: white"` ani podobné.
- Pokud potřebujete vlastní barvu, píšete ji jako proměnnou nebo poloprůhledně: `style="border-left: 4px solid var(--bs-primary)"` nebo `background: rgba(0, 133, 204, 0.1)`. Poloprůhledné podbarvení funguje na světlém i tmavém pozadí.
- Barvy textu nechte dědit z motivu. Barvu měňte jen u zvýraznění (`.highlight-*`).

### Zásady pro OJS grafy (Observable Plot)

Plot dědí barvu textu z okolí a pozadí nechává průhledné. Dovolí-li to kód, využijte toho.

- Osy, popisky, rastr a pomocné čáry: `currentColor` s nižší průhledností (`strokeOpacity`, `fillOpacity`), ne `"black"`, `"#333"` ani `"#ccc"`.
- Hlavní datové barvy a barvy zvýraznění: proměnné motivu, např. `"var(--bs-primary)"`. Barvy odvozujte z palety projektu podle sekce 5 (barvy), ne z náhodných názvů barev.
- Texty v grafu (`Plot.text`): `fill: "currentColor"` místo `"black"`. Nepoužívejte `"white"`. Kontrastní obrys bodu má použít barvu pozadí: `stroke: "var(--bs-body-bg)"`.
- Světlé výplně (`"#f0f0f0"`) nahraďte průhlednou výplní (`fill: "currentColor", fillOpacity: 0.1`).
- Plot nastavte tak, aby pozadí grafu nebylo bílé: `style: { background: "transparent" }`.
- Barvy, které jsou nyní v kapitolách natvrdo (`steelblue`, `darkred`, `black`, `#666`), ve stávajících kapitolách postupně nahradíme. V nových je nepoužívejte.

````markdown
```{ojs}
//| echo: false
Plot.plot({
  width: width,
  style: { background: "transparent", fontSize: "14px" },
  marks: [
    Plot.ruleY([0], { stroke: "currentColor", strokeOpacity: 0.5 }),
    Plot.dot(data, {
      x: "x", y: "y",
      fill: "var(--bs-primary)",
      stroke: "var(--bs-body-bg)",
      r: 5
    }),
    Plot.text(data, {
      x: "x", y: "y", text: "label",
      fill: "currentColor", dy: 16
    })
  ]
})
```
````

### Kontrola před odevzdáním

- Zkontrolujte, že graf i `div` jsou čitelné na světlém pozadí. Po zavedení skutečného tmavého motivu je zkontrolujte i na tmavém.
- Hledejte v kódu slova `black`, `white`, `#fff`, `#000` a hexadecimální šedé tóny. Všechna by měla zmizet.
- Obrázky exportované z jiných nástrojů (PNG, SVG) mají mít průhledné pozadí. Jinak se na tmavém pozadí objeví bílý obdélník.

## 4. Responsive design

Kniha se čte i na mobilu. Pravidla níže platí pro každou OJS vizualizaci.

### Šířka z proměnné `width`

OJS poskytuje vestavěnou reaktivní proměnnou `width`, tedy šířku dostupnou pro buňku. Používejte ji vždy místo pevné šířky.

- Pevná šířka (`width: 500`, `width: 600`) se v nových kapitolách **nepoužívá**. Na úzkém displeji způsobí vodorovné posouvání nebo ořez.
- Výška se odvozuje od šířky, aby se poměr stran udržel. Horní mez zabrání příliš velkým grafům na širokých monitorech.
- Čtvercové grafy (např. vektory v rovině) mají `height` rovnou šířce: `height: Math.min(width, 500)`.
- Šířku nezvětšujte nad rozumnou mez.
- Příliš vysoké grafy (např. `height: 800`) se na mobilu nevejdou na obrazovku. Výšku odvoďte od šířky (`width * 0.9`) a omezte ji.

````markdown
```{ojs}
//| echo: false
w = Math.min(width, 640)
h = Math.max(240, Math.min(w * 0.7, 480))
isNarrow = width < 480

Plot.plot({
  width: w,
  height: h,
  marginLeft: isNarrow ? 40 : 60,
  style: { background: "transparent", fontSize: isNarrow ? "12px" : "14px" },
  x: { label: isNarrow ? "x" : "Hodnota x" },
  marks: [ /* … */ ]
})
```
````

### Čitelné písmo

- Minimální velikost písma v grafu je **12 px** na mobilu a 14 px na počítači. Nastavuje se přes `style: { fontSize: … }`.
- Popisky os krátíme na úzkém displeji, viz `isNarrow` výše.
- Dlouhé texty legendy neukládejte jako několik `Plot.text` s pevnými souřadnicemi v rohu grafu, protože se na úzkém displeji překrývají s daty. Používejte `frameAnchor` a krátké texty. Delší legendy raději napište pod graf jako odstavec nebo tabulku.
- Pokud text v grafu zůstane příliš dlouhý, přesuňte jeho obsah do textu pod obrázkem, který se zalamuje sám.
- Popisky bodů a čar se nesmí překrývat. U gustého grafu popisujte jen klíčové body.

### Ovládací prvky vhodné pro dotyk

- Ovládací prvky (`Inputs.range`, `Inputs.select`, `Inputs.radio`) musí být snadno ovladatelné prstem. Cílová plocha by měla mít zhruba 44 × 44 px.
- Posuvník má mít rozumný krok (`step`). Celých čísel s krokem 1 na rozsahu 0 až 10 se na dotyku trefuje dobře, ale rozsah 2 až 200 s krokem 1 je pro prst nepřesný. U takových ovladačů zvažte větší krok.
- Dáváme přednost `Inputs.select` nebo `Inputs.radio` s několika málo volbami před textovým zadáváním hodnot.
- Ovládací prvky umístěte nad graf a nechte je pod sebou. Graf se tak při změně hodnoty neposouvá pod prstem.
- Popisek každého prvku (`label`) je krátký. Na úzkém displeji se jinak zalomí a prvek se zmenší.
- Nespoléhejte na interakce jen přes najetí myší (hover). Na mobilu nefungují. Informace musí být dostupná i bez hoveru, např. jako popisek v grafu nebo jako text pod ním.
- Ovládací prvky držte blízko grafu, který ovládají. Při posunu na mobilu musí být vidět obojí.

### Kontrola před odevzdáním

- Otevřete kapitolu v úzkém okně prohlížeče (cca 360 px). Nic se nesmí ořezávat, překrývat ani posouvat do stran.
- Zkontrolujte čitelnost popisků i legendy.
- Zkontrolujte, že všechny ovladače lze ovládat prstem a že celá kapitola funguje i bez myši.
- Vzorce `$$ … $$`, které se na úzkém displeji nevejdou, rozdělte na více řádků pomocí prostředí `align`.

## 5. Barevné schéma pro OJS

Hodnoty jsou automaticky převzaté z `hag_custom.scss` (sekce `scss:defaults`).
Dočasné řešení: později je nahradí sdílený modul, který čte barvy přímo z CSS
(viz `docs_for_agents/zadani_revize.md`, B2 a B3).

```js
COLORS = ({
  primary:     "#0085CC",   // $primary
  secondary:   "#666666",   // $secondary
  grayLight:   "#B0B0B0",   // $gray-light
  light:       "#F8F9FA",   // $light
  dark:        "#1A1A1A",   // $dark
  warning:     "#8B0512",   // $warning
  warningDark: "#5A030C",   // $warning-dark
})
```

## 6. Struktura kapitoly

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

## 7. Callout třídy

Callouty používáme střídmě. Jeden callout by měl nést jednu myšlenku a text by měl být krátký. V nastavení projektu (`hag_custom.scss`) mají callouty tyto vlastnosti:

- **Ikony jsou skryté.** Význam callout musí být zřejmý z titulku a z barvy levého pruhu, ne z ikony.
- Callout má vlevo 5px pruh. Barva pruhu závisí na typu.
- Varianty vzhledu `simple` a `minimal` mají průhledné pozadí. U `minimal` se navíc skrývá nadpis.
- Barvy pruhů a pozadí callout jsou součástí barevné palety (viz sekce 5). Autoři je v kapitolách nepřepisují. V SCSS jsou navíc dvě nesourodé definice barvy pruhu pro `.callout-note`, proto na jeho přesný odstín nespoléhejte.

### `.callout-note`: poznámka, odvození, doplněk

Pro vedlejší informace, které nejsou nutné k pochopení hlavní linie, a pro odvození. V projektu se používá ve dvou podobách:

- **Rozbalovací** (`collapse="true"`) pro delší odvození a pro náročnější látku pro zájemce, např. „Odvození, že $\sum e_i=0$“ nebo „Směrodatná odchylka lineárně algebraicky“.
- **Běžná (stále rozbalená)** pro krátký komentář nebo interpretaci, např. věta o tom, co znamená nulový součet odchylek.

````markdown
::: {.callout-note collapse="true"}
# Odvození, že $\sum e_i=0$

\begin{align}
  \sum(x_i-\bar{x}) = \sum x_i - n\cdot\bar{x} = 0
\end{align}
:::

:::{.callout-note}
Nulový součet odchylek ukazuje, že průměr je opravdu těžiště.
:::
````

Titulek píšeme jako nadpis `# …` na prvním řádku uvnitř callout. Je stručný a vystihuje obsah.

### `.callout-tip`: tip, intuice, praktická rada

Pro pomůcku, jak si pojem snáze zapamatovat nebo jak s ním pracovat v praxi. Dále pro nápad „zkuste si to“ u interaktivního grafu, nebo pro geometrickou intuici. Tip nesmí obsahovat informaci nezbytnou pro pochopení látky, protože čtenář ho může přeskočit. Používá se v modré (primární) barvě.

````markdown
::: {.callout-tip}
# Zkuste si to
Posuňte jezdce „Respondent 1“ a sledujte, jak se mění vektor odchylek.
:::
````

### `.callout-warning`: varování, častá chyba, výjimka

Pro situace, kdy hrozí chybná interpretace nebo chyba ve výpočtu. Například: „Součet odchylek je vždy nula, proto jej nelze použít jako míru variability.“ Nebo: rozdíl mezi dělením `n` a `n−1`. Warning používá tmavě červený pruh a lehce červené pozadí. Používá se jen pro skutečná upozornění, ne pro běžné důležité věci. Pro ty je `.highlight-key`.

````markdown
::: {.callout-warning}
# Pozor na dělení
V této kapitole dělíme rozptyl číslem $n$. Statistický software často dělí číslem $n-1$.
:::
````

### Obecná pravidla

- Typ callout vybíráme podle role: `note` je doplňující vysvětlení, `tip` je pomůcka, `warning` je past.
- Používáme pouze tyto tři typy. Typy `.callout-important` a `.callout-caution` v projektu nejsou nastylované, proto je nepoužíváme.
- Nevnořujeme callouty do sebe.
- Do callout nedáváme velké interaktivní grafy. Pokud je graf součástí rozbalovacího odvození, zkontrolujte ho na mobilu (viz sekce 4).
- Definice patří do `.definition-box` a příklady do `.example-box`. Callouty se k tomu nepoužívají.
- Callouty nenahrazují běžný text. Maximálně 1 až 2 callouty na obrazovku.
- Barvy do callout nepřidáváme ručně. Pozadí a pruh řeší `hag_custom.scss` (viz sekce 3 o dark/light módu).
