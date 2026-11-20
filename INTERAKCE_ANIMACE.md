# Interakce a animace v kapitolách

Stav ke commitu `8385f17`. Návrhy nejsou implementované, jde o podklad k výběru.

Legenda: ✅ interakce v kapitole je, ◐ je jen částečná (tabulka, rozbalovací řešení, záložky), ❌ chybí.

## Technické poznámky k animacím

- **OJS generátor** stačí na většinu: buňka s `{ while (true) { yield ...; await Promises.delay(40); } }` překresluje graf, `Plot` se dá vracet při každém kroku.
  Pro stovky až tisíce bodů (padající body, simulace) je lepší `<canvas>` v `html` buňce, SVG by bylo pomalé.
- **Ovládání:** každá animace má tlačítko Start/Pauza a Znovu. Při `prefers-reduced-motion` se nespouští sama.
- **Barvy** jen z `C.*` (`assets/jhrules.js`), akcent na jednu věc na obrázek. Šířka z `width`.
- **Společné prvky:** přidat do `assets/jhrules.js` pomocné funkce (např. `fallingPoints`, `arrow`), aby se nekopírovaly mezi kapitolami.
- Statické geometrické obrázky (vektory, projekce) lze kreslit v `Plot` pomocí `Plot.arrow`, `Plot.vector`, `Plot.link`; tažení bodů myší vyžaduje buňku s `d3.drag` nad SVG.

---

## Část Pravděpodobnost

### 1. Klasická pravděpodobnost (`01-klasicka-prst.qmd`)

| | |
|---|---|
| **Interakce** | ✅ tlačítka +1 / +10 / +100 hodů a Reset, posuvník tolerance ε. Simulace hodů s konvergencí relativní četnosti (zákon velkých čísel). |
| **Návrh doplnění** | Přepínač mince / kostka / „nespravedlivá“ mince s nastavitelnou π, aby student viděl, že konverguje k jiné hodnotě. |
| **Animace** | **Padající body do pásu ε.** Každý hod je bod, který padá do sloupce Panna / Orel. Okolo teoretické hodnoty je vyznačený pruh ±ε a body se v něm hromadí. Zároveň se vykresluje trajektorie relativní četnosti, která se zužuje do trychtýře `±1/√n`. Obě části se hýbou současně. |

### 2. Pravidla a vzorce (`02-prst-pravidla.qmd`)

| | |
|---|---|
| **Interakce** | ❌ žádná. |
| **Návrh interakce** | **Vennův diagram s posuvníky.** Dvě kružnice (jevy A a B) v jednotkovém čtverci. Posuvníky pro P(A), P(B) a překryv P(A∩B). Vedle se průběžně počítá P(A∪B), P(A\|B), P(B\|A) a ukazuje se, zda jsou jevy nezávislé (P(A∩B) = P(A)·P(B)). Plocha je pravděpodobnost, takže všechny vzorce jsou vidět jako poměry ploch. |
| **Animace** | **Podmíněná pravděpodobnost jako výběr části (styl Seeing Theory).** Do plochy padají náhodné body a stejnou plochou jsou vyznačené tři obdélníkové pruhy A, B, C, které se částečně překrývají. Tlačítka **Celek / A / B / C** určují, co je „vesmír“. Při volbě Celek se počítá podíl bodů, které dopadly do A, B, C, vůči všem bodům. Při volbě např. B se body mimo B zešednou, přestanou se počítat a čitatel i jmenovatel se vztahují jen k B (P(A\|B) = bodů v A∩B / bodů v B). Sloupcový graf pod plochou ukazuje živé odhady P(A), P(B), P(C), resp. po výběru P(·\|B), a čárkou teoretickou hodnotu. Čítač „v části / celkem“ je vždy vidět a po stovkách bodů se podíl ustálí. Pruhy lze přetahovat (překryv A∩B se mění), student tak vidí, kdy jsou jevy nezávislé. Nejde o přesnou kopii předlohy, jen o stejný princip: padající body, přepínač celek/část a počet zásahů proti počtu všech. |

