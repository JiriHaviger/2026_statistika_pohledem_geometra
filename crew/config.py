import os

# Vypnutí telemetrie CrewAI – musí být PŘED importem crewai
# (různé verze CrewAI používají různé názvy proměnných)
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"
os.environ["CREWAI_TRACING_ENABLED"] = "false"
os.environ["OTEL_SDK_DISABLED"] = "true"

from dotenv import load_dotenv
from crewai import LLM


# ----------------- NASTAVENÍ -----------------
load_dotenv()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY není nastaven – doplň ho do souboru .env")
#  načtení apikey ze souboru .env, který je v .gitignore, aby se necommitoval do repozitáře
# na ntb je potřeba dodat
#   balíček python-dotenv (`pip install python-dotenv`)
#   vytvořený soubor .env s obsahem: GEMINI_API_KEY="tvůj_api_key_z_Google_Cloud_Console"


gemini_model = LLM(
    model="gemini/gemini-2.5-flash",  # Flash je na výpadky 503 mnohem méně náchylný než "Pro"
    api_key=GEMINI_API_KEY,
    max_retries=5,       # Pokud Google hodí 503, CrewAI to automaticky zkusí znovu (až 5x)
)


STYLE_GUIDE_PATH = "docs_for_agents/style_guide.md"
