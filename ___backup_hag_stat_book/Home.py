import streamlit as st
from styles import ACCENT_CYAN

st.set_page_config(page_title="Statistika živě", layout="wide")


st.title("📊 Statistika živě")
st.markdown("### Interaktivní demonstrace statistických pojmů")

st.markdown("""
    **Dostupné demonstrace:**
    - **Centrální limitní věta** - vizualizace CLT
    - **SD vs SE** - dvě zkratky, které často pletou začátečníci 
    - **Intervaly spolehlivosti** (připravujeme)
    - **Testování hypotéz** (připravujeme)        
    - **Dvě možné chyby** (připravujeme)        
            
            

    👈 Vyberte téma z bočního menu
""")

st.caption("© 2025 Jiří Haviger • Statistika živě  • Vytvořeno s Claude a Gemini AI & Streamlit")