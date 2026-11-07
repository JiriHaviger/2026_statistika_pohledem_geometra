<!--
  GENEROVÁNO automaticky (python main.py style --force). Needitovat ručně.
  Sekce 5 a 6 vkládá Python (crew/style_guide.py), ostatní píše LLM.
  Datum: 2026-11-07
  Zdroje (sha256):
    _quarto.yml: 1457f484998342eebbbef5de095557d8ba870f9d92e10fbfb24e0ea27536c547
    hag_custom.scss: 8b90a1499bb82ed24e2931799dce01a337953fc38a25e9647d4889783698bfd4
    jhrules.py: 15818ee72f2047b6e6e56c82a6a3b70695696f34962597a48878566828d7e392
    assets/jhrules.js: fc6dfc072963a1cc5fcf8f74800f73bc8313ac557703e8c735672487ccda0fe0
-->

# Style Guide: Statistika pohledem geometra

## 1. Celkový styl

Kniha má být vzdušná a čtivá. Čtenář se k ní vrací při studiu a nečte ji vcelku.

### Text a odstavce

- Odstavec má 2 až 4 věty a jednu myšlenku. Delší odstavec rozdělte.
- Před vzorcem stojí věta, která říká, co bude vzorec vyjadřovat. Za vzorcem následuje slovní interpretace.
- Nové pojmy se při prvním výskytu zvýrazní tučně (`**průměr**`). Anglický ekvivalent se uvede v závorce kurzívou (`*standard deviation*`).
- Neodkazujte na „dřívější kapitolu“ bez odkazu. Používejte křížové odkazy Quarto (`@sec-...`, `@fig-...`).
- Pište česky, v prvním pořadí oslovujte čtenáře („podíváme se“, „zkusme“). Dbejte na pravopis a diakritiku. Před odevzdáním text zkontrolujte.

### Písmo a vzhled

- Celá kniha používá bezpatkové písmo (Arial/Helvetica, nastavené v `hag_custom.scss`). Písmo v kapitolách ani v grafech nepřepisujte.
- Barvy ani písmo nenastavujte inline (`style="..."`). Používejte připravené třídy: `.accent`, `.muted`, `.highlight`, `.highlight-key`, `.highlight-term`, `.highlight-warning`, `.definition-box`, `.example-box`.
- Zvýraznění používejte střídmě. Na jednom odstavci by mělo být nejvýše jedno místo označené `.accent` nebo `.highlight-warning`.
- Emoji se nepoužívají nikde: ani v nadpisech, ani v titulcích calloutů, ani v textu.
- Popisky obrázků a grafů (`figcaption`) styluje šablona. Pište je jako úplnou větu a vysvětlete, co čtenář v grafu vidí.

### Hierarchie nadpisů

- H1 je název kapitoly. Je právě jeden na soubor.
- H2 je sekce.
- H3 je podsekce.
- H4 a hlubší se nepoužívají. Potřebujete-li další úroveň, rozdělte sekci nebo použijte seznam či tučný lead-in.
- Nadpisy mají vlevo barevnou čáru, kterou přidává šablona. Neprošpikujte je proto značkami ani barvami.
- Nadpisy nečíslujte ručně.
- Názvy nadpisů mají být krátké a věcné („Momentová míra polohy“, ne „Úvahy o tom, co je to průměr“).

### Pohled geometra

Kniha se jmenuje „Statistika pohledem geometra“. Každý nový pojem proto vysvětlete i geometricky:

- jako těžiště nebo rovnováhu,
- jako vzdálenost,
- jako projekci,
- jako plochu,
- jako úhel.

Doporučená posloupnost je: intuice a obrázek, geometrický význam, vzorec, interaktivní vizualizace. Vzorec nepřichází jako první.

Vzorem je kapitola o momentových statistikách s houpačkou:

| Pojem | Geometrický obraz |
|:---|:---|
| průměr | těžiště: páku podepřenou v průměru udržíme v rovnováze |
| odchylka $e_i = x_i - \bar{x}$ | vzdálenost od bodu otáčení (rameno síly) |
| součet odchylek je nula | záporná a kladná strana jsou v rovnováze |
| průměr jako nejlepší jedno číslo | projekce vektoru dat na přímku daného jedničkovým vektorem |
| vektor odchylek | kolmice k této přímce (pravý úhel) |
| rozptyl a směrodatná odchylka | Pythagorova věta: $\|\mathbf{x}\|^2 = \|\bar{x}\mathbf{1}\|^2 + \|\mathbf{e}\|^2$ |
| šikmost a špičatost | tvar histogramu, váha vzdálených bodů |

