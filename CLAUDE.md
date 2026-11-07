# CLAUDE.md

@docs_for_agents/AGENTS.md

## Tento projekt

Quarto kniha **„Statistika pohledem geometra“** (autor Jirka Haviger), publikovaná na GitHub Pages.
Starý název „Havi Notes“ se už nepoužívá.

### Struktura

- `_quarto.yml` – seznam kapitol (`book.chapters`) a téma (`hag_custom.scss`).
- `01-pravdepodobnost/`, `02-statistika/` – kapitoly knihy (`*.qmd`).
- `_drafts/` – pracovní místo pro rozpracované a vygenerované texty (Quarto složky začínající `_` nerenderuje).
- `crew_agents.py`, `crew/`, `chapters.py` – generátor kapitol (CrewAI + Claude, model v `crew/config.py`).
  Běží v `.venv` (`.venv\Scripts\python.exe`); kontrola style guide bez API: `.venv\Scripts\python.exe -m crew.style_guide`.
- `docs_for_agents/` – podklady pro agenty (`style_guide.md`, `audit_report.md`, jednorázová zadání).

### Pravidla

- **Neměnit obsah existujících kapitol** (`*.qmd` v knize). Věcné nálezy jen vypsat autorovi.
- Nové nebo generované texty ukládat do `_drafts/`, do knihy je přesouvá autor.
- Nespouštět generátor kapitol, `quarto publish` ani nic, co přepisuje existující soubory, bez výslovného pokynu.
- Necommitovat bez pokynu. Před větší změnou doporučit commit nebo větev.
- Po změně SCSS, `_quarto.yml` nebo OJS ověřit `quarto render` (bez nových chyb a varování).
- Nové soubory pojmenovávat ASCII `kebab-case` bez diakritiky a mezer (starší soubory zatím mají smíšené názvy).

### OJS buňky (Observable JS v Quarto)

- Všechny `{ojs}` buňky stránky sdílejí jeden globální prostor: názvy proměnných musí být v kapitole unikátní.
- `Inputs`, `Plot` a `d3` jsou dostupné bez `import`.
- Šířku grafu brát z vestavěné proměnné `width`, ne pevným číslem.
- Barvy nepsat napevno (hex), ale brát ze sdílené palety projektu.

### Prostředí

- Windows, PowerShell. Quarto: `G:\Quarto\bin\quarto.exe`, Python 3.12.
- `git` není v PATH (autor používá GitHub Desktop); lze volat
  `$env:LOCALAPPDATA\GitHubDesktop\app-*\resources\app\git\cmd\git.exe`.
- API klíč je v `.env` (ignorovaný gitem) – nikdy ho nečíst, nevypisovat ani necommitovat.
