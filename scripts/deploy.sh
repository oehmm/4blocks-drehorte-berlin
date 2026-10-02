#!/bin/sh
# Handy-Versionen aller Serien neu zusammensetzen und über GitHub Pages (Ordner docs/) veröffentlichen.
set -e
cd "$(dirname "$0")/.."
for d in serien/*/; do
  slug=$(basename "$d"); [ "$slug" = "_vorlage" ] && continue
  SERIE="$slug" python3 scripts/assemble.py
done
git add -A
git commit -m "Karten aktualisieren" || echo "Keine Änderungen."
git push
echo "Live in 1–2 Minuten:"; for d in serien/*/; do s=$(basename "$d"); [ "$s" = "_vorlage" ] && continue; [ "$s" = "4blocks" ] && echo "  https://oehmm.github.io/4blocks-drehorte-berlin/" || echo "  https://oehmm.github.io/4blocks-drehorte-berlin/$s/"; done
