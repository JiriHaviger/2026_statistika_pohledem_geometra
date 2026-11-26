# Otevřené otázky (rozhoduje autor, agent nic neměnil)

## Soubory mimo knihu

Žádný z těchto souborů není v `book.chapters` v `_quarto.yml` a nic na ně neodkazuje, takže se nerenderují.

| Soubor | Velikost | Obsah |
|---|---|---|
| `01-pravdepodobnost/intro.qmd` | 748 B | Motivační úvod „Kde se potkáš s pravděpodobností“ (příklady z reálného světa, rozpracované) |
| `00-matematika/index.qmd` | 55 B | „Tady nic není, vše je zatím jen v autorově hlavě.“ |
| `02-statistika/index.qmd` | 57 B | „Tady nic není, vše je zatím jen v autorově hlavě.“ |
| `03-datova-veda/index.qmd` | 58 B | „Zatím je vše jen v autorově hlavě, zde bude později.“ |

Možnosti:

1. **`intro.qmd`:** zařadit jako úvod části (`part: 01-pravdepodobnost/intro.qmd` v `_quarto.yml`). Ostatní kapitoly knihy začínají hned obsahem, úvod by byl nová věc.
2. **Prázdné `index.qmd`:** přesunout do `_drafts/` (nic se tím neztratí, git zachová historii) nebo smazat, až budou kapitoly opravdu vznikat.
3. Ponechat beze změny. Soubory nic nestojí, jen mátou (audit je hlásí jako „není v `_quarto.yml`“).

## Nástroje a rozhodnutí z revize

- **Tmavý režim:** `dark:` v `_quarto.yml` je stále stejné jako světlé téma (C2). Řešit v dalším kroku.
- **`freeze: auto`:** neaktivováno. Uložené výsledky výpočtů by se commitovaly do `_freeze/`; kapitoly jsou jen OJS, takže přínos je malý. Rozhodnout, jestli ho chcete.
- **Favicon:** chybí; `Logo.svg` je velká černá ilustrace, na favicon se nehodí (viz logo níže).
- **`site-url`:** odhadnuto z adresy repozitáře (`https://jirihaviger.github.io/2026_statistika_pohledem_geometra/`), ověřte.
- **Logo (C7):** viz zprávu v konverzaci; čeká na schválení variant.
- **Přejmenované kapitoly:** staré adresy URL (`…/02_prst_pravidla.html` apod.) po publikaci přestanou fungovat.
