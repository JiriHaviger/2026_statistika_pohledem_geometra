# Audit kapitol

Vygenerováno: 2026-11-07. Seznam kapitol je z `_quarto.yml`, obsah kapitol se nezměnil. Zprávu **nepředávat agentům jako podklad k úpravám**, slouží autorovi k rozhodnutí.

## Osnova (spočítáno Pythonem)

| Soubor | Sekcí | OJS | Tabsetů | Slov |
|---|---|---|---|---|
| `01-pravdepodobnost/01-klasicka-prst.qmd` | 4 | 1 | 0 | 1028 |
| `01-pravdepodobnost/02-prst-pravidla.qmd` | 5 | 0 | 0 | 1052 |
| `01-pravdepodobnost/03-prst-distribuce.qmd` | 1 | 6 | 0 | 1389 |
| `01-pravdepodobnost/04-prst-diskretni.qmd` | 4 | 4 | 0 | 1309 |
| `02-statistika/01-typy-promennych.qmd` | 9 | 8 | 0 | 3688 |
| `02-statistika/02-deskriptivni-statistiky-momenty.qmd` | 4 | 7 | 0 | 3342 |
| `02-statistika/03-aritmetika-dat.qmd` | 2 | 1 | 0 | 837 |
| `02-statistika/04-deskriptivy-z-tabulky.qmd` | 3 | 5 | 0 | 1013 |
| `02-statistika/05-analyza-rozptylu-geometricky.qmd` | 1 | 4 | 1 | 1157 |

## Deterministické nálezy

- `01-pravdepodobnost/01-klasicka-prst.qmd`: pevné barvy v OJS ['#0085CC', '#357ab0'].
- `01-pravdepodobnost/02-prst-pravidla.qmd`: žádný OJS blok (chybí interaktivní vizualizace).
- `01-pravdepodobnost/02-prst-pravidla.qmd`: chybí závěr nebo shrnutí (H2 se slovem „závěr“, „shrnutí“ nebo „poznatky“).
- `01-pravdepodobnost/03-prst-distribuce.qmd`: chybí závěr nebo shrnutí (H2 se slovem „závěr“, „shrnutí“ nebo „poznatky“).
- `01-pravdepodobnost/04-prst-diskretni.qmd`: chybí závěr nebo shrnutí (H2 se slovem „závěr“, „shrnutí“ nebo „poznatky“).
- `02-statistika/01-typy-promennych.qmd`: název souboru obsahuje diakritiku nebo mezeru.
- `02-statistika/01-typy-promennych.qmd`: 9 obsahových sekcí (doporučené maximum 5).
- `02-statistika/01-typy-promennych.qmd`: pevné barvy v OJS ['#ccc'].
- `02-statistika/02-deskriptivni-statistiky-momenty.qmd`: název souboru obsahuje diakritiku nebo mezeru.
- `02-statistika/02-deskriptivni-statistiky-momenty.qmd`: pevné barvy v OJS ['#333', '#666', '#7A5B8C', '#AF3363', '#ccc', '#f0f0f0'].
- `02-statistika/03-aritmetika-dat.qmd`: název souboru obsahuje diakritiku nebo mezeru.
- `02-statistika/03-aritmetika-dat.qmd`: chybí závěr nebo shrnutí (H2 se slovem „závěr“, „shrnutí“ nebo „poznatky“).
- `02-statistika/04-deskriptivy-z-tabulky.qmd`: název souboru obsahuje diakritiku nebo mezeru.
- `02-statistika/04-deskriptivy-z-tabulky.qmd`: chybí závěr nebo shrnutí (H2 se slovem „závěr“, „shrnutí“ nebo „poznatky“).
- `02-statistika/04-deskriptivy-z-tabulky.qmd`: pevné barvy v OJS ['#4e79a7', '#666', '#e15759'].
- `02-statistika/05-analyza-rozptylu-geometricky.qmd`: chybí závěr nebo shrnutí (H2 se slovem „závěr“, „shrnutí“ nebo „poznatky“).
- `02-statistika/05-analyza-rozptylu-geometricky.qmd`: pevné barvy v OJS ['#444', '#666', '#bbb'].
- `01-pravdepodobnost/intro.qmd` není v `_quarto.yml` (kniha ho nevykreslí).
- `02-statistika/index.qmd` není v `_quarto.yml` (kniha ho nevykreslí).

## Doporučení (LLM, posuzuje jen duplicity a návaznosti podle osnov)

## Duplicity

