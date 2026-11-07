<!--
  GENEROVÁNO automaticky (python main.py style --force). Needitovat ručně.
  Sekce 5 a 6 vkládá Python (crew/style_guide.py), ostatní píše LLM.
  Datum: 2026-11-07
  Zdroje (sha256):
    _quarto.yml: 9da063e7ec705f7d1ef052b5b3dab668cfda562d91a416f47e153745349cfcd7
    hag_custom.scss: 8b90a1499bb82ed24e2931799dce01a337953fc38a25e9647d4889783698bfd4
    jhrules.py: 15818ee72f2047b6e6e56c82a6a3b70695696f34962597a48878566828d7e392
    assets/jhrules.js: 085b59f7e0426d93beaac5a7e8bca868400b74b33b4ea30a8d86353ee822eea2
-->

# Style Guide: Statistika pohledem geometra

## 1. Celkový styl

Učebnice *Statistika pohledem geometra* má působit vzdušně a klidně. Čtenář má mít prostor přemýšlet nad obrázkem a nemá se prokousávat hustým textem. Interaktivní vizualizace a geometrický pohled mají přednost před dlouhým výkladem.

**Odstavce a text**

- Odstavec má obvykle 2–4 věty a vyjadřuje jednu myšlenku. Delší blok rozděl.
- Mezi vysvětlením, vzorcem a grafem nech prázdný řádek. Vzorec nezačíná uprostřed věty, pokud to není nutné.
- Piš česky, tykej čtenáři a používej činné tvary („spočítáme“, „podíváme se“). Vyhýbej se dlouhým souvětím.
- Nový pojem zvýrazni tučně při prvním výskytu. Za český termín dej v závorce kurzívou anglický ekvivalent, např. **směrodatná odchylka** (*standard deviation, sd*).
- Přes `.highlight-term` a `.definition-box` označuj jen skutečné definice. Jinak by zvýraznění ztratilo smysl.
- Před odevzdáním text pročti kvůli překlepům. Ve starších kapitolách jich je dost a v nových se opakovat nemají.
- Název projektu se píše vždy přesně „Statistika pohledem geometra“.

**Písmo**

- Celá kniha používá bezpatkové písmo (Arial, Helvetica) a neproporcionální písmo jen pro kód. Fonty v kapitolách nepřepisuj.
- Velikost písma ani řez nastavuj lokálně jen výjimečně. Typografii řídí `hag_custom.scss`.
- Barvu textu a nadpisů nenastavuj ručně. Přebírá se z motivu.

**Hierarchie nadpisů**

| Úroveň | Použití |
|:---|:---|
| H1 (`#`) | Název kapitoly. Právě jeden na soubor. |
| H2 (`##`) | Sekce kapitoly. |
| H3 (`###`) | Podsekce uvnitř H2. |
| H4 (`####`) | Výhradně v závěru kapitoly („Shrnutí pojmů“, „Pracuj s AI“), viz šablona v sekci 6. |

- Úrovně nepřeskakuj (po H2 následuje H3, nikdy rovnou H4).
- Nadpisy H1–H3 mají v motivu automaticky barevnou levou linku. Nenahrazuj ji vlastním ohraničením ani obrázkem.
- Nadpisy začínají velkým písmenem a nekončí tečkou. Písmena v nich neformátuj ručně.
- Titulek calloutu se píše jako nadpis druhé úrovně (`## Titulek`) na prvním řádku uvnitř calloutu. Podrobnosti jsou v sekci 7.
- Nezačínej kapitolu H2 bez úvodního odstavce. Pod H1 vždy stručně řekni, o čem kapitola je a na co navazuje.

**Obrázky a grafy**

- Interaktivní vizualizace jsou standard. Jsou to OJS bloky s `//| echo: false` a štítkem `//| label: fig-...`.
- Pod obrázek patří stručný popisek, který říká, co si čtenář má všimnout. Obrázek s popiskem zabal do divu `::: {#fig-...}`.
- Na jeden obrázek zvýrazni jen jednu věc. Barvy bere graf z palety projektu (sekce 3 a 5).

**Názvy souborů**

