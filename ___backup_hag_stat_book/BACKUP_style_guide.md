# Detailní Style Guide pro Havi Notes

Tento style guide definuje pravidla a doporučení pro tvorbu obsahu v projektu "Havi Notes", s cílem zajistit konzistentní vzhled, strukturu a uživatelskou zkušenost napříč celou učebnicí. Vychází ze stávajícího nastavení v `_quarto.yml` a `hag_custom.scss`, a rozšiřuje je o best practices pro moderní webový obsah.

---

## 1. Celkový Styl (Moderní a Vzdušný)

Cílem je poskytnout čtenáři příjemné a snadno čitelné prostředí s jasnou strukturou, která odpovídá moderním standardům webového designu.

### 1.1 Typografie a Čitelnost

*   **Písmo (Font):** Projekt standardně využívá bezpatkové písmo definované tématem `cosmo`. Udržujte tento styl pro veškerý textový obsah.
*   **Velikost písma:** Základní velikost písma je `1rem`. Pro speciální bloky a poznámky je možné použít mírně menší velikost, např. `0.9rem` jako v `.example-box` (viz `hag_custom.scss`).
*   **Váha písma:**
    *   Nadpisy (`h1`, `h2`, `h3`) používají `font-weight: 600;` (semibolds) podle `$headings-font-weight` v `hag_custom.scss`.
    *   Tučný text (`**text**`) používejte pro zvýraznění klíčových pojmů.
*   **Barvy textu:**
    *   Primární barva pro nadpisy je `$primary` (`#0085CC`).
    *   Základní text by měl být `$dark` (`#1A1A1A`) v režimu "light".
    *   V `hag_custom.scss` jsou definovány další barvy (`$secondary`, `$gray-light`, `$light`, `$warning`, `$warning-dark`), které by měly být důsledně používány.

### 1.2 Hierarchie a Struktura

*   **Nadpisy:**
    *   Používejte hierarchicky správné nadpisy od `h1` po `h3` (nebo `h4` je-li to nezbytné).
    *   `h1, h2, h3` jsou vizuálně zvýrazněny `border-left: 4px solid $primary; padding-left: 1rem;` (viz `hag_custom.scss`).
    *   `#` (H1) pro název kapitoly (definován v `_quarto.yml`).
    *   `##` (H2) pro hlavní sekce v kapitole.
    *   `###` (H3) pro podsekce.
    *   Pro speciální nadpisy, které nemají být číslovány a nemají se objevovat v TOC (např. "Příklad", "Klíčové poznatky"), použijte atributy `.unnumbered .unlisted`:
        ```markdown
        ### Příklad {.unnumbered .unlisted}
        ```
*   **Odstavce:** Pište krátké, výstižné odstavce. Jeden odstavec by měl ideálně pojednávat o jedné myšlence. Vyhněte se dlouhým blokům textu pro lepší čitelnost.
*   **Mezery:** Využívejte mezery mezi odstavci a sekcemi pro "vzdušný" vzhled a lepší čitelnost.
*   **Odrážkové seznamy:** Používejte odrážkové seznamy pouze pro přehlednou prezentaci informací.
*   **Číselné seznamy:** Používejte číselné seznamy pouze pro popis kroků nějakého postupu. 

### 1.3 Zvýraznění a Speciální Formátování

*   **Klíčové pojmy:**
    *   Pro krátké, klíčové pojmy (jednotlivá slova nebo krátké fráze) použijte tučné písmo (`**text**`).
    *   Pro vizuálně výraznější zvýraznění použijte `highlight-key` třídu: `<span class="highlight-key">klíčový pojem</span>`.