- **`02-statistika/01-typy-promennych.qmd` (H1 „Deskriptivní statistiky“) × `02-statistika/02-deskriptivni-statistiky-momenty.qmd` × `02-statistika/04-deskriptivy-z-tabulky.qmd`:** Z nadpisů plyne možné překrývání u polohy a variability.
  - Soubor 01 má „Střední hodnota založená na uspořádání“, „Kvantily - další míry založené na uspořádání“ a „Míry variabiliy odvozená z kvantilů“.
  - Soubor 04 má „Ukazatele polohy: kvantily z tabulky četností“ a „Kvantilové ukazatele variability: z tabulky četností“.
  - Soubor 02 má „Momentová míra polohy“ a „Momentové míry variability“, soubor 04 pak „variabilita odvozená z průměru“.
  - Z osnov nepoznám, zda jde o duplicitu obsahu, nebo o záměrné rozlišení „z jednotlivých hodnot“ a „z tabulky“. Jistá je jen tematická blízkost nadpisů.
- **`02-statistika/01-typy-promennych.qmd` – „Deskriptivní statistiky obecně“ × H1 téhož souboru „Deskriptivní statistiky“:** Úvodní sekce nese téměř stejný název jako celá kapitola. Obsah neznám, takže nevím, zda se v ní opakuje úvod.
- **`01-pravdepodobnost/01-klasicka-prst.qmd` – „Klasický školský přístup“ × `01-pravdepodobnost/02-prst-pravidla.qmd` – „základní pojmy“:** Obě sekce zřejmě zavádějí základní pojmy pravděpodobnosti (klasická definice, jev, výsledek). Překryv je možný, ale z nadpisů ho nelze potvrdit.
- **`01-pravdepodobnost/01-klasicka-prst.qmd` – „Bernouli vs Laplace - dva přístupy k pravděpodobnosti“ × „Klasický školský přístup“ a „Zákon velkých čísel“:** V jedné kapitole se pravděpodobně třikrát probírá rozdíl mezi teoretickým a experimentálním přístupem. Rozsah překryvu z osnovy nepoznám.

## Návaznosti

- **Pořadí v `01-pravdepodobnost`:**
  - Kapitola 01 („Zákon velkých čísel“, „Bernouli vs Laplace“) předchází kapitole 02 se „základními pojmy“. Pojmy jako jev nebo pravděpodobnost se tedy zřejmě používají dřív, než jsou formálně zavedeny. Pokud je kapitola 01 záměrně motivační úvod, osnova to nezachycuje.
  - V kapitole 03 („Co je pravděpodobnostní rozdělení?“) navazuje rozdělení na výsledky a jevy z kapitol 01 a 02. Náhodná veličina ani rozdělení se v nadpisech kapitol 01 a 02 nevyskytují. Není tedy vidět, kde se pojem „náhodná veličina“ zavádí. Může to být uvnitř kapitoly 03.
  - V kapitole 04 se používají podmíněná pravděpodobnost a nezávislost z kapitoly 02 (u hypergeometrického rozdělení pravděpodobně i kombinatorika). Kombinatorika ani kombinační čísla nejsou v žádném nadpisu. Nejistota: může být zavedena uvnitř textu.
- **Rozpor mezi pořadím `01-pravdepodobnost` a `02-statistika`:** Kapitola `02-statistika/01-typy-promennych.qmd` má H1 „Deskriptivní statistiky“, ale obsahuje i sekci „Proměnná“ (typy proměnných). Chybí tedy samostatný úvod do typů dat a H1 neodpovídá názvu souboru („typy proměnných“). Plyne z toho nejasná struktura: pojem „proměnná“ se zavádí až uvnitř kapitoly s jiným H1.
- **Pořadí v `02-statistika`:**
  - Kapitola 02 („Momentové statistiky“) a kapitola 04 („z tabulky dat“) pracují s průměrem. Průměr se zřejmě zavádí až v kapitole 02 („Momentová míra polohy“), přitom kapitola 01 už zmiňuje „Střední hodnotu založenou na uspořádání“. Pojem „střední hodnota“ se tak objevuje dřív a v jiném smyslu než průměr. Návaznost na průměr z osnovy není vidět.
  - Kapitola 03 („Vlastnosti metrik a aritmetika dat“, „Transformace dat“) předpokládá znalost metrik (průměr, rozptyl, kvantily) z kapitol 01–02, pořadí je tedy v pořádku. Pojem „metrika“ se v předchozích osnovách nevyskytuje, zavádí se zřejmě až zde.
  - Kapitola 05 („Rozklad rozptylu geometricky“) předpokládá rozptyl z kapitoly 02. Mezi 02 a 05 je však kapitola 04 s „variabilitou odvozenou z průměru“. Není jasné, zda by 05 nemělo následovat bezprostředně po 02.