Pravidla pro geometrické vysvětlení:

- Geometrický výklad je součástí hlavního textu. Hlubší nebo algebraické odvození dejte do sbaleného calloutu (`collapse="true"`), viz sekce 7.
- Obrázek má být v textu nejpozději u prvního vzorce. Nesmí být až na konci kapitoly.
- Pravý úhel, těžiště, projekci a podobné prvky v obrázku vždy popište slovy.
- Vždy uveďte, co je na obrázku **to jedno, na co se dívat** (jediný zvýrazněný prvek na obrázek). Ostatní prvky jsou kontext.

### Příklad rozvržení podsekce

````markdown
## Rozptyl jako čtverec vzdálenosti

Vektor dat rozložíme na dvě složky: průměr a odchylky. Jsou na sebe kolmé.

Díky pravému úhlu platí Pythagorova věta:

$$\|\mathbf{x}\|^2 = \|\bar{x}\mathbf{1}\|^2 + \|\mathbf{e}\|^2$$

Rozptyl je tedy čtverec délky vektoru odchylek, přepočtený na jedno pozorování.
````

## 2. Dvojjazyčnost

Kniha je dnes česky (`lang: cs` v `_quarto.yml`). Přepínač CS/EN zatím neexistuje. Nové kapitoly se ale píší tak, aby šly později snadno doplnit anglicky. Pravidla níže zajistí, že obě jazykové verze budou mít stejnou strukturu.

### Strukturální pravidla

- Anglická verze má stejnou kostru jako česká: stejný počet a pořadí sekcí H2/H3, stejné callouty, stejné obrázky.
- Identifikátory (`#sec-...`, `#fig-...`, `#tbl-...`, `label:` v OJS) jsou ASCII, anglicky nebo neutrálně, bez diakritiky a bez jazykové přípony. Odkaz `@fig-moments` tak funguje v obou verzích.
- Každý překládaný blok je v samostatném divu s jazykovou třídou: `.lang-cs` a `.lang-en`. Děje se tak na úrovni celých sekcí nebo bloků, nikdy uprostřed věty.
- Obě verze bloku mají stejné pořadí: nejdříve `.lang-cs`, pak `.lang-en`.
- Vzorce a symboly ($\bar{x}$, $\sigma^2$, $z_i$) jsou společné a překládá se pouze okolní text. Jde-li o zkratky (*sd*, *var*, *MAD*), vysvětlete je v obou jazycích.
- Při prvním výskytu pojmu uveďte český termín i anglický ekvivalent. Např.: **směrodatná odchylka** (*standard deviation*). Díky tomu je glosář přeložitelný.

### Příklad bloku

````markdown
## Momentová míra polohy {#sec-moment-location}

::: {.lang-cs}
**Průměr** je těžiště dat: páka podepřená v průměru je v rovnováze.
:::

::: {.lang-en}
The **mean** is the centre of mass of the data: a lever supported at the mean balances.
:::
````

### Texty v OJS grafech

- Popisky os, legendy a ovládacích prvků nepište přímo do kódu grafu. Soustřeďte je na začátek buňky do slovníku `T` s klíči `cs` a `en`.
- Jazyk čtěte z `document.documentElement.lang` s výchozí hodnotou `"cs"`.
- Čísla formátujte podle jazyka (`toLocaleString`). V češtině je desetinná čárka, v angličtině tečka.
- Ve slovníku musí mít všechny klíče obě verze. Chybějící překlad nesmí zůstat prázdný.

````markdown
```{ojs}
//| echo: false
lang = document.documentElement.lang || "cs"
T = ({
  cs: {x: "Hodnota (poloha na páce)", mean: "Těžiště (průměr)"},
  en: {x: "Value (position on the lever)", mean: "Centre of mass (mean)"}
})[lang]
fmt = (v) => v.toLocaleString(lang, {maximumFractionDigits: 1})
```
````

### Další pravidla