- Nové soubory kapitol se jmenují ASCII kebab-case bez diakritiky a mezer, např. `06-spojita-rozdeleni.qmd`.
- Starší názvy (např. `02_deskriptivní statistiky momenty.qmd`) se přejmenují později. Nepřejmenovávej je sám a ve stávajících kapitolách je nepřebírej jako vzor.
- Každý nový soubor se přidá do `chapters:` v `_quarto.yml` pod správnou `part`.

## 2. Dvojjazyčnost

Kniha má dnes `lang: cs` a přepínač CS/EN zatím neexistuje. Nové kapitoly se ale píšou tak, aby se přepínač dal doplnit bez přepisování obsahu. Hlavní zásada je, že česká a anglická verze mají **stejnou strukturu**. Liší se jen jazyk textu.

**Struktura**

- Každý logický blok textu (odstavec, definice, callout, popisek obrázku) existuje v obou jazycích na odpovídajícím místě a ve stejném pořadí.
- Obě verze mají stejné nadpisy na stejných úrovních, stejný počet odstavců, stejné obrázky i stejné callouty.
- Vzorce, data, kód a parametry grafů jsou společné a nekopírují se. Překládá se jen text kolem nich a popisky.
- Nenechávej v kapitole pasáže, které existují jen v jednom jazyce, pokud to není záměr. Takovou pasáž označ poznámkou pro redakci.
- Název projektu „Statistika pohledem geometra“ se nepřekládá.

**Značení jazykových bloků**

Texty v obou jazycích obal do divů s třídou `.lang-cs` a `.lang-en`. Přepínač později jeden z nich skryje. Mezi dva bloky vlož prázdný řádek.

````markdown
::: {.lang-cs}
**Průměr** (*mean*) je těžiště dat. Když páku podepřeme v průměru, bude v rovnováze.
:::

::: {.lang-en}
The **mean** is the centre of mass of the data. If we support the lever at the mean, it balances.
:::
````

- Identifikátory (`#sec-...`, `#fig-...`, `label:`) musí být v dokumentu jedinečné. Vzorec názvu je `sec-moment-cs` a `sec-moment-en`, tedy stejný základ s příponou jazyka.
- Křížové odkazy (`@fig-...`) pište vždy na identifikátor ve stejném jazyce.

**Terminologie**

- Při prvním výskytu odborného pojmu uveď český termín a v závorce kurzívou anglický: **špičatost** (*kurtosis*), **těžké ocasy** (*heavy tails*).
- Používej jen jeden český termín pro jeden anglický pojem v celé knize. Pokud váháš, dohledej, co používají již hotové kapitoly.
- Zkratky u vzorců mají anglický původ (`sd`, `var`, `skew`, `kurt`). V obou jazycích zůstávají stejné.

**Texty uvnitř OJS grafů**

- Popisky os, legendy, texty v `Plot.text` a popisky ovládacích prvků nepiš natvrdo do volání grafu. Dej je do jednoho objektu se slovníkem textů, který půjde později napojit na přepínač.
- Číselné formátování řeš tak, aby šlo přepnout (desetinná čárka v češtině, tečka v angličtině). Nepiš ručně `.toFixed()` s pevným řetězcem, pokud to jde obejít.

````markdown
```{ojs}
//| echo: false
texty = ({
  cs: { osaX: "Hodnota (poloha na páce) →", teziste: "Těžiště (průměr)" },
  en: { osaX: "Value (position on the lever) →", teziste: "Centre of mass (mean)" }
})
jazyk = "cs"   // později se napojí na přepínač CS/EN
t = texty[jazyk]
```
````

**Co zatím nedělat**

- Nevytvářej samostatné anglické soubory kapitol ani nepřidávej anglické položky do `_quarto.yml`. Přepínač se řeší centrálně a až později.
- Nepřekládej strojově bez kontroly. Anglické texty musí projít redakcí stejně jako české.

## 3. Dark / Light mode

**Současný stav**