### 3a. Typy proměnných (`031-typy-promennych.qmd`)

| | |
|---|---|
| **Interakce** | ◐ cvičení „Zařaďte“ s rozbalovacím řešením, ostatní grafy statické. |
| **Návrh interakce** | **Třídění karet.** Karty s příklady (barva očí, teplota, pořadí v cíli, počet dětí) se přetahují do čtyř košů (nominální, ordinální, intervalová, poměrová), po puštění se ukáže, jaké operace koš dovoluje. Nahradí rozbalovací řešení. Alternativa bez tažení: výběr typu z `Inputs.select` u každé položky s okamžitou zpětnou vazbou. |
| **Animace** | **Měřítko se „zpřesňuje“.** Jedna a ta samá veličina (např. výška) se postupně převádí z nominální (jen kategorie) přes ordinální (pořadí) na intervalovou a poměrovou. Body se přeskupují na osu a objevují se další smysluplné operace (rovnost, pořadí, rozdíl, podíl). |

### 3b. Rozdělení diskrétní veličiny (`032-rozdeleni-diskretni-veliciny.qmd`)

| | |
|---|---|
| **Interakce** | ✅ posuvník bodu t u distribuční funkce (CDF), akcentní bod se pohybuje. |
| **Návrh doplnění** | Přepínač kostky (spravedlivá, falešná, dvě kostky – součet) a ruční úprava výšek sloupců PMF s kontrolou součtu 1. |
| **Animace** | **Od PMF k CDF.** Sloupce PMF se jeden po druhém „stohují“ a vytvářejí schodovitou CDF. Pak se z hodů simuluje empirická CDF, která se přilepí k teoretické. |

### 4. Typická diskrétní rozdělení (`04-prst-diskretni.qmd`)

| | |
|---|---|
| **Interakce** | ✅ nejbohatší kapitola: binomické (n, π), geometrické (π), hypergeometrické (N, M, n), Poissonovo (λ). |
| **Návrh doplnění** | Tlačítko „Vylosuj jednu hodnotu“ u každého rozdělení, které přidává pozorování do empirického histogramu nad teoretickou PMF. |
| **Animace** | **Galtonova deska** pro binomické rozdělení. Kuličky padají mezi hřebíky, v každé řadě se odrazí vlevo nebo vpravo s pravděpodobností π a ukládají se do přihrádek, kde vznikne tvar binomické PMF. Posuvníky n a π mění desku. Pro Poissonovo rozdělení **padání bodů do časových intervalů** (body na ose času, přihrádky o stejné délce, počet bodů v přihrádce se sleduje). |

---

## Část Deskriptivní statistika

### 5. Deskriptivní statistiky (`02-statistika/01-typy-promennych.qmd`)

| | |
|---|---|
| **Interakce** | ✅ výběr textu, výběr tvaru rozdělení a počet intervalů histogramu (bins), další grafy statické (kvantily, boxplot). |
| **Návrh doplnění** | U kvantilů přidat posuvník řádu p a tažení hranice, boxplot se odlehlými body, které lze přidávat kliknutím. |
| **Animace** | **Třídění sloupců.** Data jako sloupce náhodné výšky se uspořádají od nejmenšího, na uspořádané řadě se pak objeví medián a kvartily, které „vyjedou“ z řady. Druhá animace: **histogram vzniká z padajících bodů**, které se při změně počtu intervalů přeskupují. |

### 6. Momentové statistiky (`02-statistika/02-deskriptivni-statistiky-momenty.qmd`)

| | |
|---|---|
| **Interakce** | ✅ osm ovládacích prvků: dva respondenti, tvar rozdělení, bins, z-skór, volba momentu. |
| **Návrh doplnění** | Přidat posuvníky šikmosti a špičatosti, které rovnou deformují křivku. |
| **Animace** | **Páka a těžiště.** Body na ose jsou závaží, osa se naklání, dokud podpěra není v průměru. Pak se „odchylky“ vykreslí jako čtverce o straně $e_i$ a jejich součet plochy je rozptyl, který se při pohybu bodů mění (geometrie čtverců). Druhá: **vektor odchylek** $\mathbf{e}$ roste a zmenšuje se při posunu $b_0$, délka je nejmenší při průměru (viz kapitola o rozkladu rozptylu). |