- Metadata kapitoly (title, popis) připravte v obou jazycích, až bude přepínač hotový.
- Vyhněte se slovním hříčkám a idiomům, které nejdou přeložit. Pište jednoduše.
- Nepoužívejte obrázky s vloženým textem. Popisky patří do `figcaption` nebo do OJS, aby je šlo přeložit.
- Tabulky mají v obou jazycích stejné sloupce.

## 3. Dark / Light mode

### Současný stav

`_quarto.yml` definuje světlé i tmavé téma. Obě ale používají stejný základ (cosmo + `hag_custom.scss`), takže tmavý režim zatím není skutečně tmavý. Právě se ladí jen světlý režim, tmavý přijde později.

Nové kapitoly se proto píší už teď tak, aby po zavedení tmavého tématu fungovaly bez přepisování. Rozhodující je jediné pravidlo: **barvy se berou z proměnných motivu, ne napevno.**

### Barvy v textu a divech

- Barvy projektu tvoří paleta JHRules. V SCSS jsou to proměnné `$jh-*` v `hag_custom.scss`, v CSS jsou dostupné jako proměnné `--jh-*`. Konkrétní hodnoty najdete v sekci 5.
- Do kapitol nikdy nepište hex kód, `rgb()` ani pojmenovanou barvu (`white`, `black`, `steelblue`, `darkred`, `red`, `#666`, `#ccc`).
- V HTML divech a OJS prvcích používejte `var(--jh-text)`, `var(--jh-bg)`, `var(--jh-primary)`, `var(--jh-context)` a další `--jh-*`. Pro prosté pozadí a text lze použít i proměnné Bootstrapu `var(--bs-body-bg)` a `var(--bs-body-color)`.
- Pozadí div nenastavujte bílé ani černé. Nechte ho průhledné nebo použijte `var(--jh-bg)`.
- Inline styl `style="color: ..."` se nepoužívá. Pro zvýraznění slouží třídy `.accent`, `.muted`, `.highlight-*`.
- Barvy mají pevné role:
  - **primary** je hlavní data a prvky,
  - **accent** je jediný prvek, na který se čtenář má dívat,
  - **context** jsou osy, popisky a vedlejší data,
  - **warning** je riziko a varování.
- Barva nikdy nenese informaci sama. Rozlišujte i tvarem, čárkováním, popiskem nebo polohou, aby graf zůstal čitelný i na jiném pozadí a pro barvoslepé čtenáře.

### Příklad divu

````markdown
::: {.my-note style="color: var(--jh-text); border-left: 4px solid var(--jh-primary);"}
Text, který se přizpůsobí motivu.
:::
````

Raději než inline styl přidejte do `hag_custom.scss` třídu a v ní používejte proměnné palety.

### Barvy v OJS grafech

- Paleta se do OJS načítá z modulu `assets/jhrules.js`. Modul čte CSS proměnné `--jh-*` a vystavuje je jako objekt `C`.
- Import patří do první `{ojs}` buňky kapitoly. Cesta je relativní k souboru kapitoly, např. z podsložky `02-statistika/` je to `../assets/jhrules.js`.
- Do `Plot.plot` přidejte `style: plotStyle`. Nastaví průhledné pozadí, barvu textu a písmo podle motivu.
- Do `fill`, `stroke` a `fill` textu dávejte jen hodnoty `C.*`.
- Okraj kolem bodů (dříve `stroke: "white"`) mějte v barvě pozadí: `C.bg`.
- Modul je skutečně spolehlivý jen tehdy, když barvy nekopírujete do vlastních konstant s hex hodnotou.
- Více kategorií nekreslete duhou. Použijte `gradient(n)` z téhož modulu (plynulý přechod odstínů).
- Pozor: `C` se čte při načtení stránky. Po zavedení tmavého tématu může být nutné stránku po přepnutí režimu znovu načíst. Do kapitol proto nepište vlastní detekci režimu.

````markdown
```{ojs}
//| echo: false
import {C, gradient, plotStyle} from "../assets/jhrules.js"

Plot.plot({
  style: plotStyle,
  width: width,
  marks: [
    Plot.ruleY([0], {stroke: C.context}),
    Plot.dot(data, {x: "x", y: "y", fill: C.primary, stroke: C.bg}),
    Plot.dot([highlight], {x: "x", y: "y", fill: C.accent, r: 8})
  ]
})
```
````

