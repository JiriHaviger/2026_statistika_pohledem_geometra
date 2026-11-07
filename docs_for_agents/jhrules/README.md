# JH Rules

Designový systém pro výukové materiály z kvantitativních metod (vysokoškolská matematika a statistika) a pro datové analýzy. Platí pro všechny výstupy: grafy v matplotlib a plotly, Quarto stránky a slidy, interaktivní prvky v OJS a animace ve stylu manim (3Blue1Brown).

## Principy

- **Čistý design.** Bílé pozadí, tlumeně tmavě šedý text (ne čistá černá – menší tvrdost kontrastu), žádné rámečky, stíny ani přechody.
- **Jedna akcentová barva.** `primary` (steelblue) nese veškerý důraz a nemusí se šetřit.
- **Výjimka je výjimka.** `accent` (dark orange) zvýrazňuje jen jeden prvek: bod, sloupec, výsledek, „aha“ moment animace.
- **Kontext ustupuje.** Osy, popisky a potlačená data jsou v šedé (`context`, `context-light`), aby vynikla data.
- **Zvýraznění místo duhy.** Víc kategorií se řeší tak, že jedna je `primary` a zbytek `context-light`, ne paletou mnoha barev. Pokud je třeba, pak plynulým stupňováním od primary  po context-light.

## Barvy

| Role | Token | Hex | Kdy |
|---|---|---|---|
| Pozadí | `bg` | `#FFFFFF` | vždy |
| Text a základ | `text` | `#3d3d3d` | text, nadpisy, rovnice, běžné prvky |
| Hlavní highlight | `primary` | `#4682B4` | hlavní data, odkazy, pojmy |
| Světlá primární | `primary-light` | `#A9C6DE` | výplně, pásy CI |
| Výjimečný highlight | `accent` | `#D35400` | jeden prvek na graf |
| Kontext tmavý | `context` | `#7F7F7F` | osy, ticky, popisky, sekundární text |
| Kontext světlý | `context-light` | `#D3D3D3` | potlačená data, pomocné konstrukce |
| Mřížka | `grid` | `#EBEBEB` | grid, linky tabulek |

Přístupnost: `primary` a `accent` mají na bílé kontrast kolem 4:1 a `context` 3,9:1, tedy pod hranicí 4,5:1 pro běžný text. Text v těchto barvách používejte tučně nebo od 18px. `context` je záměrně slabší a slouží jen pro popisky os, ne pro hlavní text.

## Typografie

Arial (sans-serif) pro vše, monospace jen pro kód. Nadpisy `display`, `h1`–`h3` jsou tučné v barvě `text`. Popisky os (`axis-label`, 12px) a popisky obrázků (`caption`, 13px) jsou v barvě `context`.

## Grafy

- Bez horní a pravé osy. Mřížka žádná nebo jemná (`grid`), jen ve směru čtení hodnot.
- Legendy bez rámečku, raději přímé popisky u čar.
- Hlavní řada `primary`, srovnávací řada `text` nebo `context`, potlačené řady `context-light`.
- `accent` nejvýše na jeden prvek, např. pozorování, odhad nebo kritickou hodnotu.

### matplotlib

```python
import matplotlib.pyplot as plt
from cycler import cycler

COLOR_BG            = "#FFFFFF"
COLOR_TEXT          = "#3d3d3d"
COLOR_PRIMARY       = "#4682B4"   # steelblue
COLOR_PRIMARY_LIGHT = "#A9C6DE"
COLOR_ACCENT        = "#D35400"   # dark orange
COLOR_CONTEXT       = "#7F7F7F"
COLOR_CONTEXT_LIGHT = "#D3D3D3"
COLOR_GRID          = "#EBEBEB"

plt.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Arial", "DejaVu Sans"],
    "figure.facecolor": COLOR_BG, "axes.facecolor": COLOR_BG, "savefig.facecolor": COLOR_BG,
    "text.color": COLOR_TEXT, "axes.titlecolor": COLOR_TEXT,
    "axes.labelcolor": COLOR_CONTEXT, "axes.edgecolor": COLOR_CONTEXT,
    "xtick.color": COLOR_CONTEXT, "ytick.color": COLOR_CONTEXT,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": False, "grid.color": COLOR_GRID,
    "axes.prop_cycle": cycler(color=[COLOR_PRIMARY, COLOR_TEXT, COLOR_CONTEXT]),
    "legend.frameon": False,
})
```

### plotly

```python
import plotly.graph_objects as go, plotly.io as pio

pio.templates["jh"] = go.layout.Template(layout=dict(
    font=dict(family="Arial, sans-serif", color=COLOR_TEXT),
    paper_bgcolor=COLOR_BG, plot_bgcolor=COLOR_BG,
    colorway=[COLOR_PRIMARY, COLOR_TEXT, COLOR_CONTEXT],
    xaxis=dict(showgrid=False, linecolor=COLOR_CONTEXT, tickfont=dict(color=COLOR_CONTEXT), zeroline=False),
    yaxis=dict(gridcolor=COLOR_GRID, linecolor=COLOR_CONTEXT, tickfont=dict(color=COLOR_CONTEXT), zeroline=False),
))
pio.templates.default = "jh"
```

### Quarto (SCSS)

```scss
/*-- scss:defaults --*/
$body-bg: #FFFFFF;
$body-color: #3d3d3d;
$headings-color: #3d3d3d;
$primary: #4682B4;
$link-color: #4682B4;
$font-family-sans-serif: Arial, sans-serif;

/*-- scss:rules --*/
.accent { color: #D35400; font-weight: 700; }
.muted  { color: #7F7F7F; }
```

### OJS / Observable Plot

```js
C = ({bg: "#FFFFFF", text: "#3d3d3d", primary: "#4682B4", primaryLight: "#A9C6DE",
      accent: "#D35400", context: "#7F7F7F", contextLight: "#D3D3D3", grid: "#EBEBEB"})
```

## Animace (manim / 3b1b)

Pozadí je bílé, objekty a rovnice v barvě `text`. Hlavní objekt je `primary`, pomocné konstrukce `context` nebo `context-light`. Jeden klíčový moment (výsledek, protnutí, odhad) je `accent`. Přechody jsou plynulé a textu je co nejméně.