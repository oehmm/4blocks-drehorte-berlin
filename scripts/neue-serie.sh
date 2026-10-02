#!/bin/sh
# Neue Serie anlegen: scripts/neue-serie.sh <slug>   (z. B. dogs-of-berlin)
set -e
cd "$(dirname "$0")/.."
slug="$1"; [ -z "$slug" ] && { echo "Aufruf: scripts/neue-serie.sh <slug>"; exit 1; }
[ -e "serien/$slug" ] && { echo "serien/$slug gibt es schon."; exit 1; }
mkdir -p "serien/$slug"
sed "s/slug='vorlage'/slug='$slug'/; s/store='serie',  idb='serie'/store='$slug', idb='$slug'/" serien/_vorlage/serie.py > "serien/$slug/serie.py"
echo "Angelegt: serien/$slug/serie.py – jetzt ausfüllen, dann:"
echo "  SERIE=$slug python3 scripts/fetch.py && SERIE=$slug python3 scripts/geocode.py"
echo "  SERIE=$slug python3 scripts/photos.py && SERIE=$slug python3 scripts/build.py"
echo "  scripts/deploy.sh   ->  https://oehmm.github.io/4blocks-drehorte-berlin/$slug/"
