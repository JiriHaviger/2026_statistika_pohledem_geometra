# Seznam kapitol ke generování.
# Přidávej další kapitoly jako položky tohoto seznamu.
# Pole 'aplikacni_oblasti' je nepovinné – výchozí hodnota je "ekonomika/management a medicína".

CHAPTERS = [
    {
        "tema": "Diskrétní pravděpodobnostní rozdělení",
        "vystupni_soubor": "02-statistika/05_diskretni_distribuce.qmd",
        "klicove_pojmy": """
            1. Binomická distribuce – model opakovaných pokusů s dvěma výsledky
            2. Poissonova distribuce – model vzácných událostí v čase nebo prostoru
            3. Geometrická distribuce – model čekání na první úspěch
            4. Kumulativní distribuční funkce (CDF) – výpočet P(X ≤ x)
            5. Střední hodnota a rozptyl – interpretace parametrů rozdělení
        """,
        "zamereni_uloh": """
            - Výpočet P(X = k) z PMF
            - Výpočet P(X ≤ k) a P(X > k) z CDF
            - Určení kvantilu: najdi k tak, aby P(X ≤ k) ≥ p
            - Výpočet E(X) a Var(X) ze zadaných parametrů
            - Rozhodnutí, které rozdělení použít v dané situaci
        """,
        "nastroje": "R (dbinom, dpois, dgeom, pbinom), Python (scipy.stats), Excel (BINOM.DIST)",
        "aplikacni_oblasti": "pojišťovnictví/management výroby a epidemiologie/klinické studie",
    },
    # Příklad další kapitoly – odkomentuj a uprav:
    # {
    #     "tema": "Spojitá pravděpodobnostní rozdělení",
    #     "vystupni_soubor": "02-statistika/06_spojita_rozdeleni.qmd",
    #     "klicove_pojmy": "Normální rozdělení, Exponenciální rozdělení, ...",
    #     "zamereni_uloh": "...",
    #     "nastroje": "R, Python, Excel",
    #     "aplikacni_oblasti": "finance/řízení zásob a medicína",
    # },
]
