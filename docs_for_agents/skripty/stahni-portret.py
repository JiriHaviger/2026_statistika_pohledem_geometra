# Stažení portrétu z Wikimedia Commons do assets/portrety/ (jen s volnou licencí).
#
# Spuštění z kořene projektu:
#   python docs_for_agents/skripty/stahni-portret.py laplace "Pierre-Simon Laplace"
#   (první argument je název souboru bez přípony, druhý název článku na anglické Wikipedii)
#
# - Bere hlavní obrázek článku a jeho licenci z Commons. Uloží jen "Public domain" a "CC0".
#   Jiné licence (např. CC BY) vypíše a přeskočí, použití s uvedením zdroje musí schválit autor.
# - Uloží náhled široký 320 px jako jpg. Server omezuje počet dotazů (HTTP 429), proto skript čeká a zkouší znovu.
# - V UA je jen obecný název klienta, žádné osobní údaje.

import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

UA = {"User-Agent": "book-research/1.0"}


def get(url):
    for wait in (20, 40, 80, 120):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            print("429, čekám", wait, "s", flush=True)
            time.sleep(wait)
    raise SystemExit("Server pořád odmítá dotazy (429), zkuste později.")


def main(key, title):
    q = urllib.parse.urlencode({"action": "query", "titles": title, "prop": "pageimages",
                                "piprop": "name", "format": "json", "formatversion": 2})
    page = json.loads(get("https://en.wikipedia.org/w/api.php?" + q))["query"]["pages"][0]
    fn = page.get("pageimage")
    if not fn:
        raise SystemExit("Článek nemá hlavní obrázek.")
    time.sleep(8)
    q = urllib.parse.urlencode({"action": "query", "titles": "File:" + fn, "prop": "imageinfo",
                                "iiprop": "extmetadata|url", "iiurlwidth": 320,
                                "format": "json", "formatversion": 2})
    info = json.loads(get("https://commons.wikimedia.org/w/api.php?" + q))["query"]["pages"][0]["imageinfo"][0]
    meta = info["extmetadata"]
    licence = meta.get("LicenseShortName", {}).get("value", "")
    autor = re.sub("<[^>]+>", "", meta.get("Artist", {}).get("value", ""))[:80]
    print(fn, "|", licence, "|", autor)
    if not licence.lower().startswith(("public domain", "cc0")):
        raise SystemExit("Licence není volná dílo, obrázek se neukládá.")
    time.sleep(8)
    data = get(info["thumburl"])
    ext = fn.rsplit(".", 1)[-1].lower()
    path = f"assets/portrety/{key}.{ext}"
    open(path, "wb").write(data)
    print("Uloženo:", path, len(data), "B")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    main(sys.argv[1], sys.argv[2])
