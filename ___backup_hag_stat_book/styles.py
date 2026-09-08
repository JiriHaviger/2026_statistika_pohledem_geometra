# styles.py

# --- A. Konfigurační barvy pro Plotly (Hex kódy) ---
# Tato barva by měla být shodná s primaryColor v .streamlit/config.toml
ACCENT_CYAN = "#0085CC"  

# Barvy pro populační/základní data
POP_GRAY_DARK = "#666666" 
POP_GRAY_LIGHT = "#B0B0B0" 
HIST_GRAY = "#888888" 

# --- B. Stylování pro Streamlit (přes CSS/Markdown) ---
# Třída pro nadpisy, pokud ji potřebujete
CSS_STYLES = """
<style>
    .big-font {font-size: 1.5rem !important; font-weight: 600; color: #1A1A1A;}
    .stSlider > label, .stSelectbox > label {font-size: 1rem !important;}
    .stMetric label {font-size: 0.95rem !important;}
    .stMetric div[data-testid="stMetricValue"] {font-size: 1.1rem !important; color: #1A1A1A;}
</style>
"""

# Funkce pro aplikaci základního rozložení/stylů (volání jen 1x na každé stránce)
def apply_page_setup(title):
    st.set_page_config(page_title=title, layout="wide")
    st.markdown(CSS_STYLES, unsafe_allow_html=True)

# ... Můžete zde definovat i složitější Plotly šablony