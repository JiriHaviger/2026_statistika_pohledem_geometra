# Zadání pro agenta (v2): revize projektu „Statistika pohledem geometra"

Tato verze vychází z prohlídky skutečného repozitáře (`_quarto.yml`, `crew/*`, `docs_for_agents/*`, `.gitignore`, `04_prst_diskretni.qmd`, `04_deskriptivy z tabulky.qmd`, `index.qmd`, `intro.qmd`). Nahrazuje první verzi, která vycházela jen z nahraných souborů.

## Rozhodnutí autora (7. 11. 2026)

1. **Název projektu je „Statistika pohledem geometra“.** „Havi Notes“ je starý název a nemá se objevovat v generátoru ani v dokumentaci pro agenty.
2. **Nová kapitola „Diskrétní pravděpodobnostní rozdělení“ se nevytváří.** Záznam v `chapters.py` je pozůstatek přípravy generátoru. Téma pokrývá kapitola 4 (`04_prst_diskretni.qmd`).
3. **`intro.qmd` a podsložkové `index.qmd` (`00-matematika`, `02-statistika`, `03-datova-veda`): autor si nepamatuje, zda jsou záměrné.** Neměnit, nepřesouvat, nemazat. Jen sepsat podklady do `docs_for_agents/otevrene_otazky.md` a nechat rozhodnout autora. Kořenový `index.qmd` je v knize jako „Úvodní poznámky“ a zůstává.

## Pravidla práce

- Řiď se `docs_for_agents/AGENTS.md`. Před větší změnou vytvoř pojistku (commit nebo větev) a stručně popiš, co a proč měníš.
- **Neměnit obsah stávajících kapitol** (`*.qmd`). Měnit smí jen generátor (Python, `crew/`), SCSS, `_quarto.yml`, logo a dokumentaci. Věcné nálezy v kapitolách (příloha) řeší autor.
- **Nespouštět** generování kapitol, `quarto publish` ani nic, co přepisuje existující soubory.
- Po každém bloku: co se změnilo, jak to ověřit, co zůstalo otevřené. Necommitovat bez pokynu.
- U změn vzhledu a barev nejdřív připravit varianty a počkat na výběr autora.
- Ověřit, že `quarto render` projde bez nových chyb a varování.

**Co zatím nebylo prohlédnuto:** `01_typy promennych.qmd`, `02_deskriptivní statistiky momenty.qmd`, `03_aritmetika dat.qmd`, `05_analyza_rozptylu_geometricky.qmd`, `01-klasicka-prst.qmd`, `02_prst_pravidla.qmd`, `03_prst_distribuce.qmd`. Inventury (B1) je projdou.

## Doporučené pořadí

1. **A0 a A1** (generátor se nesmí spustit, dokud nejsou vyřešeny)
2. A2, A3 (rychlé a bezpečné)
3. A4 až A8 (kvalita generátoru)
4. B a C1 až C4 (barvy, tmavý režim, kontrast, responzivita)
5. Zbytek

---

## Blok A: Generátor kapitol (`crew_agents.py`, `crew/`, `chapters.py`)

### A0. Úklid `chapters.py` (kapitola o diskrétních rozděleních se nevytváří)

- `01-pravdepodobnost/04_prst_diskretni.qmd` už obsahuje binomické, geometrické, hypergeometrické a Poissonovo rozdělení, každé s interaktivním OJS grafem a poznámkou k Excelu.
- `chapters.py` přitom plánuje „Diskrétní pravděpodobnostní rozdělení" (binomické, Poissonovo, geometrické) do `02-statistika/05_diskretni_distribuce.qmd`. Číslo `05_` už má `05_analyza_rozptylu_geometricky.qmd` a `_quarto.yml` má zakomentovanou jinou cestu (`06_diskretni_distribuce.qmd`).
- **Rozhodnutí autora: kapitola se nevytváří** (záznam je pozůstatek přípravy generátoru). V `chapters.py` ponechat `CHAPTERS = []` a stávající položku převést na zakomentovaný vzor (struktura slovníku zůstane jako dokumentace). Zakomentovaný řádek `#- 02-statistika/06_diskretni_distribuce.qmd` v `_quarto.yml` navrhnout ke smazání, ale nemazat bez potvrzení. Dokud autor nepřidá novou položku, generování kapitol nemá co dělat.