*   **Termíny / Definice:** Pro formální definice nebo důležité termíny použijte `highlight-term` třídu: `<span class="highlight-term">Definice</span>`.
*   **Matematika:**
    *   Inline matematika: `$\\alpha + \\beta$`.
    *   Bloková matematika (automatické centrování):
        ```latex
        $$
        E = mc^2
        $$
        ```
    *   Pro zarovnané rovnice použijte prostředí `align`:
        ```latex
        \begin{align}
            f(x) &= x^2 + 2x + 1 \\
            &= (x+1)^2
        \end{align}
        ```
*   **Citace:** Používejte standardní Quarto/Pandoc citace ve formátu `[@reference-key]`. Bibliografie je definována v `references.bib` a styl v `csl: https://www.zotero.org/styles/apa`.

---

## 2. Dvojjazyčnost (CS / EN)

`_quarto.yml` je nastaveno s `lang: cs`, což je výchozí jazyk projektu. Pro budoucí implementaci přepínače jazyků je nutné myslet na strukturu obsahu.

### 2.1 Strategie pro Dvojjazyčný Obsah

Doporučuje se jedna z následujících strategií:

*   **Oddělené soubory pro každý jazyk:** Pro každou kapitolu vytvořit `kapitola.qmd` pro češtinu a `kapitola.en.qmd` pro angličtinu. Obsah v každém souboru by byl kompletně v daném jazyce. Přepínač jazyků by pak dynamicky načítal příslušnou verzi.
*   **Podmíněné bloky v jednom souboru:** Použití Quarto shortcodů nebo Pandoc divů s podmíněným vykreslováním (méně flexibilní pro údržbu, ale obsah je v jednom místě).
    ```markdown
    ::: {.lang-cs}
    Obsah v češtině.
    :::

    ::: {.lang-en}
    Content in English.
    :::
    ``````scss
/*-- scss:defaults --*/
// Původní SASS proměnné slouží k definici výchozích (light mode) CSS proměnných
$primary_light: #0085CC;
$secondary_light: #666666;
$dark_light: #1A1A1A;
$light_light: #F8F9FA;
$warning_light: #8b0512;

:root { /* Light mode defaults */
  --primary: #{$primary_light};
  --secondary: #{$secondary_light};
  --dark: #{$dark_light};
  --light: #{$light_light};
  --warning: #{$warning_light};
  --warning-dark: darken($warning_light, 10%); /* Zde by bylo lepší definovat i dark variantu přímo */
  --light-bg: #{$light_light}; // Pro použití v blocích (např. .definition-box)
  --dark-text: #{$dark_light}; // Pro použití v blocích
}

@media (prefers-color-scheme: dark) {
  :root { /* Dark mode adjustments */
    --primary: #6ab0e5; // Světlejší odstín modré pro tmavé pozadí
    --secondary: #b0b0b0; // Světlejší šedá
    --dark: #f8f9fa; // Světlý text
    --light: #1a1a1a; // Tmavé pozadí (pro základ textu)
    --warning: #e07f87; // Světlejší varovná barva
    --warning-dark: #cc505a; // Tmavší verze varovné pro tmavý režim
    --light-bg: #2a2a2a; // Tmavé pozadí pro bloky (např. .definition-box)
    --dark-text: #f8f9fa; // Světlý text pro bloky
  }
}

// Následně ve SCSS místo $primary použít var(--primary) atd.
.definition-box {
  border: 1px solid var(--primary);
  border-left: 8px solid var(--primary);
  background-color: var(--light-bg);
  // ...
}

h1, h2, h3 {
  color: var(--primary);
  border-left: 4px solid var(--primary);
  // ...
}
```

### 2.2 Konzistence

*   **Terminologie:** Pro překlady zajistěte konzistentní terminologii napříč celou učebnicí pro oba jazyky. Vytvoření glosáře klíčových termínů je silně doporučeno.
*   **Obrázky a Grafy:** Všechny popisky, osy a legendy v grafech (zejména OJS) by měly být buď dvojjazyčné, nebo připravené na dynamickou změnu jazyka. Pro OJS je možné využít proměnné pro popisky, které se načítají podle zvoleného jazyka.
*   **Metadata:** Ujistěte se, že metadata (titulky knihy, kapitol, autor atd.) v `_quarto.yml` jsou rovněž připravena na dvojjazyčnost.

