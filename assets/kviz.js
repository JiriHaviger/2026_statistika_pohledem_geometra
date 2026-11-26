// Kvíz „Otestujte se“ s okamžitou zpětnou vazbou. Rozložení: zadání | možné odpovědi | výsledek.
//
// Použití v kapitole (dvě buňky, import musí být sám):
//   import {kviz} from "../assets/kviz.js"
//   kviz([
//     {zadani: "Delší zadání příkladu, odstavce se oddělují \n.", tabulka: [["x", "n"], [0, 3], [1, 5]]},
//     {q: "Otázka", options: ["A", "B", "C"], correct: 1, why: "Vysvětlení po správné odpovědi."},
//     ...
//   ])
//
// Položka se `zadani` (a volitelnou `tabulka`, první řádek je hlavička) je text přes celou šířku,
// položky s `q` jsou otázky. Odpověď lze měnit. Krátké odpovědi se vybírají z rozbalovacího seznamu,
// dlouhé jako přepínače pod sebou. Na úzké obrazovce se odpovědi a komentář zarovnají doprava.
// Barvy: modrá = správně, cihlová = špatně (viz animace-konvence.md).

import {C} from "./jhrules.js";

const CSS = `
.kviz-radek { display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 4fr) minmax(0, 4fr);
  gap: 4px 16px; align-items: center; padding: 8px 0; border-bottom: 1px solid var(--kviz-cara); }
.kviz-radek:last-of-type { border-bottom: none; }
.kviz-odpovedi label { display: block; margin: 1px 0; cursor: pointer; }
.kviz-vysledek { font-size: 0.95em; }
.kviz-komentar { display: block; font-size: 0.9em; margin-top: 2px; }
@media (max-width: 640px) {
  .kviz-radek { grid-template-columns: 1fr; }
  .kviz-odpovedi, .kviz-vysledek { justify-self: end; text-align: right; }
}`;

function odstavce(text) {
  const frag = document.createDocumentFragment();
  String(text).split("\n").forEach((t) => {
    const p = document.createElement("p");
    p.textContent = t;
    p.style.margin = "0.4rem 0";
    frag.appendChild(p);
  });
  return frag;
}

function tabulka(rows) {
  const t = document.createElement("table");
  t.style.cssText = "border-collapse: collapse; margin: 0.4rem 0 0.6rem 0; font-size: 0.95em;";
  rows.forEach((r, i) => {
    const tr = document.createElement("tr");
    r.forEach((cell) => {
      const td = document.createElement(i === 0 ? "th" : "td");
      td.textContent = cell;
      td.style.cssText = `padding: 2px 14px 2px 0; text-align: left; ${i === 0 ? `border-bottom: 1px solid ${C.context}; font-weight: 700;` : ""}`;
      tr.appendChild(td);
    });
    t.appendChild(tr);
  });
  return t;
}

export function kviz(items) {
  const root = document.createElement("div");
  root.style.cssText = "margin: 0.5rem 0 0.5rem 0;";
  root.style.setProperty("--kviz-cara", C.contextLight);
  const style = document.createElement("style");
  style.textContent = CSS;
  root.appendChild(style);

  const stav = [];            // true, pokud je otázka zodpovězena správně
  const souhrn = document.createElement("div");
  souhrn.style.cssText = `text-align: right; font-size: 0.9em; color: ${C.context}; margin-top: 0.3rem;`;
  const obnovSouhrn = () => {
    souhrn.textContent = `Správně: ${stav.filter(Boolean).length} z ${stav.length}`;
  };

  items.forEach((item, i) => {
    if (item.zadani !== undefined) {
      const box = document.createElement("div");
      box.style.cssText = "margin: 0.9rem 0 0.2rem 0;";
      box.appendChild(odstavce(item.zadani));
      if (item.tabulka) box.appendChild(tabulka(item.tabulka));
      root.appendChild(box);
      return;
    }

    const idx = stav.length;
    stav.push(false);
    const cislo = idx + 1;

    const radek = document.createElement("div");
    radek.className = "kviz-radek";

    const otazka = document.createElement("div");
    otazka.textContent = `${cislo}. ${item.q}`;

    const odpovedi = document.createElement("div");
    odpovedi.className = "kviz-odpovedi";
    const vysledek = document.createElement("div");
    vysledek.className = "kviz-vysledek";
    vysledek.setAttribute("aria-live", "polite");

    const vyhodnot = (k) => {
      vysledek.replaceChildren();
      if (k < 0) { stav[idx] = false; obnovSouhrn(); return; }
      const ok = k === item.correct;
      stav[idx] = ok;
      const verdikt = document.createElement("span");
      verdikt.textContent = ok ? "✓ správně" : "✗ zkuste to znovu";
      verdikt.style.color = ok ? C.primaryText : C.warning;
      vysledek.appendChild(verdikt);
      if (ok && item.why) {
        const komentar = document.createElement("span");
        komentar.className = "kviz-komentar";
        komentar.textContent = item.why;
        komentar.style.color = C.context;
        vysledek.appendChild(komentar);
      }
      obnovSouhrn();
    };

    const kratke = item.options.every((o) => String(o).length <= 30);
    if (kratke) {
      const sel = document.createElement("select");
      ["—", ...item.options].forEach((o) => {
        const opt = document.createElement("option");
        opt.textContent = o;
        sel.appendChild(opt);
      });
      sel.addEventListener("change", () => vyhodnot(sel.selectedIndex - 1));
      odpovedi.appendChild(sel);
    } else {
      const skupina = `kviz-${Math.random().toString(36).slice(2)}-${idx}`;
      item.options.forEach((o, k) => {
        const lab = document.createElement("label");
        const inp = document.createElement("input");
        inp.type = "radio";
        inp.name = skupina;
        inp.style.marginRight = "6px";
        inp.addEventListener("change", () => vyhodnot(k));
        lab.appendChild(inp);
        lab.appendChild(document.createTextNode(o));
        odpovedi.appendChild(lab);
      });
    }

    radek.append(otazka, odpovedi, vysledek);
    root.appendChild(radek);
  });

  obnovSouhrn();
  root.appendChild(souhrn);
  return root;
}
