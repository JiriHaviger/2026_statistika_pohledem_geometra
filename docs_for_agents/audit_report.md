Následuje auditní zpráva se zjištěnými nálezy a doporučeními.

---

# Auditní report kapitol

## 1. Duplicity

### 1.1 Duplicita v definici typů proměnných
**Popis:** Sekce definující a kategorizující typy proměnných (nominální, ordinální, diskrétní kardinální, spojitá kardinální, kvalitativní vs. kvantitativní, intervalové vs. poměrové škály) se objevuje ve dvou kapitolách s podobným rozsahem detailů.
**Soubory a sekce:**
*   `01-pravdepodobnost/03_prst_distribuce.qmd` – Sekce: **Od kategorií k číslům**
*   `02-statistika/01_deskriptivní statistiky kvantily.qmd` – Sekce: **Proměnná**
**Co přesně se opakuje:** Definice a podrobná kategorizace proměnných, včetně tabulek shrnujících typy proměnných, co lze určit, příklady a relevantní statistiky. Ačkoliv se v kapitole o pravděpodobnosti zmiňuje v kontextu osy x grafu rozdělení, rozsah detailů je nadbytečný, když existuje dedikovaná sekce ve statistice.

### 1.2 Duplicita v pravděpodobnosti průniku jevů
**Popis:** Sekce o pravděpodobnosti průniku jevů opakuje vzorce a koncepty již zmíněné nebo snadno odvoditelné z předchozích sekcí o podmíněné pravděpodobnosti a nezávislosti jevů.
**Soubor a sekce:**
*   `01-pravdepodobnost/02_prst_pravidla.qmd` – Sekce: **nezávislost jevů** a **Pravděpodobnost průniku jevů**
**Co přesně se opakuje:** V sekci "nezávislost jevů" je uvedena definice $P(A \cap B) = P(A) \cdot P(B)$ pro nezávislé jevy. Sekce "Pravděpodobnost průniku jevů" následně opakuje tento vzorec a vzorec $P(A \cap B) = P(A) \cdot P(B|A)$ pro závislé jevy, který je přímým důsledkem definice podmíněné pravděpodobnosti. Obsah druhé sekce by mohl být integrován do předchozích.

### 1.3 Konceptuální duplicity při výpočtu deskriptivních statistik z tabulky
**Popis:** Kapitola věnovaná výpočtu deskriptivních statistik z tabulky četností znovu definuje pojmy jako kvantily, rozpětí, IQR, aritmetický průměr a rozptyl, ačkoliv tyto definice byly detailně uvedeny v předchozích kapitolách o deskriptivních statistikách.
**Soubor a sekce:**
*   `02-statistika/04_deskriptivy z tabulky.qmd` – Sekce: **Ukazatele polohy: kvantily**, **Kvantilové ukazatele variability**, **Aritmetický průměr a těžiště dat**, **variabilita odvozená z průměru**
**Co přesně se opakuje:** Úvodní odstavce každé z těchto sekcí znovu definují statistiky namísto toho, aby se přímo zaměřily na jejich výpočet z tabulky četností s předpokladem znalosti definic. Například: "Tato sekce definuje kvantily..." místo "Tato sekce popisuje výpočet kvantilů z tabulky četností...".

## 2. Nesoulad názvu souboru s obsahem

### 2.1 Nesoulad v názvu souboru a H1 pro deskriptivní statistiky
**Popis:** Název souboru `02-statistika/01_deskriptivní statistiky kvantily.qmd` naznačuje zaměření na kvantily, zatímco hlavní nadpis H1 je "Deskriptivní statistiky", což je velmi obecné. Obsah souboru skutečně zahrnuje širší spektrum deskriptivních statistik (typy proměnných, modus, grafy) a nejen kvantily.
**Soubor:** `02-statistika/01_deskriptivní statistiky kvantily.qmd`
**H1 nadpis:** Deskriptivní statistiky
**Navrhovaný lepší název souboru:** `02-statistika/01_deskriptivni_stat_cetnosti_kvantily.qmd` nebo `02-statistika/01_zakladni_deskriptivni_stat.qmd`
**Důvod:** Nový název lépe reflektuje, že se kapitola zabývá jak statistikami založenými na četnostech (modus), tak na uspořádání (kvantily), a zároveň ji odlišuje od následující kapitoly o momentových statistikách.

