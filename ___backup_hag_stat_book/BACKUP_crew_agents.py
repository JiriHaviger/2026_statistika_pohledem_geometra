import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool

# ----------------- NASTAVENÍ -----------------
load_dotenv()
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"
os.environ["CREWAI_TRACING_ENABLED"] = "false"
os.environ["GEMINI_API_KEY"] = "AIzaSyDJOH9c6stLvoqtjPReMosaScFhZEN0mzM"

# ----------------- NÁSTROJE -----------------
@tool("Čtečka souborů")
def read_file(file_path: str) -> str:
    """Přečte obsah souboru z disku. Vstupem je přesná cesta k souboru."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Chyba při čtení souboru {file_path}: {str(e)}"

# ----------------- AGENTI -----------------
project_manager = Agent(
    role="Projektový manažer a stylový strážce",
    goal="Udržovat konzistentní styl, strukturu i barevné schéma celé učebnice.",
    backstory="Jsi velmi pečlivý koordinátor vzdělávacího projektu.",
    llm="gemini/gemini-2.5-flash", 
    verbose=True
)

content_agent = Agent(
    role="Autor statistiky a lineární algebry",
    goal="Psát kvalitní obsah v češtině podle přesných pravidel.",
    backstory="Zkušený lektor statistiky.",
    llm="gemini/gemini-2.5-flash",
    verbose=True
)

ojs_agent = Agent(
    role="Specialista na Observable JS",
    goal="Vytvářet interaktivní prvky s konzistentním barevným schématem.",
    backstory="Expert na Observable JS a data vizualizace.",
    llm="gemini/gemini-2.5-flash",
    verbose=True
)

reviewer_agent = Agent(
    role="Recenzent a finální editor",
    goal="Kontrolovat dodržení všech pravidel včetně barevné konzistence.",
    backstory="Přísný matematik a editor.",
    llm="gemini/gemini-2.5-flash",
    verbose=True
)

# ----------------- ÚKOLY -----------------
task1 = Task(
    description="""
    Tvým úkolem je zanalyzovat stávající nastavení projektu a vytvořit **Detailní Style Guide** pro novou kapitolu.
    
    Použij k tomu nástroj `read_file` a prozkoumej tyto soubory v kořenovém adresáři:
    1. `_quarto.yml` – abys pochopil strukturu knihy, navigaci a globální nastavení.
    2. `hag_custom.scss` – abys zjistil, jaké CSS/SASS styly a barvy jsou již definované.
    3. `02-statistika/01_deskriptivní statistiky kvantily.qmd` – jako ukázku toho, jak píšeme text a kódy teď.

    Na základě této analýzy sestav Style Guide, který respektuje stávající kód, ale doplňuje/rozšiřuje pravidla o:
    **1. Celkový styl (Moderní):** Vzdušný styl psaní, krátké odstavce, bezpatkové písmo, správná hierarchie.
    **2. Dvojjazyčnost:** Příprava pro přepínač jazyků (CS / EN) a konzistentní obsah.
    **3. Dark / Light mode:** Jak zajistit, aby stávající barvy z .scss fungovaly v obou režimech.
    **4. Responsive design:** Pravidla pro OJS vizualizace, aby se nerozbíjely na mobilech.
    **5. Speciální bloky:** Definice pro divy (příklady se skrytým řešením) a na konec kapitoly přidej strukturu pro studentský AI prompt.
    """,
    expected_output="Kompletní Style Guide v Markdown formátu, který striktně vychází ze souborů _quarto.yml a hag_custom.scss.",
    output_file="style_guide.md",
    agent=project_manager,
    tools=[read_file]
)
task2 = Task(
description="""
    Napiš textový obsah kapitoly na téma: **{tema}**.
    Výstupem bude struktura pro soubor: `{vystupni_soubor}`.
    
    Při psaní striktně dodržuj Style Guide (z task1) a následující akademické požadavky:
    1. V teoretické části podrobně a srozumitelně vysvětli tato **hlavní témata**: {klicove_pojmy}.
    2. Zaměř se na geometrickou nebo intuitivní interpretaci těchto pojmů, aby byla látka pro studenty vizuálně pochopitelná.
    3. Praktické příklady a cvičení zaměř na: {zamereni_uloh}.
    4. U praktických ukázek demonstruj postup a interpretaci výsledků v následujícím prostředí: {nastroje}.
    5. Nezapomeň u příkladů připravit sekce pro skrytá řešení (podle formátu ze Style Guide).
    """,
    expected_output="Kompletní Quarto Markdown obsah kapitoly v češtině splňující detailní zadání témat a nástrojů.",
    output_file="02-statistika/05_diskretni_distribuce.qmd",
    agent=content_agent
)

task3 = Task(
    description="""
        Vytvoř 2–4 interaktivní Observable JS prvky, které striktně dodržují barevné schéma definované ve Style Guide.
        """,
    expected_output="Hotové OJS bloky s konzistentními barvami.",
    agent=ojs_agent
)

task4 = Task(
    description="""
        Zkontroluj celou kapitolu. Ověř dodržení Style Guide (struktura, divy, 
        barevná konzistence v textu i grafech), matematickou správnost a kvalitu studentského promptu.
        """,
    expected_output="Finální verze kapitoly + komentáře k případným úpravám.",
    agent=reviewer_agent
)

# ----------------- CREW -----------------

crew = Crew(
    agents=[
        project_manager, 
        content_agent, 
    #    ojs_agent, 
    #    reviewer_agent
    ],
    tasks=[
        task1, 
        task2, 
    #    task3, 
    #    task4
    ],
    process=Process.sequential,
    verbose=True,
    max_rpm=10,
)

#=====================================================================================================

print("🚀 Spouštím CrewAI a generuji obsah...")

result = crew.kickoff(inputs={
    "tema": "Diskrétní distribuce",     
    "vystupni_soubor": "02-statistika/05_diskretni distribuce.qmd",
    "klicove_pojmy": """
        Binomická, Poissonova, Geometrická,... 
        Hypergeometrická distribuce, pravděpodobnostní funkce, kumulativní funkce...
        , střední hodnota, rozptyl
        """,
    "zamereni_uloh": """
        určení pravděpodobnosti ze zadaného kvantilu a kvantil ze zadané pravděpodobnosti, 
        střední hodnoty a rozptylu.
        """,
    "nastroje": "Excel, R, Python (SciPy), Observable JS",    
})
print("\n--- 💾 VYNUCENÝ ZÁPIS NA DISK ---")

# 2. Uložení TASK 1: Style Guide (Získání výstupu přímo z objektu task1)
try:
    with open("style_guide.md", "w", encoding="utf-8") as f:
        # Vytáhneme surový text z prvního úkolu
        f.write(str(task1.output.raw))
    print("✅ Soubor 'style_guide.md' úspěšně uložen do kořene projektu.")
except Exception as e:
    print(f"❌ Chyba při zápisu Style Guide: {e}")

# 3. Uložení TASK 2: Nová kapitola (Získání výstupu z druhého úkolu)
try:
    cesta_kapitola = "02-statistika/05_diskretni_distribuce.qmd"
    with open(cesta_kapitola, "w", encoding="utf-8") as f:
        # Vytáhneme surový text z druhého úkolu
        f.write(str(task2.output.raw))
    print(f"✅ Nová kapitola úspěšně uložena do: {cesta_kapitola}")
except Exception as e:
    print(f"❌ Chyba při zápisu kapitoly: {e}")