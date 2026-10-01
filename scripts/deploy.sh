#!/bin/sh
# Baut die Handy-Version neu und veröffentlicht sie über GitHub Pages (Ordner docs/).
set -e
cd "$(dirname "$0")/.."
python3 scripts/assemble.py
git add -A
git commit -m "4 Blocks Karte aktualisieren" || echo "Keine Änderungen."
git push
echo "Live in 1–2 Minuten: https://oehmm.github.io/4blocks-drehorte-berlin/"