---

## 3. Dark / Light Mode

Téma `cosmo` spolu s `hag_custom.scss` definuje světlý režim. Pro zajištění kompatibility s tmavým režimem je potřeba adaptovat barvy.

### 3.1 Využití CSS Vlastností (Custom Properties)

Místo přímého použití SASS proměnných, jako `$primary`, je doporučeno přemapovat je na CSS custom properties (CSS proměnné), které lze snadněji přepínat v závislosti na zvoleném tématu.

**Příklad úpravy `hag_custom.scss`:**

*   **Testování:** Pečlivě otestujte všechny prvky v obou režimech (světlá a tmavá) pomocí vývojářských nástrojů prohlížeče.

---

## 4. Responsive Design pro OJS Vizualizace

Vizualizace vytvořené v Observable JavaScript (OJS) musí být plně responzivní a správně se zobrazovat na různých velikostech obrazovek, včetně mobilních zařízení.

### 4.1 Obecná Pravidla pro OJS

*   **Velikost grafu:** Místo pevné šířky (`width: 800;`) použijte `width: width,` (globální proměnná `width` poskytovaná Quarto) pro dynamické přizpůsobení. Pro výšku (`height`) použijte rozumnou pevnou hodnotu nebo ji vypočítejte jako poměr k šířce (např. `height: width * 0.5`).
*   **Měřítka a Rozsahy:** Měřítka (scales) by měla být nastavena tak, aby se automaticky přizpůsobovala rozsahu dat a dostupnému prostoru.
*   **Popisky a Legendy:**
    *   Ujistěte se, že popisky os, legendy a titulky grafů zůstávají čitelné i na malých obrazovkách.
    *   `style: { fontSize: "14px", background: "transparent" }` je dobrý základ, ale může vyžadovat media queries pro menší obrazovky, pokud popisky kolidují.
    *   Vyvarujte se příliš mnoha ručně definovaných `ticks` na osách (`ticks: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]`), nechte Observable Plot automaticky vybrat optimální počet pro danou šířku.
*   **Interaktivita:** Pokud grafy obsahují interaktivní prvky, zajistěte, aby byly snadno ovladatelné dotykem.
*   **Testování:** Vždy testujte OJS vizualizace na různých zařízeních a velikostech okna prohlížeče.

### 4.2 Konkrétní Doporučení

*   **Nastavení `width` v OJS bloku:**
    ```ojs
    Plot.plot({
      width: width, // Responzivní šířka
      height: 250,  // Pevná výška nebo výpočet založený na šířce
      // ...
    })
    ```
*   **`screenshot: true`:** Pro případy, kdy je vizualizace složitá pro vykreslení na všech zařízeních, nebo když je potřeba rychlá náhledová verze, může být `//| screenshot: true` užitečné. Mělo by být používáno s rozvahou, protože omezuje interaktivitu.
*   **Minimalizace pevných rozměrů:** Vyhněte se `marginLeft`, `marginRight` s pevnou pixelovou hodnotou, pokud to není nezbytně nutné, a zvažte jejich nastavení v kontextu `width`.

---

## 5. Speciální Bloky

Pro zlepšení didaktiky a interaktivity zavádíme definice pro speciální bloky.

### 5.1 Bloky s Příklady a Skrytým Řešením (Callout `collapse="true"`)

Pro příklady, jejichž řešení má být zpočátku skryto, využijte existující `callout-note` s atributem `collapse="true"`, jak je již demonstrováno v ukázkové kapitole.

*   **Struktura:**
    ```markdown
    ::: {.callout-note collapse="true"}
      # Název Příkladu / Úkolu {.unnumbered .unlisted}
      Zde je zadání příkladu nebo úkolu.

      ---

      #### Řešení
      Zde je detailní řešení, včetně kódu nebo matematických kroků.

      ```ojs
      // Kód řešení
      ```
    :::
    ```
