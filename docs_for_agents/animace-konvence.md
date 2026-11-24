# Konvence pro animace a interaktivní ukázky (OJS)

Platí pro všechny nové i upravované ukázky v knize. Doplňuje obecnou paletu v `docs_for_agents/jhrules/README.md`
(tam je „co je za barvu“, tady „co která barva v knize znamená“). Kdo ukázku píše nebo upravuje, drží se tohoto.

## Význam barev (tokeny z `assets/jhrules.js`, nikdy hex)

| Barva | Token | V ukázce znamená |
|---|---|---|
| modrá | `C.primary` | to, co se pozorovalo nebo nasimulovalo (hody, výběry, četnosti z dat), sledovaný jev |
| světle modrá | `C.primaryLight` | výplně a pásy (jev v obdélníku, pás tolerance) |
| oranžová | `C.accent` | teorie, ke které se pozorování blíží (úsečka PMF, schody CDF, čárka u sloupce), nebo jeden zvýrazněný prvek |
| šedá | `C.contextLight`, `C.context` | kontext: body mimo sledovaný jev, osy, pomocné popisky, „druhá možnost“ pro srovnání |
| tmavý text | `C.text` | texty, výběr (aktivní tlačítko), tmavá čárka teorie, když oranžová znamená něco jiného |
| bordó | `C.warning` | chyba, špatná odpověď |

- Oranžová nejvýše na jeden druh prvku v obrázku. Pokud oranžová už znamená „průnik“ (animace sjednocení), teorie je tmavá čárka a text to říká.
- Skupiny A, B, C: A modrá (`primary`), B světle šedá (`contextLight`), C tmavší šedá (`context`).
- Pokud text kapitoly nebo popisek mluví o barvě, musí odpovídat tomuto kódu. Při nové ukázce, která z konvence vybočuje, to vždy napsat do textu.

## Zápis a texty

- Vykání, česky. Čárka jako desetinný oddělovač v popiscích (`cz()` pomocí `.toFixed().replace(".", ",")`), v LaTeXu `0{,}5`.
- Obecné jevy velkými písmeny $A$, $B$, $C$. Pravděpodobnost úspěchu $\pi$, počet pokusů $n$, Poisson $\lambda$,
  hypergeometrické: $N$ (soubor), $M$ (úspěchy v souboru), $n$ (výběr). Konkrétní jevy z příkladu (karty) se pojmenují $A$, $B$.
- Pojem se zvýrazní `{.highlight-term}` jen u své definice (jednou v knize), jinde se na něj odkazuje.
- Texty neodkazují na pořadí kapitol ani je nevyjmenovávají (úvod části `intro.qmd` je záměrně obecný).

## Ovládání

- Průběžné pouštění: **Plynule / Pauza**, kroky **+1** (nebo +10), **+100**, vždy **Restart**. Vlastní ovládací prvky přes `animation({buttons: false, controls})`.
- Volba režimu (rozdělení, podmínka, úroveň měření): řada tlačítek `makeButton`, aktivní má obrys `C.text` a tučné písmo. Posuvník jen pro plynulý parametr.
- První kroky pomalu (jednotlivý hod je vidět), pak zrychlit. Po ručním kroku se výsledek ukáže hned.
- Osy histogramů pevné (měřítko se nesmí měnit s přibývajícími daty) a s hodnotami (aspoň 0 a maximum). Teorie je vždy na stejném místě.

## Technické zásady (prohlížečová odolnost)

- Šířka přes `width = columnWidth(Generators)` (každá kapitola má jednu úvodní buňku s importy). **Nikdy** nepoužívat vestavěné `width`.
- **Nezpůsobovat změnu výšky stránky po vytvoření buňky.** Buňka, na které závisí šířka, se po každé změně šířky vytvoří znovu.
  Pokud se pod ní po chvíli změní výška (například objeví popis), může vzniknout smyčka a animace bliká. `columnWidth` proto oznamuje jen skutečnou změnu šířky
  a `animation()` vykreslí první snímek ihned. Nový kód se tomu nesmí vyhýbat (žádné vkládání prvků do stránky z časovačů).
- Stav ukázky patří do objektu `state` uvnitř `animation()`, ne do globálních proměnných buňky. Pozor na proměnné mimo `state` (například odkazy na tlačítka), ty se vytvoří při každém překreslení buňky.
- Canvas se kreslí jen z `draw`, nic jiného do něj nesahá. Měnit velikost canvasu jen v `draw` s vymazáním (viz 032, blok se slovy).
- Používat jen to, co umí všechny běžné prohlížeče (Chrome, Edge, Opera, Vivaldi, Brave, Safari, Firefox): canvas 2D, `ResizeObserver`, `IntersectionObserver`, `Array.flatMap`.
  Nepoužívat `ctx.roundRect`, `structuredClone`, top-level `await` a podobné novinky bez ověření. Po změně vždy `quarto render` bez varování.
