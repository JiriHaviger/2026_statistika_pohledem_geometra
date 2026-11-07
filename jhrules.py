"""JH Rules – barvy a nastavení matplotlib / plotly.

Kopie palety z hag_custom.scss (proměnné $jh-*). Při změně palety uprav obě místa;
shodu kontroluje `.venv\\Scripts\\python.exe -m crew.style_guide`.
"""
C = dict(bg="#FFFFFF", text="#3D3D3D", primary="#4682B4", primary_light="#A9C6DE",
         primary_text="#3D729E", accent="#D35400", context="#7F7F7F",
         context_light="#D3D3D3", grid="#EBEBEB", warning="#8C2D35")


def use_matplotlib():
    import matplotlib.pyplot as plt
    from cycler import cycler
    plt.rcParams.update({
        "font.family": "sans-serif", "font.sans-serif": ["Arial", "DejaVu Sans"],
        "figure.facecolor": C["bg"], "axes.facecolor": C["bg"], "savefig.facecolor": C["bg"],
        "text.color": C["text"], "axes.titlecolor": C["text"],
        "axes.labelcolor": C["context"], "axes.edgecolor": C["context"],
        "xtick.color": C["context"], "ytick.color": C["context"],
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": False, "grid.color": C["grid"],
        "axes.prop_cycle": cycler(color=[C["primary"], C["text"], C["context"]]),
        "legend.frameon": False,
    })


def use_plotly():
    import plotly.graph_objects as go
    import plotly.io as pio
    pio.templates["jh"] = go.layout.Template(layout=dict(
        font=dict(family="Arial, sans-serif", color=C["text"]),
        paper_bgcolor=C["bg"], plot_bgcolor=C["bg"],
        colorway=[C["primary"], C["text"], C["context"]],
        xaxis=dict(showgrid=False, linecolor=C["context"], tickfont=dict(color=C["context"]), zeroline=False),
        yaxis=dict(gridcolor=C["grid"], linecolor=C["context"], tickfont=dict(color=C["context"]), zeroline=False),
    ))
    pio.templates.default = "jh"


def gradient(n):
    """n odstínů plynule od primary po context-light (více kategorií bez duhy)."""
    a = [int(C["primary"][i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(C["context_light"][i:i + 2], 16) for i in (1, 3, 5)]
    t = [i / max(n - 1, 1) for i in range(n)]
    return ["#%02x%02x%02x" % tuple(round(x + (y - x) * k) for x, y in zip(a, b)) for k in t]