### 7. Aritmetika dat (`02-statistika/03-aritmetika-dat.qmd`)

| | |
|---|---|
| **Interakce** | ❌ tabulky a jeden statický graf. |
| **Návrh interakce** | **Dva posuvníky transformace $a$ a $b$ v $y = a\cdot x + b$.** Body na ose a statistiky (průměr, medián, sd, IQR) se přepočítávají živě, vedle je tabulka s původními a novými hodnotami. Tlačítka „z-skór“, „robustní“, „normalizace“ nastaví $a$ a $b$ rovnou. |
| **Animace** | **Plynulý posun a roztažení.** Body se posouvají (přičtení) a roztahují od počátku (násobení), čára průměru a vousy IQR se hýbou spolu s nimi. Student vidí, že posun nemění vzdálenosti, kdežto násobení je zvětšuje. Při z-skóru se tečky „nalepí“ na nulu a jednotkovou šířku. |

### 8. Deskriptivní statistiky z tabulky (`02-statistika/04-deskriptivy-z-tabulky.qmd`)

| | |
|---|---|
| **Interakce** | ✅ posuvníky polohy a počtu přidaných osob, páka s mediánem a průměrem se živě mění. |
| **Návrh doplnění** | Kliknutím do sloupců histogramu měnit četnosti a sledovat F, kvantily a průměr. |
| **Animace** | **Kumulativní četnost „stoupá“ jako schody:** vodorovná čára na hladině 0,25 / 0,5 / 0,75 se zvedá a zastaví na první hodnotě, kde F ≥ hladina (hledání kvantilu z tabulky). |

### 9. Rozklad rozptylu geometricky (`02-statistika/05-analyza-rozptylu-geometricky.qmd`)

| | |
|---|---|
| **Interakce** | ◐ pouze záložky (`panel-tabset`) se čtyřmi kroky, bez ovládání. |
| **Návrh interakce** | **Tažení bodu dat y v rovině** (dvě domácnosti). Přímka modelu (směr $\mathbf{1}$) je pevná, projekce se přepočítává živě a vedle se ukazují délky $\|\mathbf{y}\|$, $\|\bar{\mathbf{y}}\|$, $\|\mathbf{e}\|$ s kontrolou Pythagorovy věty. |
| **Animace** | Viz samostatná sekce **Geometrická řada (průměr jako projekce → rozklad rozptylu)** níže. Tato kapitola by se předělala na krokovou prezentaci se sloupcem dat vedle obrázku. |

---

## Geometrická řada: průměr jako projekce → rozklad rozptylu

Cíl: skutečně geometrický pohled, ne jen ilustrace. Data jsou **jeden vektor $\mathbf{y}\in\mathbb{R}^n$** a statistiky jsou délky a projekce. Obrázek je vždy spojený s tabulkou dat, jak ukazuje první vzorový screenshot (sloupce $y$, $\bar{x}\cdot\mathbf{1}$, $d$, $\hat{y}$, $b$ vedle vektorového obrázku, dole tlačítka Zpět / Přehrát / Další a tečky kroků).

**Základní myšlenka, proč nemusí být obrázek „stínem“:** vektory, které se rozkládají na navzájem kolmé části, leží přesně v podprostoru o tolika rozměrech, kolik je částí. Při rozkladu $\mathbf{y}=\bar{y}\mathbf{1}+\mathbf{d}$ stačí rovina $\text{span}\{\mathbf{1},\mathbf{d}\}$, při rozkladu mezi skupinami a uvnitř skupin $\mathbf{y}=\bar{y}\mathbf{1}+\mathbf{b}+\mathbf{w}$ stačí 3D. Osy obrázku tedy zvolíme ve směrech těchto složek (ortonormální báze z $\mathbf{1}/\sqrt{n}$, $\mathbf{d}/\|\mathbf{d}\|$, …). Pak jsou délky na obrázku přesné a Pythagorova věta se dá změřit. Samotné „natočení pohledu“ ze vzorového screenshotu je potřeba jen tehdy, když chceme ukázat, že skutečný prostor má $n$ rozměrů, a to jako volitelný krok na konci.

