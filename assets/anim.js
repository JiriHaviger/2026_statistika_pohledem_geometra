// Pomocný modul pro canvas animace v OJS (nový soubor, nic stávajícího nemění).
// Barvy bere z jhrules.js. Použití v kapitole (cesta je relativní k souboru kapitoly):
//   import {animation, drawText, clamp, ease} from "../assets/anim.js"
//
// animation({width, height, setup, step, draw, readout, pointer, controls}) vrátí DOM uzel:
//   <canvas> + tlačítka Start/Pauza a Znovu + vlastní ovládací prvky + řádek s popisem.
//   setup(prev)          vytvoří stav (prev je předchozí stav při „Znovu“, jinak null)
//   step(state, ctl)     jeden krok simulace (volá se jen při běhu)
//   draw(ctx, state, w, h, ctl)  vykreslení jednoho snímku
//   readout(state, ctl)  text (nebo DOM uzel) pod obrázkem
//   pointer(state, ev, ctl)  ev = {type: "down"|"move"|"up", x, y, pressed}
//   controls(ctl)        vrátí DOM uzel s vlastními prvky (ctl.state, ctl.redraw(), ctl.running)
// Animace se nespouští sama při prefers-reduced-motion a stojí, když není vidět.

import {C} from "./jhrules.js";

// Šířka sloupce s textem. Vestavěná OJS proměnná `width` v knize měří celou plochu včetně okraje
// (asi dvojnásobek), takže grafy přetékaly doprava. V kapitole se používá jako
//   width = columnWidth(Generators)
// a všechny buňky pak dostávají šířku textového sloupce (sleduje se i změna velikosti okna).
// Pozor: hodnota se oznámí jen tehdy, když se šířka skutečně změnila. ResizeObserver totiž hlásí i změny výšky
// (například když pod animací naskočí text s popisem). Každé oznámení znovu vytvoří všechny buňky, které na šířce
// závisí, a ty zase změní výšku stránky, takže animace donekonečna blikala.
export function columnWidth(Generators) {
  return Generators.observe((notify) => {
    const root = document.querySelector("#quarto-document-content") || document.body;
    let last = null, timer = null;
    const measure = () => {
      const p = Array.from(root.querySelectorAll("p"))
        .find((el) => !el.closest(".column-margin, .callout, aside, table, figure"));
      const w = Math.max(280, Math.floor((p && p.clientWidth) || root.clientWidth || window.innerWidth));
      if (w === last) return;
      last = w;
      notify(w);
    };
    measure();
    // změna šířky okna se zpracuje až po krátké pauze, ať se buňky nepřekreslují při každém pixelu
    const ro = new ResizeObserver(() => { clearTimeout(timer); timer = setTimeout(measure, 120); });
    ro.observe(root);
    return () => { clearTimeout(timer); ro.disconnect(); };
  });
}

export const clamp =(x, lo, hi) => Math.max(lo, Math.min(hi, x));

// plynulý náběh 0 → 1
export const ease = (t) => {
  const u = clamp(t, 0, 1);
  return u * u * (3 - 2 * u);
};

export function drawText(ctx, s, x, y, {align = "left", color = C.text, bold = false, size = 12, baseline = "alphabetic"} = {}) {
  ctx.fillStyle = color;
  ctx.font = `${bold ? "bold " : ""}${size}px Arial, Helvetica, sans-serif`;
  ctx.textAlign = align;
  ctx.textBaseline = baseline;
  ctx.fillText(s, x, y);
}

export function makeButton(label, onclick) {
  const b = document.createElement("button");
  b.type = "button";
  b.textContent = label;
  b.style.cssText = "font:13px Arial,Helvetica,sans-serif;padding:3px 12px;cursor:pointer;" +
    `border:1px solid ${C.contextLight};border-radius:3px;background:${C.bg};color:${C.text}`;
  b.addEventListener("click", onclick);
  return b;
}

export function animation({
  width, height = 300, setup, step, draw, readout, pointer, controls,
  fps = 30, autoplay = true, buttons = true, stepsPerFrame = 1
}) {
  const dpr = window.devicePixelRatio || 1;
  const root = document.createElement("div");
  const canvas = document.createElement("canvas");
  canvas.width = Math.round(width * dpr);
  canvas.height = Math.round(height * dpr);
  canvas.style.width = width + "px";
  canvas.style.height = height + "px";
  canvas.style.display = "block";
  if (pointer) {
    canvas.style.touchAction = "none";
    canvas.style.cursor = "grab";
  }
  const ctx = canvas.getContext("2d");
  ctx.scale(dpr, dpr);

  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  let state = setup(null);
  let running = autoplay && !reduce;
  let visible = true;
  let dirty = true;

  const bar = document.createElement("div");
  bar.style.cssText = "display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:6px 0";
  const info = document.createElement("div");
  info.style.cssText = `font:13px Arial,Helvetica,sans-serif;color:${C.text};min-height:1.5em`;

  const toggle = makeButton(running ? "Pauza" : "Start", () => {
    ctl.running = !running;
  });

  const ctl = {
    get state() { return state; },
    get running() { return running; },
    set running(v) {
      running = v;
      toggle.textContent = running ? "Pauza" : "Start";
      dirty = true;
    },
    redraw() { dirty = true; },
    reset() { state = setup(state); dirty = true; }
  };

  if (buttons) {
    bar.append(toggle, makeButton("Znovu", () => ctl.reset()));
  }
  if (controls) bar.append(controls(ctl));

  function render() {
    ctx.clearRect(0, 0, width, height);
    draw(ctx, state, width, height, ctl);
    if (readout) {
      const t = readout(state, ctl);
      if (typeof t === "string") info.textContent = t;
      else info.replaceChildren(t);
    }
  }

  if (pointer) {
    let pressed = false;
    const send = (type, e) => {
      const r = canvas.getBoundingClientRect();
      pointer(state, {
        type, pressed,
        x: (e.clientX - r.left) * width / r.width,
        y: (e.clientY - r.top) * height / r.height
      }, ctl);
      dirty = true;
    };
    canvas.addEventListener("pointerdown", (e) => {
      pressed = true;
      canvas.setPointerCapture(e.pointerId);
      canvas.style.cursor = "grabbing";
      send("down", e);
    });
    canvas.addEventListener("pointermove", (e) => send("move", e));
    const release = (e) => {
      pressed = false;
      canvas.style.cursor = "grab";
      send("up", e);
    };
    canvas.addEventListener("pointerup", release);
    canvas.addEventListener("pointercancel", release);
  }

  if ("IntersectionObserver" in window) {
    new IntersectionObserver((entries) => {
      visible = entries[entries.length - 1].isIntersecting;
    }).observe(canvas);
  }

  // smyčka se sama zruší, když buňka zanikne (změna posuvníku, změna šířky okna)
  let seen = false;
  const timer = setInterval(() => {
    if (!root.isConnected) {
      if (seen) clearInterval(timer);
      return;
    }
    seen = true;
    if (!visible) return;
    if (running && step) {
      for (let i = 0; i < stepsPerFrame; i++) step(state, ctl);
      dirty = true;
    }
    if (dirty) {
      dirty = false;
      render();
    }
  }, 1000 / fps);

  root.append(canvas, bar, info);
  // první snímek hned, ať popis pod obrázkem nenaskočí až o chvíli později a nezměnil tím výšku stránky
  try { render(); } catch (e) { /* kapitola si případnou chybu ohlásí při dalším snímku */ }
  return root;
}