- `_quarto.yml` definuje světlé i tmavé téma (`light` a `dark`), ale obě používají stejný základ: `cosmo` a `hag_custom.scss`. Tmavý režim proto zatím **není skutečně tmavý**.
- Právě se ladí jen světlý režim. Tmavý přijde později.
- Pozor na jednu věc: nic se nemá ladit „na oko“ jen pro světlé pozadí. Nové kapitoly se píšou tak, aby po doplnění tmavého motivu fungovaly bez úprav.

**Základní pravidlo: žádné napevno zadané barvy**

Barvy v kapitolách (v divech, stylech i grafech) se **nikdy nepíšou napevno**. Nepoužívej hexadecimální kódy, `rgb(...)`, ani pojmenované barvy typu `steelblue`, `darkred`, `black`, `white`, `grey`. Takové barvy nereagují na změnu motivu. Najdeš je ve starších kapitolách a nejsou vzorem.

Barvy projektu tvoří paleta JHRules:

- V `hag_custom.scss` jsou to proměnné `$jh-*`. Ty se používají jen v SCSS, nikdy v `.qmd`.
- Zároveň jsou dostupné jako CSS proměnné `--jh-*` (např. `--jh-text`, `--jh-bg`, `--jh-primary`, `--jh-accent`, `--jh-context`, `--jh-grid`, `--jh-warning`).
- V OJS se berou z modulu `assets/jhrules.js`.
- Konkrétní hodnoty a pravidla jejich použití jsou v sekci 5.

**HTML a divy**

- Vlastní `<div>` a inline styly barvu přebírají z CSS proměnných: `color: var(--jh-text)`, `background: var(--jh-bg)`, ohraničení z `var(--jh-primary)`. Pokud potřebuješ jemný podklad, použij průhlednost přes `color-mix` nebo přes `opacity`, nikoli novou pevnou barvu.
- Pokud potřebuješ nový opakovaně použitý styl, neřeš ho v kapitole. Přidej třídu do `hag_custom.scss` a v kapitole použij jen třídu.
- Nejdřív zkus existující třídy: `.definition-box`, `.example-box`, `.highlight`, `.highlight-key`, `.highlight-warning`, `.highlight-term`, `.accent`, `.muted`.
- Nespoléhej na to, že pozadí je bílé. Nepoužívej bílý okraj kolem bodů ani bílé výplně „aby to vypadalo čistě“. Použij barvu pozadí z motivu.
- Význam nikdy nenes pouze barvou. K barevnému rozlišení přidej popisek, tvar značky, styl čáry nebo text.

````markdown
::: {style="border-left: 4px solid var(--jh-primary); padding-left: 1rem; color: var(--jh-text);"}
Takto se píše vlastní div. Barvy jdou z proměnných motivu, ne napevno.
:::
````

**OJS grafy**

- Barvy do grafu importuj z modulu a používej je místo textových názvů. Konkrétní klíče objektu `C` ověř přímo v `assets/jhrules.js`, nevymýšlej si vlastní.
- Graf nesmí mít nastavené pevné pozadí. Průhledné pozadí a zděděná barva textu zajistí, že osy a popisky budou čitelné na světlém i tmavém podkladu.
- Osy, mřížku a vedlejší prvky kresli barvami pro kontext a mřížku. Barvu pro zdůraznění použij jen na jednu věc, na kterou se má čtenář dívat.

````markdown
```{ojs}
//| echo: false
import {C} from "/assets/jhrules.js"

Plot.plot({
  width,
  style: { background: "transparent", color: "inherit", fontSize: "14px" },
  marks: [
    Plot.ruleY([0]),
    Plot.dot(data, { x: "x", y: "y", fill: C.primary }),
    Plot.dot([vyber], { x: "x", y: "y", fill: C.accent, r: 8 })
  ]
})
```
````

- Barvy proto vždy odkazuj přes `C.<název>` a nepiš je do každého volání zvlášť.
- Pokud graf používá víc datových řad, rozliš je i stylem čáry (plná, čárkovaná, tečkovaná) a popiskem. Starší kapitoly rozlišují jen barvami a to nestačí.
- Po doplnění tmavého motivu bude potřeba každý graf zkontrolovat v obou režimech. Piš ho tak, aby nezbyl žádný napevno zadaný odstín, který by se musel hledat a přepisovat.

