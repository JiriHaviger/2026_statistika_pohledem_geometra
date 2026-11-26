"""Kořen projektu a skládání cest.

Všechny cesty v generátoru se skládají přes PROJECT_ROOT, takže program funguje
stejně bez ohledu na to, z jakého adresáře je spuštěn. Modul nemá žádné závislosti.
"""

from pathlib import Path

# Adresář nad balíčkem crew/ = adresář s _quarto.yml (nezávisí na aktuálním adresáři)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

if not (PROJECT_ROOT / "_quarto.yml").exists():
    raise RuntimeError(f"V {PROJECT_ROOT} chybí _quarto.yml – nejde o kořen projektu.")


DOCS_DIR = PROJECT_ROOT / "docs_for_agents"
STYLE_GUIDE_PATH = DOCS_DIR / "style_guide.md"
STYLE_GUIDE_BACKUP_PATH = DOCS_DIR / "style_guide.backup.md"
STYLE_GUIDE_RAW_PATH = DOCS_DIR / "style_guide.raw.md"   # surový výstup LLM při chybě
AUDIT_REPORT_PATH = DOCS_DIR / "audit_report.md"
DRAFTS_DIR = PROJECT_ROOT / "_drafts"            # sem se generují kapitoly (Quarto složku ignoruje)
REVIEW_DIR = DOCS_DIR / "review"                 # reporty ke generovaným kapitolám


def project_path(relative: str) -> Path:
    """Absolutní cesta k souboru v projektu. Cesta nesmí vést mimo projekt."""
    path = (PROJECT_ROOT / relative).resolve()
    if not path.is_relative_to(PROJECT_ROOT):
        raise ValueError(f"Cesta vede mimo projekt: {relative}")
    return path


def display_path(path: Path) -> str:
    """Cesta relativní ke kořeni projektu (pro výpisy uživateli)."""
    try:
        return path.resolve().relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        return str(path)