### A1. `style_guide.md` je rozbitý

Soubor `docs_for_agents/style_guide.md` (ze kterého čerpají všichni agenti) obsahuje:

- blok `COLORS` a kus šablony struktury **na začátku souboru**, v kódovém bloku s nesouladnými ohradami (šest zpětných apostrofů),
- úvodní větu LLM („Následuje závazný Style Guide…") uprostřed souboru,
- **prázdnou sekci 5** (barevné schéma),
- **zkomolenou sekci 6** (šablona struktury se ztratila, zbyl jen fragment `{ojs}`),
- sekci 3, která tvrdí, že existuje jen světlé téma,
- starý název „Havi Notes“ (správný název je „Statistika pohledem geometra“),
- `warningDark: "#6f040f" // ztmaveno o 10 %`, což neodpovídá `darken(#8b0512, 10%)` (vychází zhruba `#5a030b`).

Příčina: LLM kopíruje bloky, a šablona v `prompts.py` obsahuje vnořené ohrady (```` ``` ```` uvnitř ```` ``` ````), které ukončí vnější blok.

- Sekce 5 a 6 vkládat **v Pythonu** po vygenerování (COLORS z B3, CHAPTER_STRUCTURE z `prompts.py`). Nesvěřovat LLM.
- Vnější ohradu pro vnořený obsah dělat čtyřmi zpětnými apostrofy nebo `~~~~` (v `prompts.py` i ve style guide).
- Výstup LLM zpracovat: odříznout vše před prvním `#`, ověřit nadpisy 1 až 7 v daném pořadí, sudý počet ohrad, neprázdnou sekci 5.
- Do hlavičky uložit sha256 vstupů (`_quarto.yml`, `hag_custom.scss`, případně brand soubor). Při neshodě varovat a vyžadovat `style --force`.
- Po opravě style guide **přegenerovat** a předložit autorovi diff. Správný název projektu je „Statistika pohledem geometra“ (viz Rozhodnutí autora). Prohledat repozitář na „Havi Notes“: v generátoru, `prompts.py` a `docs_for_agents/` nahradit, výskyty v kapitolách jen vypsat autorovi.
- **Akceptace:** `style_guide.md` projde automatickou kontrolou (struktura, ohrady, sekce 5 a 6 jsou přesnou kopií zdroje).

### A2. Cesty ukotvit k projektu

Zámek `Path(output_path).exists()` je relativní k aktuálnímu adresáři. Při spuštění odjinud tiše selže a kapitola se vygeneruje nebo přepíše jinde. Totéž platí pro `STYLE_GUIDE_PATH`, `AUDIT_REPORT_PATH` a `read_file`.

- Zavést `PROJECT_ROOT` (adresář s `_quarto.yml`) a skládat cesty přes něj.
- **Akceptace:** spuštění z libovolného adresáře dává stejný výsledek, zámek funguje.

### A3. CLI místo komentování kódu

`__main__` se ovládá odkomentováváním bloků (komentář říká: „generování pak zakomentuj").

- `python main.py style [--force]`, `chapter --index N [--force]`, `audit`.
- Bez `--force` zůstává zámek. S `--force` vypsat, co se přepíše, a požádat o potvrzení.
- Přejmenovat kořenový `crew_agents.py` (název koliduje s balíčkem `crew/`), např. na `main.py`.

### A4. OJS doplňovat deterministicky

Dnes projde celá kapitola třemi LLM přepisy (obsah → OJS → recenze).

- `ojs_agent` vrací jen JSON `{"1": "<kód>", ...}`. Python nahradí `// OJS_PLACEHOLDER_SEKCE_N`, zkontroluje, že žádný placeholder nezbyl a počet bloků odpovídá počtu sekcí.
- Recenzent smí vrátit celou kapitolu, ale Python porovná vstup a výstup: počet H2, `{ojs}` bloků, tabsetů a délku (pokles o více než 15 % je chyba). Diff jde do review reportu (A6).

### A5. Výstup do `_drafts/`

Autor už složku `_drafts/` používá (`prubezne_odkladiste.qmd`). Quarto adresáře začínající `_` ignoruje.

- Generovat do `_drafts/<slug>.qmd`, ne přímo do knihy. Autor po kontrole přesune.
- Zámek kontroluje existenci v obou místech a shodu slugu bez číselného prefixu (zachytí `05_diskretni…` vs. `04_prst_diskretni…`).

### A6. Validace a REVIEW NOTES mimo kapitolu

Po zápisu draftu:

- `quarto render <draft> --to html` (subprocess, timeout), stderr do reportu.
- Statické kontroly:
  - žádný `OJS_PLACEHOLDER`,
  - nejvýše 5 obsahových sekcí, každá právě 1 `{ojs}` blok,
  - **žádný název proměnné se neopakuje napříč OJS buňkami kapitoly** (všechny buňky sdílejí jeden globální prostor, duplicita rozbije stránku),
  - žádný `import` v OJS, žádné pevné hex barvy, žádná pevná číselná `width`,
  - v qmd nezůstal `<!-- REVIEW NOTES -->`.
- REVIEW NOTES, diff z A4 a výsledek validace ukládat do `docs_for_agents/review/<slug>.md`. `output_file` v `task_review` odstranit (zápis je dnes dvakrát: CrewAI i ruční `open`).

### A7. Numerické výsledky přes nástroj

Recenzent má ověřit „číselné výsledky jsou správné", ale LLM aritmeticky selhává.

- Přidat nástroj `calc` (krátký Python s numpy a scipy.stats v izolovaném procesu `python -I`, s timeoutem, bez souborů a sítě).
- `content_agent` počítá všechny výsledky (zadání, řešení, self-testy, aplikační úlohy) nástrojem, recenzent je přepočítá.
- Čísla odvozená z dat v textu kapitoly počítat přímo ve stránce přes inline OJS (`${…}`), aby text nemohl nesouhlasit s grafem (viz příloha, nález 1). Ověřit, že syntaxe nekoliduje s `$…$` pro matematiku.
- Zvážit jiný model pro recenzenta než pro autora (nezávislá kontrola). Dnes všichni čtyři agenti sdílejí `gemini-2.5-flash`.

### A8. Sjednotit specifikaci na jednom místě

`prompts.py` a `crew_agents.py` si odporují, a recenzent kontroluje podle té horší verze:

| Téma | `prompts.py` (CHAPTER_STRUCTURE) | `crew_agents.py` (zadání, checklist) |
|---|---|---|
| Školský příklad | tabset Zadání / Postup / Výsledek | tabset Zadání / Řešení |
| AI prompty | 1 na sekci + 3 v závěru | „studentský AI prompt" (1) |
| Aplikační úlohy | 2 až 3 | 2 |
| Barvy v OJS | „CSS proměnné" | „COLORS konstanty" |

- Zdrojem pravdy je `CHAPTER_STRUCTURE` (případně doplněná malým slovníkem počtů). Zadání i checklist recenzenta z něj generovat.
- Ve šabloně jsou ukázky specifické pro rozdělení (Poisson, Bin). Mohou zkreslit jiná témata, nahradit neutrálními zástupci.
- Řádky začínající `#` uvnitř šablony vypadají jako nadpisy H1. Označit je jako pokyn jinou syntaxí.
- **Geometrie je dnes jen volitelná:** v šabloně stojí „Geometrická *nebo* intuitivní interpretace". Kniha se jmenuje „pohledem geometra". Doplnit povinnost geometrického pohledu (těžiště, vzdálenost, projekce, plocha, úhel…) a explicitní výjimku, když pojem geometrii nemá. Vzorem je sekce 8.3 (houpačka s těžištěm).
- Rozhodnout s autorem o emoji v nadpisech (💬, 🏭): SCSS ikony callout skrývá a nahrazuje je emoji, což působí odlišně od „čistého designu".

### A9. Pravidla pro `ojs_agent`

Agent nemá žádné znalosti o specifikách Quarto OJS a nezná vzor z knihy.

- Do zadání doplnit pravidla: proměnné unikátní napříč kapitolou (přípona podle sekce), v buňce se proměnná definuje jako `x = …` (`const`/`let` jen uvnitř bloku `{ … }`, ověřit v dokumentaci), `Inputs`, `Plot` i `d3` jsou dostupné bez `import` (binomická ukázka v `04_prst_diskretni.qmd` importuje `Inputs` ze sítě), responzivní šířka přes vestavěné `width`, barvy ze sdíleného modulu (B2).
- Přidat 2 až 3 ověřené vzorové buňky z vlastních kapitol (slider a sloupcový graf z `04_prst_diskretni.qmd`, houpačka z `04_deskriptivy z tabulky.qmd`), očištěné od pevných barev.

### A10. Audit je zastaralý a nespolehlivý

- `AUDIT_FILES` je napevno a obsahuje neexistující `01_deskriptivní statistiky kvantily.qmd` (dnes `01_typy promennych.qmd`, který v seznamu chybí). `read_file` při chybě vrací text chyby místo výjimky, takže LLM pokračuje bez upozornění.
- `docs_for_agents/audit_report.md` popisuje sekce, které v dnešním souboru nejsou (např. „Aritmetický průměr a těžiště dat"), a cituje větu („Tato sekce definuje kvantily…"), kterou jsem v `04_deskriptivy z tabulky.qmd` nenašel. Navíc doporučuje smazat sekci „Pravděpodobnost průniku jevů", i když vzorec pro závislé jevy není duplicita. `intro.qmd` v knize vůbec není (viz C11), takže nález o chybějícím H2 je bezpředmětný.
- **Zprávu nepředávat jako podklad k úpravám. Po opravě auditu přegenerovat.**
- Seznam souborů číst ze `_quarto.yml`. `read_file` musí při chybě vyvolat výjimku.
- Před LLM spočítat v Pythonu osnovu každé kapitoly (H1, H2, počet OJS bloků, tabsetů, slov) a deterministické nálezy (více než 5 sekcí, chybí OJS, chybí závěr, pevné hex barvy, názvy souborů s diakritikou nebo mezerou). LLM dostane osnovy a posuzuje jen duplicity a návaznosti. Report rozdělit na „deterministické nálezy" a „doporučení" a před ukládáním odříznout úvodní větu LLM.
- `mkdir(parents=True, exist_ok=True)` pro `docs_for_agents/`.

### A11. `crew/tools.py` a `crew/config.py`

- `read_file` čte libovolnou cestu. Omezit na `PROJECT_ROOT` a zakázat `.env` a `.git` (v souladu s AGENTS.md: „never expose API keys").
- Ověřit, že `gemini/gemini-2.5-flash` je stále dostupný (název modelu je jen na jednom místě).

### A12. Drobnosti

- Nepoužitý import `gemini_model` v hlavním skriptu odstranit.
- `context=[předchozí task]` uvést explicitně.
- Validovat povinné klíče v `CHAPTERS` na začátku (dnes `KeyError` až uprostřed běhu).
- Výchozí `aplikacni_oblasti` definovat jednou jako konstantu.

---

## Blok B: Barvy a responzivita

### B1. Inventura barev v OJS

Skutečný stav (agent doplní o zbylé kapitoly): v obou prohlédnutých kapitolách se **nepoužívá `COLORS`** ani modrá `#0085CC` z motivu. Používají se `steelblue`, `#4e79a7`, `#e15759` (Tableau), `#666` a v zakomentovaném kódu `#0275d8`. V knize jsou tak aspoň tři různé modré. Vypsat výsledek inventury, neměnit.

### B2. OJS čte barvy z CSS

- Sdílený modul exportující `COLORS` z `getComputedStyle(document.documentElement)` (`--bs-primary` atd.) a reaktivní `isDark` (MutationObserver na `body`, přes `Generators.observe`), aby se grafy po přepnutí režimu překreslily. Ověřit, jak Quarto v dané verzi označuje tmavý režim.
- **Neumisťovat do `lib/`.** `.gitignore` je zkopírovaná Python šablona, která ignoruje `lib/`, `build/`, `dist/`, `target/` a `*.html`. Použít např. `assets/`. Zvážit i úpravu `.gitignore` (viz C12).
- Cíl: změna palety nevyžaduje přegenerování ani úpravu žádné kapitoly.

### B3. Jeden zdroj pravdy pro paletu

- Quarto ≥ 1.6 (`quarto --version`): `_brand.yml`. Jinak `palette.yml` plus malý skript generující `_palette.scss` a JSON pro OJS.
- Stejnou paletu používá matplotlib/plotly téma (`hag_theme.py`).
- Sémantické role (akcent = „na co se dívat", neutrály = kontext, jedna tlumená kontrastní barva), ne odstíny. Konkrétní barvy navrhnout jako varianty k výběru.

### B4. Responzivita OJS grafů

Grafy mají pevnou šířku (`width: 600` ve dvou grafech v `04_deskriptivy z tabulky.qmd`, jinde výchozích 640). Na telefonu se zmenší spolu s písmem.

- Používat vestavěné `width`, přizpůsobit výšku, větší písmo a okraje, ověřit při šířce 375 px.
- Ovládací prvky (slidery) dostatečně velké pro dotyk, popisky na jednom řádku.

---

## Blok C: SCSS, `_quarto.yml`, logo, názvy souborů

### C1. Struktura SCSS

Pravidla (`.navbar-brand`, `.definition-box`, `h1, h2, h3`, `.highlight-*`, `.callout`) jsou v sekci `scss:defaults`, která má obsahovat jen proměnné. Proto tolik `!important`.

- Přesunout pravidla do `/*-- scss:rules --*/`, `!important` odstraňovat po jednom a ověřovat render.

### C2. Tmavý režim není tmavý

V `_quarto.yml` je `dark: [cosmo, hag_custom.scss]`, tedy totéž co světlé téma. Ve vyrenderovaném `_book` mají `bootstrap-dark-….min.css` a `bootstrap-….min.css` skoro stejnou velikost (500 724 vs. 500 714 B).

- Ověřit v prohlížeči. Pokud potvrzeno, definovat skutečně tmavý základ (tmavý bootswatch nebo vlastní `$body-bg`, `$body-color`).
- V pravidlech nahradit pevné `$light`/`$dark` (`.definition-box`, `.callout-note`, `h3 { color: $dark }`) za `var(--bs-body-bg)`, `var(--bs-body-color)`, `var(--bs-tertiary-bg)` (Bootstrap 5.3, ověřit verzi) a `rgba(0, 133, 204, …)` za odvození z `$primary`.

### C3. Nadpisy

`h1, h2, h3 { color: $primary; border-left: 4px solid; padding-left: 1rem }` je globální, zasáhne callouty, tabsety i boxy a vynucuje workaround `.definition-box h3 { border-left: none }`. Barva nadpisů neutrální, čáru jen u `main h2` nebo zrušit, workaround odstranit.

### C4. Kontrast

`$primary: #0085CC` má na bílé kontrast zhruba 4,0:1, pod 4,5:1 pro běžný text (odkazy, aktivní TOC, `.highlight-term`). Zavést tmavší odstín pro text a odkazy (≥ 4,5:1, ověřit skriptem), podkladové odstíny z něj odvozovat.

### C5. Mrtvý a duplicitní kód v calloutech

`.callout-note` má `border-left-color` dvakrát (`$primary` vs. `$secondary`, vyhrává první kvůli specifičnosti). Pravidla `.callout-*-icon-container { color }` jsou mrtvá (ikona je `display: none`). Prázdné bloky (`&.callout-tip {}`, `&.callout-style-default {}`) smazat.

### C6. Deprecation varování a drobnosti v SCSS

- `darken()`, `lighten()` jsou zastaralé globální funkce Dart Sass. Ověřit varování, nahradit `color.adjust` / `color.scale`.
- `.navbar-brand::before { content: "📊" }` odstranit.
- `.example-box { font-size: 0.9 × }` zrušit (příklady jsou nejčtenější část).
- Definovat font, základ 1,0625 až 1,125 rem, řádkování 1,6 až 1,7 a šířku sloupce (`grid: body-width`). Hodnoty ověřit vizuálně.

### C7. Logo

`Logo.svg` (46 KB, 1024×1024) je plná ilustrace s `fill="#000000"` napevno. V tmavém režimu bude neviditelné a v postranním panelu zabírá zhruba třetinu výšky.

- Pro panel připravit 2 varianty menšího znaku (např. Σ, nebo ořez portrétu) kolem 40 až 56 px ke schválení. Plnou ilustraci použít na úvodní stránce.
- `fill="currentColor"`, nebo samostatná světlá a tmavá varianta (Quarto light/dark logo, ověřit verzi).
- Odstranit Inkscape metadata (např. svgo).

### C8. Názvy souborů

`02_deskriptivní statistiky momenty.qmd`, `03_aritmetika dat.qmd`, `04_deskriptivy z tabulky.qmd`, `01_typy promennych.qmd` mají diakritiku a mezery, ostatní jiné oddělovače (`01-klasicka-prst.qmd` vs. `02_prst_pravidla.qmd`). Navrhnout ASCII `kebab-case`, přejmenovat přes `git mv`, aktualizovat `_quarto.yml`, `chapters.py`, odkazy a style guide a vyrenderovat celý web. Upozornit autora, že staré URL přestanou fungovat.

### C9. `_quarto.yml`

- `date: "12/15/2025"` je napevno a v americkém formátu u české knihy: `date: today` a `date-format`.
- `csl: https://www.zotero.org/styles/apa` načítá styl ze sítě při každém renderu: uložit lokálně (zvážit i český styl).
- `include-after-body: []` je prázdné, odstranit.
- Doplnit pro veřejný web: `site-url`, `repo-url`, favicon, `open-graph`, `twitter-card`.
- `freeze: auto` a commitovat `_freeze/`, aby se při publikování znovu nespouštěl výpočet.

### C10. Soubory mimo knihu

Rozhodnutí autora: **neměnit** (autor si nepamatuje, zda jsou záměrné). `01-pravdepodobnost/intro.qmd`, `00-matematika/index.qmd`, `02-statistika/index.qmd` a `03-datova-veda/index.qmd` nejsou v `chapters`, takže se nerenderují. Agent jen vytvoří `docs_for_agents/otevrene_otazky.md` s podklady (velikost, první řádky, zda je soubor v `chapters`, zda na něj něco odkazuje) a možnostmi: zařadit jako úvody částí (`part: 01-pravdepodobnost/intro.qmd`, `intro.qmd` obsahuje motivační úvod k pravděpodobnosti), nebo přesunout do `_drafts/`. Rozhodne autor.

### C11. `.gitignore`

Je to zkopírovaná Python šablona (Django, Celery, Sphinx, PyInstaller…). Ignoruje i `lib/` a `*.html`, které mohou nechtěně zablokovat vlastní soubory (sdílený JS modul, `include-in-header` HTML). Vyčistit na to, co projekt potřebuje, a ověřit, že `.env` zůstává ignorovaný.

---

## Blok D: Dokumentace

### D1. `HAG_POSTUP.md`

- Překlepy: „Commint to main" → „Commit to main", „Push orogin" → „Push origin".
- Doplnit „Generování kapitol": CLI (A3), kontrola draftu v `_drafts/` a reportu (A6), přesun do knihy, `quarto render`, commit.
- Před `quarto publish gh-pages` vždy `git pull`.

### D2. `docs_for_agents/AGENTS.md`

- Soubor je obecný (styl práce, bezpečnost, Python) a leží v podsložce, kde se při startu relace nenačte (Claude Code čte `AGENTS.md` při startu jen z pracovního adresáře a výše, a jen když neexistuje `CLAUDE.md`). Vytvořit kořenový `CLAUDE.md` (do zhruba 200 řádků), který obsahuje `@docs_for_agents/AGENTS.md` a krátkou sekci „Tento projekt“.
- Toto zadání je jednorázové: **neimportovat ho do `CLAUDE.md`** (načítalo by se do každého požadavku). Uložit jako `docs_for_agents/zadani_revize.md` a odkazovat se na něj jen v zadání úkolu.
- Doplnit sekci „Tento projekt": neměnit existující kapitoly, `_drafts/` jako pracovní místo, ověřovat `quarto render`, nic nepublikovat, vzor OJS buněk (A9), názvy souborů (C8).

### D3. `index.qmd`

Věta „…založená na quarto book stylu s využitím plotly" je zastaralá: grafy jsou Observable Plot (OJS). Opravu udělá autor.

---

## Příloha: věcné nálezy v kapitolách (rozhodne autor, agent NEMĚNÍ)

1. **`04_deskriptivy z tabulky.qmd`: průměr je chybně 7,56 (dvakrát v textu).** Z tabulky vychází Σ xᵢnᵢ = 1473, tedy 1473 / 200 = **7,365**. Graf v téže kapitole správně ukazuje 7,37 (a 7,21 po přidání 5 osob s hodnotou 1).
2. **Stejný soubor, interpolace Q₃:** výpočet „k = 1 + 9·0,75 = 7,75, F(8) < 7,75 < F(9) → Q₃ = 8,75" míchá pořadí hodnot s kumulativní četností. Standardní definice (typ 7) dává pro n = 200 pozici 150,25, a obě sousední pozorování jsou 9, tedy **Q₃ = 9**.
3. **Stejný soubor, nadpis a drobnosti:** sekce „Kvantilové ukazatele variability" obsahuje výklad váženého průměru (IQR tam není), v textu Q₁ je „menší než 0.5" místo 0,25, „budeme mt data".
4. **`04_prst_diskretni.qmd`, Excel:** `=NEGBINOM.DIST(1; x; p)` má být `=NEGBINOM.DIST(x; 1; p; NE)` (funkce bere počet neúspěchů, počet úspěchů, pravděpodobnost, kumulativní příznak).
5. **`04_prst_diskretni.qmd`, geometrické rozdělení:** vzorec p(x) = π(1−π)ˣ počítá neúspěchy před prvním úspěchem (souhlasí s poznámkou k Excelu), ale graf používá (1−p)^(k−1)·p pro počet pokusů. Sjednotit definici.
6. **`04_prst_diskretni.qmd`, Poisson:** osa y je napevno `[0; 0,5]`, takže pro λ ≲ 0,7 se sloupce ořezávají (P(0) je až 0,9). Graf končí na k = 20, takže pro λ = 20 chybí zhruba 44 % pravděpodobnosti.