**Sloupec dat** (vlevo) se v každém kroku mění spolu s obrázkem: sloupec, který se právě konstruuje, je zvýrazněn akcentní barvou, tabulka dole ukazuje $\Sigma$ a $\Sigma^2$ (součet čtverců = čtverec délky).

| Krok | Obrázek (vektory) | Tabulka dat | Kontrola |
|---|---|---|---|
| 1. Data jako vektor | $\mathbf{y}$ jako šipka z počátku. Pro $n=2$ bod v rovině, pro více dat „n souřadnic“ zobrazených jako sloupec. Přepínač $n=2$ / $n=3$ / skupinová data. | sloupec $y$ | $\|\mathbf{y}\|^2=\sum y_i^2$ |
| 2. Podprostor „samé stejné hodnoty“ | přímka ve směru $\mathbf{1}$ (každé dato stejné číslo $b_0$). Posuvník $b_0$ pohybuje bodem $b_0\mathbf{1}$ po přímce. | přibude sloupec $b_0\cdot\mathbf{1}$ (všude stejné číslo) | |
| 3. Nejbližší bod = průměr | z bodu $\mathbf{y}$ se spouští kolmice na přímku. Při posuvu $b_0$ se zobrazuje délka $\|\mathbf{y}-b_0\mathbf{1}\|$, nejmenší je v patě kolmice. Animace se zastaví a vyznačí pravý úhel. | sloupec $d=y-b_0$, dole $\Sigma^2$ mění hodnotu živě, minimum je u $b_0=\bar{y}$ | $b_0=\bar{y}$, $\sum d_i=0$ |
| 4. Pythagorova věta | trojúhelník $\mathbf{y}$, $\bar{y}\mathbf{1}$, $\mathbf{d}$. Z přepon a odvěsen se postaví čtverce, ploch čtverců $\|\mathbf{y}\|^2=n\bar{y}^2+\sum d_i^2$. | sloupce $y$, $\bar{y}\mathbf{1}$, $d$ se součty čtverců | rozptyl $=\|\mathbf{d}\|^2/n$ |
| 5. Táhnutí dat | student táhne koncový bod $\mathbf{y}$ myší, projekce se přepočítává živě. U dvou dat je vidět, že rozptyl je čtvercem vzdálenosti od diagonály. | tabulka se přepočítává | |
| 6. Skupiny: podprostor „konstanta ve skupině“ | $n$ dat rozdělených do skupin A, B, C. Podprostor $\hat{\mathbf{y}}$ je rozepnutý indikátory skupin (průměr každé skupiny). Projekce $\mathbf{y}\to\hat{\mathbf{y}}$ je to samé co v kroku 3, jen v podprostoru o dimenzi 3. | sloupce $y$, $\bar{x}\cdot\mathbf{1}$, $\hat{y}$ (průměry skupin) | |
| 7. $\mathbf{b}$ a $\mathbf{w}$ | $\hat{\mathbf{y}}-\bar{y}\mathbf{1}=\mathbf{b}$ (rozdíly průměrů skupin od celkového), $\mathbf{w}=\mathbf{y}-\hat{\mathbf{y}}$ (uvnitř skupin). Tři navzájem kolmé směry: 3D obrázek, který lze natáčet myší. | sloupce $b$ a $w$, součty čtverců $SS_b$, $SS_w$ | $SS_{celk}=SS_b+SS_w$, podíl $\eta^2=SS_b/SS_{celk}$ |
| 8. (volitelně) Natočení pohledu | ukáže, že skutečný prostor je $\mathbb{R}^n$ a obrázek je jeho řez. Pohled se natáčí kolem osy $\mathbf{d}$. Slouží jen jako názorné upozornění, ne jako nutná součást výkladu. | | |