## 3. Chybějící nebo neúplné části

### 3.1 Chybějící H2 nadpis v úvodní kapitole
**Popis:** Úvodní kapitola `01-pravdepodobnost/intro.qmd` obsahuje úvodní text k pravděpodobnosti, ale tento text není zařazen pod žádný H2 nadpis. Je popsán jako "Obsah" v přehledu, což není skutečný nadpis v souboru.
**Soubor:** `01-pravdepodobnost/intro.qmd`
**Chybějící část:** Konkrétní H2 nadpis pro hlavní obsah kapitoly.

## 4. Doporučení

### 4.1 Doporučení pro duplicitu typů proměnných
*   **Akce:** Přesunout / Konsolidovat obsah.
*   **Konkrétní akce:** Ponechat detailní definice a kategorizace typů proměnných pouze v `02-statistika/01_deskriptivní statistiky kvantily.qmd` v sekci "Proměnná". V kapitole `01-pravdepodobnost/03_prst_distribuce.qmd` v sekci "Od kategorií k číslům" zkrátit obsah na velmi stručné shrnutí relevantní pro pravděpodobnostní rozdělení a odkázat čtenáře na podrobnější vysvětlení v kapitole `02-statistika/01_deskriptivní statistiky kvantily.qmd`.

### 4.2 Doporučení pro duplicitu v pravděpodobnosti průniku jevů
*   **Akce:** Smazat / Přesunout / Integrovat.
*   **Konkrétní akce:** Smazat sekci "Pravděpodobnost průniku jevů" v souboru `01-pravdepodobnost/02_prst_pravidla.qmd`. Vzorce pro průnik jevů (pro nezávislé i závislé) by měly být integrovány do sekce "nezávislost jevů" a/nebo do sekce "podmíněná pravděpodobnost" jako logické důsledky jejich definic.

### 4.3 Doporučení pro konceptuální duplicity v deskriptivních statistikách z tabulky
*   **Akce:** Přepracovat úvodní odstavce.
*   **Konkrétní akce:** V souboru `02-statistika/04_deskriptivy z tabulky.qmd` přepracovat úvodní odstavce sekcí "Ukazatele polohy: kvantily", "Kvantilové ukazatele variability", "Aritmetický průměr a těžiště dat" a "variabilita odvozená z průměru". Namísto redefinování statistik explicitně uvést, že kapitola se zaměřuje na *výpočet těchto již definovaných statistik z tabulky četností*. Příklad: "Pro výpočet kvantilů z tabulky četností se používá kumulativní relativní četnost..."

### 4.4 Doporučení pro nesoulad názvu souboru s obsahem (deskriptivní statistiky)
*   **Akce:** Přejmenovat soubor.
*   **Konkrétní akce:** Přejmenovat soubor `02-statistika/01_deskriptivní statistiky kvantily.qmd` na `02-statistika/01_deskriptivni_stat_cetnosti_kvantily.qmd` nebo `02-statistika/01_zakladni_deskriptivni_stat.qmd`.

### 4.5 Doporučení pro chybějící H2 nadpis v úvodní kapitole
*   **Akce:** Doplnit H2 nadpis.
*   **Konkrétní akce:** V souboru `01-pravdepodobnost/intro.qmd` přidat H2 nadpis nad hlavní obsah kapitoly, například `## Úvod do pravděpodobnosti a její aplikace` nebo `## Kde se setkáváme s pravděpodobností v reálném světě`.