- **Propojení pravděpodobnosti a statistiky:** Osnovy neobsahují žádnou sekci, která by navázala `02-statistika` na rozdělení z `01-pravdepodobnost`. Střední hodnota a rozptyl náhodné veličiny jako teoretické protějšky momentových statistik se z nadpisů nevyčtou. Nelze říct, zda se řeší jinde.
- **Nekonzistence pojmenování a číslování:** Soubor `01-pravdepodobnost/01-klasicka-prst.qmd` používá pomlčky, ostatní podtržítka. Čistě podle osnov to může být i záměr a nevím, zda to ovlivňuje pořadí v knize.

## Doporučení

1. **Překryv „klasický přístup“ × „základní pojmy“:** Porovnat sekce „Klasický školský přístup“ (01) a „základní pojmy“ (02). Případné duplicitní definice ponechat na jednom místě a na druhé dát odkaz.
2. **Tři sekce o přístupech k pravděpodobnosti v kapitole 01:** Ověřit, zda „Klasický školský přístup“, „Zákon velkých čísel“ a „Bernouli vs Laplace“ neříkají totéž. Pokud ano, sloučit „Bernouli vs Laplace“ do ostatních dvou. Pokud ne, doplnit do nadpisu, co sekce přidává.
3. **Pořadí 01 → 02:** Do úvodu kapitoly 01 doplnit předběžné vysvětlení nebo odkaz „pojmy viz kapitola 02“. Alternativně prohodit pořadí, pokud kapitola 01 skutečně používá pojmy z 02. Rozhodnutí závisí na obsahu, který z osnov nevidím.
4. **Náhodná veličina a rozdělení (03):** Zkontrolovat, zda se „náhodná veličina“ zavádí v kapitole 03. Pokud ne, doplnit definici před první použití. Jediná H2 sekce „Co je pravděpodobnostní rozdělení?“ nevypovídá o struktuře, proto kapitolu rozdělit na podsekce (H2) podle témat.
5. **Kombinatorika v kapitole 04:** Ověřit, zda je kombinační číslo definováno před „Binomické rozdělení“ a „Hypergeometrické rozdělení“. Pokud ne, doplnit krátkou definici nebo odkaz do kapitoly 02.
6. **Kapitola `02-statistika/01-typy-promennych.qmd`:**
   - Sjednotit H1 „Deskriptivní statistiky“ s názvem souboru. Buď přejmenovat H1 na „Typy proměnných a základní deskriptivní statistiky“, nebo oddělit sekci „Proměnná“ do vlastní kapitoly.
   - Jelikož má kapitola 3688 slov a 9 sekcí, rozdělit ji například mezi sekce o četnostech a sekce o uspořádání/kvantilech. Dělicí bod je vidět v nadpisech.
   - Sekce „Kvantily – další míry…“ má `{.unnumbered .unlisted}`, což je u věcného obsahu nekonzistentní s ostatními sekcemi. Zvážit, zda nemá být číslovaná a uvedená v obsahu.
7. **Duplicita deskriptivních statistik (01 × 04):** Do úvodu kapitoly 04 doplnit odkaz na odpovídající sekce v kapitole 01 a ověřit, že se definice kvantilů neopakují. Pokud ano, zredukovat je v 04 na použití vzorců pro tabulku.
8. **Střední hodnota × průměr (01 × 02):** V sekci „Střední hodnota založená na uspořádání“ (01) vysvětlit, že jde o medián, nebo uvést odkaz na kapitolu 02. Z osnovy nelze poznat, zda už se tak děje. Sjednotit terminologii „střední hodnota“ a „průměr“.
9. **Pořadí kapitol 04 a 05:** Ověřit, zda 05 nevyžaduje nic z 04. Pokud ne, přesunout 05 hned za 02, případně do úvodu 05 doplnit explicitní odkaz na rozptyl z 02.
10. **Pojem „metrika“ (03):** Zavést „metriku“ na začátku sekce „Aritmetika dat“ jednou větou nebo odkazem. V předchozích osnovách se pojem nevyskytuje.
11. **Propojení pravděpodobnosti a statistiky:** Doplnit na konec `01-pravdepodobnost` nebo na začátek `02-statistika` sekci o vztahu teoretických a výběrových charakteristik. Pokud tato návaznost existuje v textu, ověřit a případně uvést explicitní odkaz.
12. **Kapitola 05:** Jediná H2 „Postup vizualizace“ neodpovídá H1 „Rozklad rozptylu geometricky“. Rozdělit kapitolu na H2 sekce, například zadání, geometrická konstrukce a interpretace. Přesný obsah neznám, rozdělení tedy musí navrhnout autor podle textu.