**Co se opravdu hýbe (animace v krocích 2, 3, 5, 7):**

- **Kolmice a minimum délky.** Bod $b_0\mathbf{1}$ jezdí po přímce a spolu s ním roste a klesá úsečka k $\mathbf{y}$ a plocha čtverce nad ní. Minimum je viditelné jako dno paraboly vedle obrázku (součet čtverců jako funkce $b_0$).
- **Přechod z průměru na skupinové průměry.** Vektor $\bar{y}\mathbf{1}$ se postupně „rozvětví“: nejprve všechna data mají stejný průměr, pak se sloupec rozdělí podle skupin a každé skupině se plynule přesune hodnota na její průměr (tabulka i šipka $\hat{\mathbf{y}}$ se mění současně).
- **Šipky se při přehrání skládají za sebou** (sčítání vektorů: $\bar{y}\mathbf{1}$, pak $+\mathbf{b}$, pak $+\mathbf{w}$ se dostane do $\mathbf{y}$) a tlačítko Zpět je skládá zpět.
- **Interaktivní prvky:** posuvník $b_0$, tažení koncového bodu $\mathbf{y}$, přepínač počtu dat a skupin, tlačítka Zpět / Přehrát / Další s tečkami kroků.

**Provedení:** stránku buď jako jednu OJS buňku s krokovým ovladačem (stav `step`, tlačítka z `Inputs.button`, grafika v `Plot` s `Plot.arrow`/`Plot.link`), nebo pro 3D krok s `<canvas>` a vlastním jednoduchým promítáním (rotační matice, bez knihovny). Tabulka je HTML, obrázek reaguje na stejný stav, takže jsou vždy synchronní. Protože jde o jádro knihy, doporučuji udělat nejdřív prototyp pro kroky 1 až 5 v `_drafts/` a ukázat ho před rozšířením.

**Vazba na ostatní kapitoly:** krok 3 je geometrické vysvětlení průměru. Do kapitoly o momentových statistikách (6) se vloží jen odkaz „(viz kapitola o rozkladu rozptylu)“ a tamější animace páky a čtverců zůstane jako samostatná. Kapitola o rozkladu rozptylu je pak sama o sobě úplná a nezávislá.

---

## Souhrn a doporučené pořadí

| Kapitola | Interakce | Animace (návrh) |
|---|---|---|
| 1 Klasická pravděpodobnost | ✅ | padající body do pásu ε, trychtýř |
| 2 Pravidla a vzorce | ❌ | padající body, přepínač Celek / A / B / C, zásahy v části vs. celku |
| 3a Typy proměnných | ◐ | zpřesňování měřítka |
| 3b Rozdělení diskrétní veličiny | ✅ | od PMF ke CDF |
| 4 Typická rozdělení | ✅ | Galtonova deska, padání do intervalů |
| 5 Deskriptivní statistiky | ✅ | třídění sloupců, vznik histogramu |
| 6 Momentové statistiky | ✅ | páka a čtverce odchylek |
| 7 Aritmetika dat | ❌ | posun a roztažení bodů |
| 8 Statistiky z tabulky | ✅ | stoupající kumulativní četnost |
| 9 Rozklad rozptylu | ◐ | geometrická řada: průměr jako projekce → $\mathbf{b}$ a $\mathbf{w}$, s tabulkou dat |

**Doporučené pořadí práce** (největší přínos při nejmenší práci):

1. **Kapitola 9** (tažení bodu a projekce). Je to jádro geometrického pohledu a základ pro pozdější regresi.
2. **Kapitola 2** (Vennův diagram + padající body s výběrem pruhu). Dnes tam žádná interakce není.
3. **Kapitola 7** (dva posuvníky $a$, $b$). Je nejlevnější, stačí jedna buňka.
4. **Kapitola 1 a 4** (padající body, Galtonova deska). Sdílejí kód pro padající body.
5. Ostatní.

Doporučuju hotové animace nejdřív ladit v `_drafts/`, jak vyžadují pravidla projektu, a do knihy je přesunout až po vizuální kontrole.