## 4. Responsive design

Čtenáři otevírají knihu často na mobilu. Každá OJS vizualizace musí být čitelná a ovladatelná na úzké obrazovce, tedy od šířky přibližně 360 px.

**Šířka a výška**

- Šířku grafu bereme z vestavěné OJS proměnné `width`, která odpovídá šířce obsahu stránky. Díky tomu se graf přizpůsobí zařízení a po změně velikosti okna se překreslí.
- Nepiš pevnou šířku (`width: 500`, `width: 600`), která na mobilu přeteče nebo se zmenší tak, že text zmizí. Pevné rozměry jsou ve starších kapitolách a nesmí se přebírat.
- Výšku odvoď od šířky, např. `height: Math.round(width * 0.6)`, a omez ji shora i zdola. Pro čtvercové grafy (geometrické vizualizace) použij `Math.min(width, 500)` pro obě strany.
- Extrémní výšky (několik set pixelů navíc) na mobilu nutí čtenáře dlouho rolovat. Graf se má vejít na obrazovku.
- Text uvnitř grafu nesmí překrývat data. U úzkého grafu přesuň legendu pod graf, nebo ji vypiš do textu v HTML.

**Písmo**

- Velikost písma v grafu nesmí být menší než 12 px. Doporučená hodnota je 14 px (`style: {fontSize: "14px"}`).
- Na úzké obrazovce zkrať popisky os a zmenši počet značek na ose (`ticks`), aby se nepřekrývaly.
- Zvaž větší levý okraj (`marginLeft`), aby se vešly popisky osy y.
- Dlouhé texty uvnitř grafu (jako výsledky výpočtů) piš pod graf do odstavce, ne přes `Plot.text` s pevnými souřadnicemi.

**Ovládací prvky**

- Posuvníky, výběry a přepínače musí mít dostatečně velkou dotykovou plochu (alespoň zhruba 44 × 44 px). Nepřetěsnávej je k sobě.
- Preferuj posuvníky s rozumným krokem (`step`) a málo hodnotami. Rozsah 0–200 s krokem 1 se na dotykovém displeji ovládá špatně.
- Popisky ovládacích prvků drž krátké, aby se nezalamovaly přes celý řádek.
- Ovládací prvky umísťuj nad graf, ne vedle něj. Čtenář je pak nepřekryje prstem a graf zůstane plně viditelný.
- Informace nesmí být dostupná jen po najetí myší (`hover`, tooltip). Na dotykových zařízeních hover není. Důležitý údaj vždy vypiš v textu nebo v popisku.
- Počet ovládacích prvků na jednu vizualizaci drž nízký. Jeden až dva jsou dobře, víc se na mobilu rychle stává nepřehledným.

````markdown
```{ojs}
//| echo: false
import {C} from "/assets/jhrules.js"

viewof hodnota = Inputs.range([0, 10], {step: 1, value: 5, label: "Hodnota"})

{
  const uzky = width < 480
  const strana = Math.min(width, 500)
  return Plot.plot({
    width: strana,
    height: strana,
    style: { background: "transparent", color: "inherit", fontSize: uzky ? "12px" : "14px" },
    x: { domain: [0, 10], label: "Osa x₁", ticks: uzky ? 5 : 10 },
    y: { domain: [0, 10], label: "Osa x₂", ticks: uzky ? 5 : 10 },
    marks: [
      Plot.dot([{x: hodnota, y: hodnota}], { x: "x", y: "y", fill: C.accent, r: 6 })
    ]
  })
}
```
````

**Kontrola před odevzdáním**

- Prohlédni kapitolu v úzkém okně prohlížeče (zhruba 360 px) a v režimu mobilního zařízení ve vývojářských nástrojích.
- Ověř, že graf nepřetéká, texty se nepřekrývají, ovládací prvky jdou ovládat prstem a nic nevyžaduje hover.

## 5. Barevné schéma pro OJS

Paleta JHRules je převzatá z `hag_custom.scss` (proměnné `$jh-*`), což je jediný zdroj pravdy.
V OJS se barvy **nikdy nepíší napevno**, berou se z modulu, který je čte z CSS:

