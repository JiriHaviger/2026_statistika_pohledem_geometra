"""
Kalkulačka pro agenty: spustí krátký Python v samostatném procesu a vrátí vypsaný výstup.

Agenti (jazykové modely) aritmeticky chybují, proto všechny číselné výsledky počítá tento nástroj.
Dostupné: numpy (np), scipy.stats (stats), math, statistics, fractions, itertools, functools.

UPOZORNĚNÍ: je to pojistka proti nehodám, ne bezpečnostní sandbox. Chrání před náhodným
čtením souborů a importem síťových modulů, ale NE před úmyslně škodlivým kódem.
Proces běží s `python -I`, s prázdným prostředím (bez API klíče), v prázdném dočasném
adresáři, s limitem času a délky výstupu. Modul nemá závislosti na crewai.
"""

import os
import subprocess
import sys
import tempfile

TIMEOUT_SECONDS = 30            # první import scipy po instalaci umí trvat i přes 10 s
MAX_OUTPUT_CHARS = 4000

# Kód, který se spustí v podprocesu. Uživatelský kód dostane omezené builtins:
# bez open/exec/eval a s importem jen povolených modulů. Knihovny samotné běží s plnými
# builtins (omezení platí jen pro kód napsaný agentem).
_RUNNER = r'''
import builtins, fractions, functools, itertools, math, statistics, sys, traceback
import numpy as np
import scipy.stats as stats

ALLOWED = {"math", "statistics", "fractions", "itertools", "functools", "numpy", "scipy"}
BLOCKED = {"open", "exec", "eval", "compile", "input", "breakpoint", "exit", "quit", "help",
           "memoryview", "__loader__", "__spec__"}
# Čtení a zápis souborů přes numpy
for name in ("load", "loadtxt", "genfromtxt", "fromfile", "memmap", "save", "savetxt",
             "savez", "savez_compressed", "fromregex"):
    if hasattr(np, name):
        def _denied(*args, _name=name, **kwargs):
            raise PermissionError(f"np.{_name}: práce se soubory není povolena")
        setattr(np, name, _denied)

real_import = builtins.__import__
def safe_import(name, globals=None, locals=None, fromlist=(), level=0):
    if level != 0 or name.split(".")[0] not in ALLOWED:
        raise ImportError(f"import {name} není povolen (povoleno: {', '.join(sorted(ALLOWED))})")
    return real_import(name, globals, locals, fromlist, level)

safe_builtins = {k: v for k, v in vars(builtins).items() if k not in BLOCKED}
safe_builtins["__import__"] = safe_import
namespace = {"__builtins__": safe_builtins, "np": np, "numpy": np, "stats": stats, "math": math,
             "statistics": statistics, "fractions": fractions, "itertools": itertools,
             "functools": functools}

code = sys.stdin.read()
try:
    exec(compile(code, "<calc>", "exec"), namespace)
except BaseException:
    tb = traceback.format_exc().strip().splitlines()
    print("\n".join(tb[-6:]), file=sys.stderr)
    sys.exit(1)
'''


def _kill_tree(process: subprocess.Popen) -> None:
    """Ukončí proces i s potomky. Na Windows venv spouští skutečný Python jako potomka
    launcheru, a samotné kill() by ho nechalo běžet."""
    if os.name == "nt":
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(process.pid)],
                       capture_output=True, check=False)
    else:
        process.kill()


def run_calc(code: str, timeout: int = TIMEOUT_SECONDS) -> str:
    """Spustí `code` a vrátí text výstupu. Výsledky musí kód vypsat příkazem print().
    Chyby se vrací jako text začínající „CHYBA:“ (nevyvolávají výjimku)."""
    if not code.strip():
        return "CHYBA: prázdný kód."
    env = {"SYSTEMROOT": os.environ.get("SYSTEMROOT", "")} if os.name == "nt" else {}
    with tempfile.TemporaryDirectory() as workdir:
        process = subprocess.Popen(
            [sys.executable, "-I", "-c", _RUNNER],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, encoding="utf-8", errors="replace", cwd=workdir, env=env,
        )
        try:
            stdout, stderr = process.communicate(code, timeout=timeout)
        except subprocess.TimeoutExpired:
            _kill_tree(process)
            process.communicate()
            return f"CHYBA: výpočet překročil limit {timeout} s a byl přerušen."

    if process.returncode != 0:
        return "CHYBA:\n" + (stderr.strip() or f"proces skončil s kódem {process.returncode}")
    output = stdout.strip()
    if not output:
        return "CHYBA: kód nic nevypsal. Výsledky vypiš příkazem print()."
    if len(output) > MAX_OUTPUT_CHARS:
        output = output[:MAX_OUTPUT_CHARS] + f"\n… (výstup zkrácen na {MAX_OUTPUT_CHARS} znaků)"
    return output