### Kontrolní seznam

- V kódu OJS ani v textu není žádný napevno zapsaný barevný kód.
- Pozadí grafů je průhledné (`plotStyle`).
- Text v grafu používá `C.text` nebo `C.context`, nikdy čistě černou ani bílou.
- Na obrázku je nejvýše jeden prvek v barvě `C.accent`.
- Obrázek se ověří ve světlém režimu. Tmavý režim se zkontroluje, až bude hotový.

## 4. Responsive design

Čtenáři otevírají učebnici i na telefonu. Každá OJS vizualizace proto musí být čitelná a ovladatelná na úzké obrazovce.

### Šířka a rozměry

- Šířka grafu vychází z vestavěné proměnné `width`. V `Plot.plot` použijte `width: width`.
- Nepoužívejte pevné šířky typu `width: 600` nebo `width: 500`. Na mobilu by graf přetekl nebo by se horizontálně posouval.
- Výšku odvoďte od šířky, aby se zachoval poměr stran. U čtvercových geometrických obrázků (vektory v rovině) volte `height: width`, ale s horním omezením, např. `Math.min(width, 500)`.
- Graf, který potřebuje velkou výšku, nechte na mobilu nižší. Nepoužívejte fixní `height: 800`.
- Dbejte na dostatečné okraje (`marginLeft`, `marginBottom`), aby se nepřekrývaly popisky os.
- Při úzké šířce snižte počet značek na ose (`ticks`), případně popisky zkraťte.

### Písmo a popisky

- Písmo v grafu má mít nejméně 12 px, což nastavuje `plotStyle`. Menší písmo nepoužívejte.
- Dlouhé popisky nepište jako `Plot.text` ve vnitřku grafu na pevné souřadnice. Na úzké šířce se překrývají.
- Legendu s výsledky umístěte do rohu pomocí `frameAnchor`, nebo ještě lépe pod graf jako běžný text či tabulku.
- Informace nesmí záviset jen na tooltipu nebo najetí myší. Na dotykovém zařízení neexistuje.
- Popis grafu (`figcaption`) musí obsahovat hlavní sdělení, protože na mobilu mohou být detaily malé.

### Ovládací prvky

- Používejte `Inputs.range`, `Inputs.select`, `Inputs.radio`. Jsou dotykově použitelné.
- Posuvníky mají být přes celou šířku textu. Pro dotyk je vhodné cílové políčko nejméně 44 px vysoké.
- Ovládací prvky dávejte nad graf, ne vedle něj, a vždy s krátkým popiskem.
- Posuvník s celými čísly má `step: 1`. Na mobilu se špatně nastavují desetinná čísla, proto volte rozumný krok.
- Počet prvků omezte. Na telefonu mají dva až tři prvky nad grafem smysl, víc už ne.
- Pro volbu z několika málo možností použijte `Inputs.radio`. Při delším seznamu `Inputs.select`.

### Příklad

````markdown
```{ojs}
//| echo: false
import {C, plotStyle} from "../assets/jhrules.js"

viewof x1 = Inputs.range([0, 10], {step: 1, value: 7, label: "Respondent 1"})

Plot.plot({
  style: plotStyle,
  width: width,
  height: Math.min(width, 500),
  marginLeft: 40,
  x: {domain: [0, 10], label: "Osa x₁"},
  y: {domain: [0, 10], label: "Osa x₂"},
  marks: [
    Plot.dot([{x: x1, y: 3}], {x: "x", y: "y", fill: C.primary, r: 6})
  ]
})
```
````

### Kontrola před odevzdáním

- Graf se při zúžení okna na přibližně 360 px nepřekrývá a nepřetéká.
- Všechny popisky jsou čitelné bez přiblížení.
- Ovládací prvky jdou nastavit prstem.
- Graf nepoužívá pevnou šířku ani výšku.
- Význam obrázku je zřejmý i z popisku pod ním.

## 5. Barevné schéma pro OJS

Paleta JHRules je převzatá z `hag_custom.scss` (proměnné `$jh-*`), což je jediný zdroj pravdy.
V OJS se barvy **nikdy nepíší napevno**, berou se z modulu, který je čte z CSS:

```js
import {C, gradient, plotStyle} from "../assets/jhrules.js"
```

