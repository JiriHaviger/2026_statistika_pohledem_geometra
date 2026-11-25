// Paleta JHRules pro OJS grafy.
// Barvy se čtou z CSS proměnných --jh-* (definuje je hag_custom.scss),
// takže změna palety nevyžaduje úpravu žádné kapitoly.
// Záložní hodnoty platí, jen kdyby CSS proměnné chyběly.
//
// Použití v kapitole (jednou, v první {ojs} buňce; cesta je relativní k souboru kapitoly):
//   import {C, gradient, plotStyle} from "../assets/jhrules.js"
//   Plot.plot({ marks: [Plot.barY(data, {x: "k", y: "p", fill: C.primary})] })

const FALLBACK = {
  bg: "#FFFFFF", text: "#3D3D3D", primary: "#4682B4", primaryLight: "#A9C6DE",
  primaryText: "#3D729E", accent: "#C46F26", context: "#7F7F7F",
  contextLight: "#D3D3D3", grid: "#EBEBEB", warning: "#A8402F",
  primaryDark: "#2F5D84", green: "#6B8E23", greenDark: "#475F1A"
};

// primaryLight → --jh-primary-light
const cssName = (key) => "--jh-" + key.replace(/[A-Z]/g, (m) => "-" + m.toLowerCase());

function readPalette() {
  const style = getComputedStyle(document.documentElement);
  const palette = {};
  for (const [key, fallback] of Object.entries(FALLBACK)) {
    palette[key] = style.getPropertyValue(cssName(key)).trim() || fallback;
  }
  return palette;
}

export const C = readPalette();

// Přepnutí světlého/tmavého režimu (tlačítko Quarto v postranním panelu): barvy se čtou jednou při načtení
// a plátna se kreslí jejich hodnotami, proto se stránka po přepnutí načte znovu (volba režimu se pamatuje).
// Poslouchá se jen kliknutí na přepínač, nic se nehlídá v pozadí, takže nemůže vzniknout smyčka.
if (typeof document !== "undefined" && !window.__jhSchemeReload) {
  window.__jhSchemeReload = true;
  document.addEventListener("click", (e) => {
    if (e.target.closest && e.target.closest(".quarto-color-scheme-toggle")) {
      setTimeout(() => window.location.reload(), 200);
    }
  });
}

// Společný styl Observable Plot podle JHRules: průhledné pozadí, text v barvě text,
// Arial, popisky 12 px. Použití: Plot.plot({ style: plotStyle, ... })
// Další pravidla (bez horní a pravé osy, mřížka jen ve směru čtení hodnot, bez rámečku
// legendy) se řeší v kódu grafu, viz docs_for_agents/jhrules/README.md.
export const plotStyle = {
  background: "transparent",
  color: C.text,
  fontFamily: "Arial, Helvetica, sans-serif",
  fontSize: "12px"
};

// n odstínů plynule od primary po contextLight (více kategorií bez duhy)
export function gradient(n) {
  const parse = (hex) => [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16));
  const a = parse(C.primary), b = parse(C.contextLight);
  return Array.from({length: n}, (_, i) => {
    const t = i / Math.max(n - 1, 1);
    return "#" + a.map((x, j) => Math.round(x + (b[j] - x) * t).toString(16).padStart(2, "0")).join("");
  });
}