```js
import {C, gradient, plotStyle} from "/assets/jhrules.js"
```

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

Projekt používá tři typy calloutů: `.callout-note`, `.callout-tip` a `.callout-warning`. Jejich vzhled řídí `hag_custom.scss`, a proto nic v kapitole nestyluj ručně.

**Společná pravidla**

- Callout se zapisuje jako div se třídou: `::: {.callout-note}` a končí `:::`.
- **Titulek se píše jako nadpis druhé úrovně (`## Titulek`) na prvním řádku uvnitř calloutu.** Takto to ukazuje šablona v sekci 6. Starší kapitoly používají `# Titulek`, což pro nové kapitoly neplatí.
- Titulek je krátký a konkrétní („Odvození, že součet odchylek je nulový“). Nepoužívej obecné „Poznámka“.
- Ikony jsou v projektu vypnuté. Význam calloutu tedy nese titulek a barevný pruh vlevo. Barva sama nestačí, protože `.callout-note` a `.callout-tip` mají podobný pruh. Typ calloutu proto vždy vyjádři i slovy v titulku nebo v prvním odstavci.
- Callout je krátký. Dlouhé vysvětlení patří do běžného textu. Uvnitř calloutu zachovej styl z sekce 1 (krátké odstavce).
- Callouty nezanořuj do sebe. Nepoužívej je k formátování celé kapitoly.
- Nepoužívej H3 a nižší nadpisy uvnitř calloutu.
- Nepiš do calloutu ručně nastavené barvy. Platí pravidlo ze sekce 3.

**Varianty vzhledu**

- Výchozí varianta (`default`) je standard.
- Varianta `appearance="simple"` skryje rámeček, nechá jen pruh a titulek. Hodí se pro lehčí poznámky.
- Varianta `appearance="minimal"` skryje titulek úplně. Použij ji jen tehdy, když se význam jasně vyplývá z textu a titulek by byl zbytečný. Titulek se v ní nezobrazí, ale přesto ho napiš kvůli konzistenci a dostupnosti.
- Dlouhá odvození a doplňující výklad pro zájemce skládej přes `collapse="true"`. Čtenář tak nemusí text přeskakovat.

**`.callout-note` – poznámka**

Použij pro doplňující informaci, shrnutí myšlenky nebo odvození, které není nutné číst ihned. Typicky:

- doplňující výklad nebo souvislost s jiným tématem,
- odvození vzorce nebo geometrický pohled „pro zájemce“ (sbalený `collapse="true"`),
- shrnutí důsledku právě odvozeného výsledku.

**`.callout-tip` – tip**

Použij pro praktickou radu, trik nebo pomoc k lepšímu porozumění:

- jak si pojem představit nebo na co se v grafu dívat,
- tip na interakci s vizualizací („Posuň jezdec a sleduj, jak se mění odchylky“),
- doporučení postupu při výpočtu.

**`.callout-warning` – varování**

Použij střídmě, jen pro skutečné riziko chyby:

- častá chyba v interpretaci nebo ve výpočtu (např. záměna rozptylu a směrodatné odchylky),
- podmínky, za kterých metoda neplatí,
- pozor na rozdíl mezi dvěma podobnými pojmy.

Varování se vyznačuje samostatnou výraznou barvou. Kdyby ho bylo v kapitole příliš, přestane být vidět. Doporučení je nejvýše jedno až dvě varování na kapitolu.

**Příklady zápisu**

````markdown
::: {.callout-note collapse="true"}
## Odvození, že součet odchylek je nulový

Krátký úvod a pak vlastní odvození.
:::

::: {.callout-tip}
## Jak číst graf

Posuň jezdec a sleduj, jak se mění vektor odchylek.
:::

::: {.callout-warning}
## Pozor na záměnu pojmů

Rozptyl je ve čtvercích původní jednotky. Směrodatná odchylka je ve stejné jednotce jako data.
:::
````

**Co callouty nenahrazují**

- Definice patří do `.definition-box`, příklady do `.example-box`.
- Callout není náhrada za nadpis. Pokud by měl obsah vlastní téma, udělej z něj podsekci H3.