- Cesta je **relativní k souboru kapitoly** (`../assets/…`). Absolutní `/assets/…` Quarto odmítne.
- Import patří **jen do jedné (první) OJS buňky kapitoly**. Jinak se `C` definuje víckrát a stránka se rozbije.

| Konstanta | Hodnota | Použití |
|---|---|---|
| `C.bg` | `#FFFFFF` | pozadí stránky a grafu (graf má průhledné pozadí) |
| `C.text` | `#3D3D3D` | běžný text, nadpisy, druhá datová řada |
| `C.primary` | `#4682B4` | hlavní datová barva (sloupce, křivky, prvky grafu) |
| `C.primaryLight` | `#A9C6DE` | výplně, podklady, vedlejší řady téže věci |
| `C.primaryText` | `#3D729E` | tmavší primary jen pro odkazy a text (kontrast ≥ 4,5 : 1) |
| `C.accent` | `#D35400` | NA CO SE DÍVAT: jedna věc na obrázek (zvýrazněný bod, hodnota, výsledek) |
| `C.context` | `#7F7F7F` | kontext: osy, popisky, vedlejší data |
| `C.contextLight` | `#D3D3D3` | okrajové a pomocné prvky |
| `C.grid` | `#EBEBEB` | mřížka (jen vodorovná, jemná) |
| `C.warning` | `#8C2D35` | pouze varování a chyby (tlumená bordó) |

Úplná pravidla stylu JHRules: `docs_for_agents/jhrules/README.md`.

Principy:

- Čistý design: bílé pozadí, tlumeně tmavě šedý text (ne čistá černá), žádné rámečky, stíny ani přechody.
- Jedna akcentová barva: `primary` nese veškerý důraz a nemusí se šetřit.
- Výjimka je výjimka: `accent` zvýrazňuje jen jeden prvek (bod, sloupec, výsledek).
- Kontext ustupuje: osy, popisky a potlačená data jsou šedé (`context`, `contextLight`).
- Zvýraznění místo duhy: víc kategorií = jedna `primary` a zbytek `contextLight`, případně plynulé stupňování `gradient(n)`.

Grafy:

- Bez horní a pravé osy. Mřížka žádná nebo jemná (`C.grid`), jen ve směru čtení hodnot.
- Legendy bez rámečku, raději přímé popisky u čar.
- Hlavní řada `C.primary`, srovnávací `C.text` nebo `C.context`, potlačené `C.contextLight`.
- Společný styl: `Plot.plot({ style: plotStyle, ... })` (průhledné pozadí, Arial, 12 px).
- Popisky obrázků jsou v barvě `context` (13 px), text je v Arialu, kód v monospace.
- Přístupnost: `primary` a `accent` mají na bílé kontrast jen kolem 4 : 1. Text v těchto barvách patří tučně nebo od 18 px. Odkazy mají tmavší `C.primaryText`. `context` je jen pro popisky os, ne pro hlavní text.

Python (matplotlib, plotly): `from jhrules import C, use_matplotlib, use_plotly`. Animace (manim): bílé pozadí, objekty a rovnice `text`, hlavní objekt `primary`, pomocné konstrukce `context` nebo `contextLight`, jeden klíčový moment `accent`.

## 6. Struktura kapitoly

**ZÁVAZNÁ STRUKTURA KAŽDÉ KAPITOLY (Cognitive Load Theory)**

> POKYN – začátek kapitoly:
> Hned pod hlavní nadpis kapitoly (H1) vlož motivační odstavec.
> Tento odstavec nastíní reálný, praktický problém z oblasti ekonomiky,
> managementu nebo medicíny, který bez znalosti této kapitoly nelze efektivně vyřešit.
> Odstavec musí studenta vtáhnout do děje a ukázat mu, PROČ se dané téma učí.
> Rozsah: 3–5 vět. Žádné klišé typu "V této kapitole se podíváme...".

Šablony ve vnější ohradě ze čtyř zpětných apostrofů (````) se kopírují BEZ této vnější ohrady.

Kapitola se skládá z nejvýše 5 sekcí, bloku aplikačních úloh a závěru.
Každá sekce pokrývá JEDEN koncept. Kratší je lepší.

---

