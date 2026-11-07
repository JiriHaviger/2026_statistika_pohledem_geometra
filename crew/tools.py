from crewai.tools import tool

from crew.paths import PROJECT_ROOT, project_path

# Soubory a složky, které agenti číst nesmí (tajné údaje, historie gitu, prostředí)
FORBIDDEN_PARTS = {".env", ".git", ".venv"}


# ----------------- NÁSTROJE -----------------

@tool("Čtečka souborů")
def read_file(file_path: str) -> str:
    """Přečte obsah souboru projektu. Vstupem je cesta relativní ke kořeni projektu,
    např. `_quarto.yml` nebo `02-statistika/01_typy promennych.qmd`."""
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
