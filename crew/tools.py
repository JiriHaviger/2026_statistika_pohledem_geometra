from crewai.tools import tool

from crew.calc import run_calc
from crew.paths import PROJECT_ROOT, project_path

# Soubory a složky, které agenti číst nesmí (tajné údaje, historie gitu, prostředí)
FORBIDDEN_PARTS = {".env", ".git", ".venv"}


# ----------------- NÁSTROJE -----------------

@tool("Čtečka souborů")
def read_file(file_path: str) -> str:
    """Přečte obsah souboru projektu. Vstupem je cesta relativní ke kořeni projektu,
    např. `_quarto.yml` nebo `02-statistika/01-typy-promennych.qmd`."""
    try:
        path = project_path(file_path)
    except ValueError as e:
        return f"Chyba: {e}"

    if FORBIDDEN_PARTS & set(path.relative_to(PROJECT_ROOT).parts):
        return f"Chyba: čtení {file_path} není povoleno."

    try:
        return path.read_text(encoding="utf-8")
    except OSError as e:
        return f"Chyba při čtení souboru {file_path}: {e}"


@tool("Kalkulačka")
def calc(code: str) -> str:
    """Spustí krátký Python a vrátí, co kód vypsal. Slouží ke VŠEM číselným výpočtům
    (nikdy nepočítej z hlavy). Výsledky vypiš příkazem print(). K dispozici jsou
    np (numpy), stats (scipy.stats), math, statistics, fractions, itertools, functools;
    jiné importy, soubory a síť nejsou povoleny. Příklad:
    print(stats.binom.pmf(3, 10, 0.5)); print(np.mean([1, 2, 3, 4]))"""
    return run_calc(code)
