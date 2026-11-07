import os

# Vypnutí telemetrie CrewAI – musí být PŘED importem crewai
# (různé verze CrewAI používají různé názvy proměnných)
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"
os.environ["CREWAI_TRACING_ENABLED"] = "false"
os.environ["OTEL_SDK_DISABLED"] = "true"

from dotenv import load_dotenv
from crewai import LLM

from crew.paths import PROJECT_ROOT


# ----------------- NASTAVENÍ -----------------
# API klíč se načítá ze souboru .env v kořeni projektu (soubor je v .gitignore,
# takže se nikdy necommituje). Obsah .env:
#   ANTHROPIC_API_KEY=sk-ant-...
# Klíč: platform.claude.com → Settings → API Keys (účtuje se zvlášť od předplatného Claude).
# Instalace (do .venv): uv pip install --python .venv\Scripts\python.exe "crewai[anthropic]" python-dotenv
load_dotenv(PROJECT_ROOT / ".env")   # vždy .env z kořene projektu, ne z aktuálního adresáře
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise RuntimeError("ANTHROPIC_API_KEY není nastaven – doplň ho do souboru .env")

# Jediné místo, kde je název modelu.
MODEL_NAME = "anthropic/claude-sonnet-5-5"

llm_model = LLM(
    model=MODEL_NAME,
    api_key=ANTHROPIC_API_KEY,
    max_tokens=64000,  # strop délky odpovědi; celá kapitola se musí vejít do jedné odpovědi
    stream=True,       # při velkém max_tokens je streamování nutné (jinak hrozí timeout)
    max_retries=5,     # při přetížení serveru CrewAI zkusí volání znovu (až 5×)
    # temperature záměrně nenastavujeme – nové modely Claude ji odmítají
)

# Původní nastavení (Gemini) pro případný návrat:
# llm_model = LLM(
#     model="gemini/gemini-2.5-flash",
#     api_key=os.environ.get("GEMINI_API_KEY"),
#     max_retries=5,
# )
