from crewai.tools import tool


# ----------------- NÁSTROJE -----------------

@tool("Čtečka souborů")
def read_file(file_path: str) -> str:
    """Přečte obsah souboru z disku. Vstupem je přesná cesta k souboru."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Chyba při čtení souboru {file_path}: {str(e)}"
