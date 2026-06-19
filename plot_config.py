# plot_config.py
# Barvy pro Plotly grafy

ACCENT_CYAN = "#0085CC"
POP_GRAY_DARK = "#666666" 
POP_GRAY_LIGHT = "#B0B0B0" 
HIST_GRAY = "#888888"

# Plotly šablona s jednotnými barvami
import plotly.graph_objects as go

PLOTLY_TEMPLATE = go.layout.Template(
    layout=dict(
        colorway=[ACCENT_CYAN, POP_GRAY_DARK, POP_GRAY_LIGHT],
        font=dict(family="Arial, sans-serif", size=14),
        plot_bgcolor="white",
        paper_bgcolor="white"
    )
)