*   **Nadpis:** Použijte `{.unnumbered .unlisted}` u nadpisu bloku (`# Název Příkladu / Úkolu`), aby se nezobrazoval v TOC a nebyl číslován.
*   **Oddělovač:** Pro vizuální oddělení zadání od řešení použijte vodorovnou čáru (`---`).
*   **Řešení nadpis:** Řešení vždy uvádějte pod nadpis `#### Řešení`.

### 5.2 Blok pro AI Prompt (Nový typ calloutu)

Na konec každé kapitoly (nebo významné sekce) přidejte blok, který studentům nabídne strukturovaný prompt pro interakci s AI nástroji. Tento blok by měl být zřetelně oddělený a vizuálně rozpoznatelný.

*   **Vizuální Styl:** Vytvoříme novou třídu `.ai-prompt` pro existující `callout-tip`, aby se vizuálně odlišil.

*   **Příklad struktury:**
    ```markdown
    ::: {.callout-tip title="AI Pomocník pro tuto kapitolu" .ai-prompt}
    Chtěli byste lépe porozumět této kapitole? Zkuste použít následující prompt ve vašem oblíbeném AI nástroji (např. ChatGPT, Gemini):

    ```text
    "Jsem student/ka a právě studuji kapitolu o [Název Kapitoly, např. Deskriptivní Statistice - Kvantilech] z učebnice [Název Učebnice, např. Havi Notes].
    Tato kapitola pojednává o [stručný přehled témat, např. typech proměnných, mírách polohy (modus, medián, kvantily), mírách variability (rozpětí, IQR) a box-plotech].

    Mohl/a bys mi prosím:
    1. Vysvětlit klíčové pojmy [uveď 3-5 klíčových pojmů z kapitoly, např. 'kardinální proměnná', 'medián', 'mezikvartilové rozpětí', 'kvantilová funkce', 'box-plot'] jednodušším jazykem s reálnými příklady?
    2. Navrhnout 3-5 praktických cvičení nebo úloh, které mi pomohou ověřit si porozumění látce?
    3. Identifikovat 2-3 nejčastější chyby nebo nedorozumění, ke kterým studenti v této oblasti docházejí, a jak se jim vyhnout?
    4. Navrhnout téma pro malý výzkumný projekt, kde bych mohl/a aplikovat znalosti z této kapitoly?

    Při odpovědích se snaž být stručný/á a jasný/á, a pokud je to možné, používej český jazyk. Děkuji!"
    ```

    **Tipy pro studenty:**
    *   Můžete upravit prompt dle vašich specifických potřeb.
    *   Nahraďte zástupné texty `[ ]` konkrétními informacemi z kapitoly, kterou právě studujete.
    *   Experimentujte s různými AI nástroji a jejich nastaveními.
    :::
    ```

*   **SCSS pro `.ai-prompt` (příklad pro `hag_custom.scss`):**
    ```scss
    .callout-ai-prompt {
      border-left-color: #6a1b9a !important; // Speciální barva (např. fialová)
      background-color: rgba(106, 27, 154, 0.1) !important; // Světlejší pozadí
      .callout-title {
        color: #6a1b9a !important;
        font-weight: bold;
      }
      .ai-prompt code { // Styl pro prompt text
        background-color: rgba(106, 27, 154, 0.05);
        border: 1px solid rgba(106, 27, 154, 0.2);
        display: block;
        padding: 1rem;
        border-radius: 5px;
        white-space: pre-wrap; /* Pro zalomení textu */
        word-break: break-all; /* Pro dlouhé řetězce bez mezer */
      }
    }
    ```
    Tímto zajistíme vizuální odlišení tohoto bloku od ostatních `callout-tip` bloků.