### SEKCE  (opakuj nejvýše 5×)

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
Blok obsahuje 2–3 delší úlohy z reálné praxe.
Oblasti: ekonomika a management, nebo medicína a veřejné zdraví.
Inspirace stylem: Elementary Linear Algebra (Anton), Grinstead & Snell.

Každá aplikační úloha má:
- **Kontext** (2–4 věty reálného příběhu, ne abstraktní zadání)
- **Více dílčích otázek** označených a), b), c) – budují na sobě
- Tabset Zadání (shrnutí) / Řešení

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

## 7. Callout třídy

Callouty slouží k oddělení doplňkového obsahu od hlavního výkladu. Projekt používá tři typy: `.callout-note`, `.callout-tip` a `.callout-warning`. Vzhled řídí `hag_custom.scss`: ikony jsou vypnuté a každý callout má silnější levou hranu. Barvy do callout nikdy nepřepisujte.

### Pravidla pro všechny callouty

- Titulek se píše jako nadpis druhé úrovně (`## Titulek`) na prvním řádku uvnitř calloutu. Stejně se píší i záložky a shodně se šablonou v sekci 6.
- Titulky jsou bez emoji. Atribut `title=` ani nadpis `# Titulek` se v nových kapitolách nepoužívá.
- Titulek je krátký a věcný, nejvýše několik slov.
- Uvnitř calloutu nepoužívejte další nadpisy. Ostatní text je běžný odstavec.
- Callouty neskládejte do sebe a nepoužívejte je jako dekoraci. Na jednu obrazovku patří nejvýše jeden.
- Dlouhý obsah (odvození, algebraický výklad) dejte do sbaleného calloutu: `collapse="true"`.

````markdown
::: {.callout-note collapse="true"}
## Odvození, že součet odchylek je nulový

Zde je postup odvození...
:::
````

### `.callout-note` (poznámka)

Použijte pro doplňující myšlenku, interpretaci nebo odvození, které navazuje na hlavní text, ale nepatří do něj.

- Typický obsah: geometrický význam právě odvozeného vzorce, poznámka o značení, volitelné odvození.
- Pro náročnější nebo nepovinný obsah používejte sbalenou variantu (`collapse="true"`).
- Krátká poznámka bez titulku je možná, ale titulek je preferovaný.

````markdown
::: {.callout-note}
## Význam nulového součtu

Součet odchylek je nulový, protože průměr je těžiště. Záporná a kladná strana jsou v rovnováze.
:::
````

### `.callout-tip` (tip)

Použijte pro praktickou radu, zkratku nebo doporučený postup. Čtenáři má usnadnit práci.

- Typický obsah: jak si pojem zapamatovat, jak ho ověřit v interaktivním grafu, kdy použít který vzorec.
- Tip je krátký a konkrétní, bez teorie.
- Vyzvěte čtenáře k jedné akci, např. „Posuňte posuvník a sledujte, jak se mění vektor odchylek.“

````markdown
::: {.callout-tip}
## Vyzkoušejte

Změňte hodnotu respondenta 2 a sledujte, že vektor odchylek zůstává kolmý k přímce průměru.
:::
````

### `.callout-warning` (varování)

Použijte pro místa, kde se čtenář snadno splete: častá chyba, výjimka z pravidla, nebezpečné zjednodušení.

- Používejte ho střídmě, jinak varování ztratí váhu. Doporučení: nejvýše jedno na kapitolu nebo sekci.
- Obsah má říct, co je chyba, proč vzniká a jak se jí vyhnout.
- Varování neslouží pro obecné zajímavosti. Ty patří do `.callout-note`.

````markdown
::: {.callout-warning}
## Pozor na dělení

Rozptyl dělíme počtem pozorování $n$ (popisná statistika). Výběrový rozptyl by se dělil $n-1$.
:::
````

### Jak vybrat správný typ

| Chci čtenáři sdělit | Typ |
|:---|:---|
| doplňující souvislost, interpretaci nebo odvození | `.callout-note` |
| praktickou radu nebo vyzvat k vyzkoušení | `.callout-tip` |
| upozornit na častou chybu nebo úskalí | `.callout-warning` |
| definici pojmu | `.definition-box` (ne callout) |
| řešený příklad | `.example-box` (ne callout) |

Definice a příklady mají vlastní třídy. Nepoužívejte pro ně callouty.
