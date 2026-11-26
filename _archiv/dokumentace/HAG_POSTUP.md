# Jak dělat Quarto projekt na GitHub Pages (Manuál)

## Prvotní nastavení (pouze jednou)
- Založit adresář pro repozitáře: Lokálně na rychlém disku, úplně mimo síťové disky a synchronizační služby jako OwnCloud/OneDrive (např. D:\___GitHub_repos\).
- Stáhnout a nainstalovat: GitHub Desktop (GHD) a Quarto CLI.
- GHD přihlášení: Přihlásit se přes tvůj GitHub účet (nikoliv Google účet – GitHub sice umožňuje registraci přes Google, ale účet jako takový je samostatná identita na GitHub.com).

## Vytvoření NOVÉHO projektu (na zelené louce)
- V GitHub Desktop: File -> New repository.
- Name: Název složky (bez diakritiky, ideálně s podtržítky nebo pomlčkami)
- Local path: Vybrat tvůj adresář (např. D:\___GitHub_repos\)
- Git Ignore: Zvolit Python (GHD automaticky vytvoří soubor .gitignore, který zajistí, že se na web nebudou posílat pomocné systémové soubory). Šablonu pak zkrátit na to, co projekt potřebuje (viz `.gitignore` v tomto projektu): plná Python šablona ignoruje i `lib/` a `*.html`, což může zablokovat vlastní soubory.
- Kliknout na Create repository.
- V GHD kliknout na Publish repository (tím se prázdný projekt založí i na webu GitHubu).

## Stáhnout EXISTUJÍCÍ projekt na čistý počítač (pouze jednou)
- V GHD: File -> Clone repository
- local path: Ověřit, že se stahuje do tvé bezpečné složky (mimo OwnCloud).
- Pro generátor kapitol (jen pokud ho budeš na tom počítači používat): vytvořit `.venv`
  (postup je v komentáři v `crew/config.py`) a soubor `.env` s `ANTHROPIC_API_KEY=...`. `.env` se nikdy necommituje.

## Běžná práce na počítači (Workflow)
- v GHD klik na **Fetch origin** = kontrola aktuální verze projektu na githubu a v počítači
- pokud zjistí změny, pak **Pull origin** = stáhne aktuální verzi
- pracuju lokálně ve VScode
- náhled: v terminálu `quarto preview`; před commitem celý web `quarto render` (nesmí hlásit chyby ani varování)
- v GHD stručně popsat změny
- GHD **Commit to main** = připraví soubor k odeslání, zamrazí aktuální stav
- GHD **Push origin** pošle data na web.

## Generování nové kapitoly (agent)
Kapitola se nikdy nepíše přímo do knihy, vzniká nejdřív v `_drafts/`.
1. Do `chapters.py` přidat položku podle vzoru (téma, cílový soubor, klíčové pojmy, zaměření úloh, nástroje).
2. Seznam a stav: `.venv\Scripts\python.exe main.py chapter`
3. Generování: `.venv\Scripts\python.exe main.py chapter --index N`
   (autor → OJS → recenzent; volá placený API Claude, cena závisí na délce kapitoly).
   Existující kapitolu ani draft program nepřepíše; draft přepíše jen s `--force` a po potvrzení.
4. Zkontrolovat výsledek:
   - `_drafts/<název>.qmd` (text kapitoly),
   - `docs_for_agents/review/<slug>.md` (report: výsledek kontrol, REVIEW NOTES recenzenta, diff, výsledek kontrolního renderu).
5. Nálezy v reportu opravit ručně, čísla v textu ověřit (agenti je počítají nástrojem, ale poslední slovo je autorovo).
6. Soubor přesunout do kapitoly knihy (správná složka, ASCII `kebab-case` název bez diakritiky a mezer) a přidat do `_quarto.yml`.
7. `quarto render` (bez chyb a varování), commit.

Další příkazy: `main.py style` (kontrola style guide, `--force` přegeneruje), `main.py audit` (audit kapitol, výsledek v
`docs_for_agents/audit_report.md`). Po úpravě SCSS nebo `_quarto.yml` stačí obnovit style guide bez LLM:
`.venv\Scripts\python.exe -m crew.style_guide --refresh`.

## Publikování na GitHub Pages
- Před publikací vždy: **Fetch/Pull origin** (nebo v terminálu `git pull`), aby se nepublikovala starší verze, a `quarto render` bez chyb.
- Všechno commitnout a pushnout.
- ve VSCode terminal příkazem **quarto publish gh-pages**
- Poprvé se vytvoří větev `gh-pages`; v GitHubu v Settings → Pages ověřit, že zdrojem je větev `gh-pages`.
- Adresa webu: `https://<uživatel>.github.io/<název repozitáře>/` (u zdarma účtu musí být repozitář veřejný).
- Po přejmenování souborů kapitol přestanou fungovat staré odkazy (adresy URL).
