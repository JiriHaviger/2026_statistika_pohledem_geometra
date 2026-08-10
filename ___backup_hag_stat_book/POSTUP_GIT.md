# 📘 Manuál pro aktualizaci webu (hag-stat)

Tento postup použij pokaždé, když v Codespaces upravíš soubory a chceš, aby se změny projevily na tvém webu.

---

## 1️⃣ Vygenerování webu (Render)
Quarto musí tvoje `.qmd` soubory převést na HTML. V terminálu Codespaces spusť:

```bash
# 1. Přejdi do složky s knihou
cd hag-stat-book

# 2. Vygeneruj HTML verzi (vytvoří soubory do ../docs)
quarto render --to html

# 3. Vrať se zpět do hlavního adresáře
cd ..

# Přidej všechny změny do balíčku
git add .

# Vytvoř potvrzení s popisem toho, co jsi změnil
git commit -m "aktualizace obsahu a re-render webu"

# Pošli změny na GitHub
git push origin main

# 3. Kontrola nasazení (Actions)
Web se neaktualizuje okamžitě. Musíš chvíli počkat: 
Otevři svůj repozitář na GitHubu v prohlížeči.
Klikni na záložku Actions (v horní liště).
Sleduj řádek pages build and deployment:
🟡 Žlutá tečka: GitHub právě staví tvůj web.
✅ Zelená fajfka: Hotovo, web je aktualizovaný.
❌ Červený křížek: Někde nastala chyba (zkontroluj logy).

$ 4. Zobrazení změn na webu
Otevři: https://jirihaviger.github.io/hag-stat/

[!IMPORTANT] Pokud změny nevidíš, i když v Actions svítí zelená: Tvůj prohlížeč má uloženou starou verzi v paměti (cache). Stiskni klávesovou zkratku **CTRL + F5** (vynucené obnovení)

🛠️ Jednorázová kontrola nastavení (když to nefunguje)
Pokud se web neaktualizuje vůbec, zkontroluj tyto tři věci:

Settings -> Pages: Branch je nastavena na main a složka na /docs.

.gitignore: Nesmí obsahovat řádek docs (jinak se soubory neodešlou).

_quarto.yml: Musí mít v sekci project nastaveno output-dir: ../docs.