# Jak dělat Quarto projekt na GitHub Pages (Manuál)

## Prvotní nastavení (pouze jednou)
- Založit adresář pro repozitáře: Lokálně na rychlém disku, úplně mimo síťové disky a synchronizační služby jako OwnCloud/OneDrive (např. D:\___GitHub_repos\).
- Stáhnout a nainstalovat: GitHub Desktop (GHD) a Quarto CLI.
- GHD přihlášení: Přihlásit se přes tvůj GitHub účet (nikoliv Google účet – GitHub sice umožňuje registraci přes Google, ale účet jako takový je samostatná identita na GitHub.com).

## Vytvoření NOVÉHO projektu (na zelené louce)
- V GitHub Desktop: File -> New repository.
- Name: Název složky (bez diakritiky, ideálně s podtržítky nebo pomlčkami)
- Local path: Vybrat tvůj adresář (např. D:\___GitHub_repos\)
- Git Ignore: Zvolit Python (GHD automaticky vytvoří soubor .gitignore, který zajistí, že se na web nebudou posílat pomocné systémové soubory).
- Kliknout na Create repository.
- V GHD kliknout na Publish repository (tím se prázdný projekt založí i na webu GitHubu).

## Stáhnout EXISTUJÍCÍ projekt na čistý počítač (pouze jednou)
- V GHD: File -> Clone repository
- local path: Ověřit, že se stahuje do tvé bezpečné složky (mimo OwnCloud).


### Běžná práce na počítači (Workflow) 
- v GHD klik na **Fetch origin** = kontrola aktuální verze projektu na githubu a v počítači
- pokud zjistí změny, pak **Pull origin** = stáhne aktuální verzi
- pracuju lokálně ve VScode
- v GHD stručně popsat změny
- GHD **Commint to main** = připraví soubor k odeslání, zamrazí aktuální stav
- GHD **Push orogin** pošle data na web. 

### Publikování na git pages
- ve VSCode terminal příkazem **quarto publish gh-pages**


