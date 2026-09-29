from crewai import Agent
from crew.config import gemini_model


# ----------------- AGENTI -----------------

project_manager = Agent(
    role="Projektový manažer a stylový strážce",
    goal="Udržovat konzistentní styl, strukturu i barevné schéma celé učebnice.",
    backstory="Jsi velmi pečlivý koordinátor vzdělávacího projektu.",
    llm=gemini_model,
    verbose=True
)

content_agent = Agent(
    role="Autor statistiky a lineární algebry",
    goal="Psát kvalitní obsah v češtině podle přesných pravidel.",
    backstory=(
        "Zkušený lektor statistiky. Tvůj styl je inspirován Grinstead & Snell "
        "(Introductory Probability) a Anton (Elementary Linear Algebra): "
        "jasné definice, krátké odstavce, reálné příklady z ekonomiky a medicíny."
    ),
    llm=gemini_model,
    verbose=True
)

ojs_agent = Agent(
    role="Specialista na Observable JS",
    goal="Vytvářet interaktivní prvky s konzistentním barevným schématem.",
    backstory="Expert na Observable JS a data vizualizace.",
    llm=gemini_model,
    verbose=True
)

reviewer_agent = Agent(
    role="Recenzent a finální editor",
    goal="Kontrolovat dodržení všech pravidel včetně barevné konzistence.",
    backstory="Přísný matematik a editor.",
    llm=gemini_model,
    verbose=True
)
