import os
from google import genai
from google.genai import types

# 1. Ruční nastavení klíče (přesně jako to máš ty)
os.environ["GEMINI_API_KEY"] = "AIzaSyDJOH9c6stLvoqtjPReMosaScFhZEN0mzM"

api_key = os.environ.get("GEMINI_API_KEY")
print(f"Kontrola klíče: {api_key[:10]}...")

# 2. Testovací volání přes oficiální Google GenAI SDK
try:
    # Inicializace klienta (automaticky si vezme GEMINI_API_KEY z os.environ)
    client = genai.Client()
    
    response = client.models.generate_content(
        model='gemini-2.5-flash', # případně 'gemini-2.5-pro' pro pokročilejší placený model
        contents='Ahoj, funguje můj placený API klíč v pořádku?',
    )
    print("\n[ÚSPĚCH] Google API funguje skvěle!")
    print("Odpověď od Gemini:")
    print(response.text)

except Exception as e:
    print(f"\n[CHYBA] Propojení s Google API selhalo: {e}")
    print("Zkontroluj, zda máš v Google Cloud Console povolené 'Generative Language API' a nastavenou fakturaci (Billing).")