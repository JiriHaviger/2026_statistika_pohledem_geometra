# CLAUDE.md

@docs_for_agents/AGENTS.md
@docs_for_agents/animace-konvence.md
@docs_for_agents/bloky-a-tmavy-rezim.md

## Tento projekt

Quarto kniha **„Statistika pohledem geometra“** (autor Jirka Haviger), publikovaná na GitHub Pages.
Starý název „Havi Notes“ se už nepoužívá.

### Struktura

- `_quarto.yml` – seznam kapitol (`book.chapters`) a téma (`hag_custom.scss`).
- `01-pravdepodobnost/`, `02-statistika/` – kapitoly knihy (`*.qmd`).
  Kapitoly mají jednotnou YAML hlavičku (jen `title:`, bez nadpisu `#`). Společná nastavení složky jsou v `_metadata.yml`
  (u pravděpodobnosti `execute: echo: false`), takže se v buňkách nepíše `//| echo: false`.
  Úvod části (`01-pravdepodobnost/intro.qmd`, zapojený přes `part:` v `_quarto.yml`) je záměrně obecný, **nevyjmenovává kapitoly**
  (jen průběh části, barevnou konvenci a ovládání ukázek), takže přidání kapitoly nevyžaduje jeho úpravu.
  Texty knihy vykají (ne tykání).
- `_drafts/` – pracovní místo pro rozpracované texty (Quarto složky začínající `_` nerenderuje).
- `_archiv/` – odložený generátor kapitol (CrewAI), staré podklady a zálohy. Nepoužívá se, nečíst a neupravovat bez pokynu
  (Quarto složku s `_` nerenderuje). Kniha se píše a ladí přímo s Claudem.
- `docs_for_agents/` – konvence pro Clauda (`animace-konvence.md`, `bloky-a-tmavy-rezim.md`, `jhrules/README.md`)
  a vzorové OJS buňky `ojs_vzory.qmd` (prohlídka: `quarto preview` tohoto souboru).

### Pravidla

- **Neměnit obsah existujících kapitol** (`*.qmd` v knize). Věcné nálezy jen vypsat autorovi.
- Nové texty ukládat do `_drafts/`, do knihy je přesouvá autor.
- Nespouštět `quarto publish` ani nic, co přepisuje existující soubory, bez výslovného pokynu.
- Necommitovat bez pokynu. Před větší změnou doporučit commit nebo větev.
- Po změně SCSS, `_quarto.yml` nebo OJS ověřit `quarto render` (bez nových chyb a varování).
- Nové soubory pojmenovávat ASCII `kebab-case` bez diakritiky a mezer (starší soubory zatím mají smíšené názvy).

### OJS buňky (Observable JS v Quarto)

- Všechny `{ojs}` buňky stránky sdílejí jeden globální prostor: názvy proměnných musí být v kapitole unikátní.
- `Inputs`, `Plot` a `d3` jsou dostupné bez `import`.
- Šířku grafu brát z vestavěné proměnné `width`, ne pevným číslem.
- Barvy nepsat napevno (hex): `import {C, gradient, plotStyle} from "../assets/jhrules.js"` (čte CSS proměnné `--jh-*`).
  Cesta je **relativní k souboru kapitoly** (kapitoly i `_drafts/` jsou o úroveň hlouběji); absolutní `/assets/…`
  Quarto odmítne. Import patří jen do jedné (první) OJS buňky kapitoly, jinak se `C` definuje víckrát.
  `assets/` se kopíruje do `_book` přes `project: resources:` v `_quarto.yml`.
  Nové kapitoly tak dělají; stávající kapitoly se zatím nemění.

### Barvy (styl JHRules)

- Úplná pravidla stylu: `docs_for_agents/jhrules/README.md` (čistý design, jedna akcentová barva, žádné rámečky, stíny ani přechody).
- **Jediný zdroj palety:** proměnné `$jh-*` v `hag_custom.scss`. Kopie jsou jen záložní hodnoty v `assets/jhrules.js`.
- Při změně palety upravit `hag_custom.scss`, `hag_dark.scss` a záložní hodnoty v `assets/jhrules.js`.
- Akcent (`accent`, okrová) jen na jednu věc na obrázek, jinak `primary` a šedé `context`. Varování `warning` (cihlová červená).
  V grafech jen modrá, šedá a akcent. Zelené, tmavě modré a červené odstíny jsou pro bloky v textu (viz `bloky-a-tmavy-rezim.md`).
- Kniha má světlý i tmavý režim, výchozí je **tmavý** (`hag_dark.scss`, přepínač pod logem). Změnu barev ověřit v obou.

### Prostředí

- Windows, PowerShell. Quarto je v PATH (`quarto render`).
- `git` není v PATH (autor používá GitHub Desktop); lze volat
  `$env:LOCALAPPDATA\GitHubDesktop\app-*\resources\app\git\cmd\git.exe`.
- API klíč je v `.env` (ignorovaný gitem) – nikdy ho nečíst, nevypisovat ani necommitovat.
