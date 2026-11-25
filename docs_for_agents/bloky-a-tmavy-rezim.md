# Bloky (callouty), zvýraznění pojmů a tmavý režim

Platí pro všechny kapitoly. Barvy grafů a animací jsou v `docs_for_agents/animace-konvence.md` a `jhrules/README.md`,
tady jsou **bloky v textu** a **přepínač světlého a tmavého režimu**.

## Bloky se píší jako Quarto callouty

Zápis zůstává `::: {.callout-…}` (nadpis `## Nadpis`, rozbalování `collapse="true"` a další volby Quarto fungují). Vzhled se řídí
jen stylem knihy (`hag_custom.scss`), takže ruční psaní a úpravy se nemění. Quarto má pět pevných typů, další role se řeší
třídou přidanou ke stejnému bloku.

| Role | Zápis | Barva (světlý režim) | Vzhled |
|:---|:---|:---|:---|
| Poznámka | `::: {.callout-note}` | modrá `$jh-primary` | horní pruh, rámeček, lehké podbarvení |
| Klíčové poznatky | `::: {.callout-important}` | tmavě modrá `$jh-primary-dark` | plná hlavička v barvě, bílé písmo |
| Jak na to v Excelu | `::: {.callout-tip}` | olivová `$jh-green` | jako Poznámka |
| Příklad | `::: {.callout-note .priklad}` | tmavě olivová `$jh-green-dark` | jako Poznámka |
| Upozornění | `::: {.callout-caution}` | šedá `$jh-context` | jako Poznámka |
| Pozor | `::: {.callout-warning}` | cihlová `$jh-warning` | jako Poznámka |
| Zapamatujte si | `::: {.callout-note .zapamatuj}` | okrová `$jh-accent` | jako Poznámka |

- Ikony se nezobrazují. Barva titulku a pruhu je stejná.
- **Klíčové poznatky** (závěr kapitoly) jsou vždy `callout-important`, ne `callout-note`.
- Pojem se při definici zvýrazní `[pojem]{.highlight-term}` (tmavě modrý štítek s bílým písmem, v obou režimech stejný).
- Zelená a červená jsou jen pro bloky a text. **V grafech a animacích zůstává jen modrá, šedá a okrový akcent.**

## Soubory

- `hag_custom.scss`: světlá paleta (`$jh-*`, jediný zdroj; kopie v `jhrules.py` a záložní hodnoty v `assets/jhrules.js`) a všechna pravidla
  včetně bloků. Tmavý režim sem nepatří, ale proměnné `$callout-tint` a `$callout-solid-tint` (podbarvení) lze přepsat.
- `hag_dark.scss`: tmavý režim (proměnné `$jh-*` zesvětlené pro tmavé pozadí a odvozené proměnné Bootstrapu). Barvy zde **nejsou** v kontrole
  `crew.style_guide`, ta čte jen `hag_custom.scss`.
- `_quarto.yml`: `theme: dark: [cosmo, hag_dark.scss, hag_custom.scss]`, `light: [cosmo, hag_custom.scss]`.
  **Pořadí je důležité.** Quarto bere u vrstev motivu dřívější soubor jako silnější, proto je `hag_dark.scss` před `hag_custom.scss`.
  Co se v `hag_custom.scss` odvozuje (například `$body-bg: $jh-bg`), se v `hag_dark.scss` musí přepsat znovu.
  Výchozí je **první uvedený motiv, tedy tmavý režim**. Přepínač je pod logem v postranním panelu.
- Návrhy a náhled variant: `_drafts/paleta.qmd`.

## Tmavý režim a OJS

- Barvy v OJS (`C` z `assets/jhrules.js`) se čtou z CSS proměnných `--jh-*` jednou při načtení, v tmavém režimu tedy dostanou tmavé hodnoty.
- Po kliknutí na přepínač se stránka **načte znovu** (volba režimu se pamatuje), aby se grafy a plátna překreslila novými barvami.
  Posluchač je jen na kliknutí v `jhrules.js`, nehlídá se nic v pozadí, takže nemůže vzniknout smyčka.
- V OJS se barvy dál nepíší napevno. Bílé písmo na barevných plochách je výjimka jen v SCSS.
