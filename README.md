# Drehorte-Karten

Interaktive Karten mit Drehorten von Serien, als Handy-App (PWA) und als Claude-Artifact.
Erste Serie: **4 Blocks** – https://oehmm.github.io/4blocks-drehorte-berlin/

Funktionen: Karte mit selbst gezeichneter OSM-Basiskarte, Fotos von Wikimedia Commons, Szenenbilder hochladen
(Vergleichsregler), Figurenseiten, Rundgang mit echten Fußwegen und GPS-Navigation, „In der Nähe“, eigene Drehorte
und Beschreibungen, Geräte-Abgleich (Cloudflare Worker, `sync-worker/`), Offline-Paket.

## Aufbau

```
serien/<slug>/serie.py   alles Serienspezifische: Orte, Figuren, Arten, Rundgang, Fotos, Texte, Kartenausschnitt
serien/<slug>/osm, raw   heruntergeladene Rohdaten (nicht im Repo)
serien/<slug>/out        erzeugte Daten (bei 4blocks ein Link auf site/ = Artifact-Ordner)
serien/<slug>/eigene.json übernommene eigene Einträge (scripts/import_eigene.py)
site/4blocks-karte.html  die App-Seite (für alle Serien gleich, liest Texte aus drehorte.json)
docs/                    GitHub Pages: 4 Blocks im Hauptordner, weitere Serien unter docs/<slug>/
```

## Neue Serie anlegen

```sh
scripts/neue-serie.sh dogs-of-berlin        # legt serien/dogs-of-berlin/serie.py aus der Vorlage an
# serie.py ausfüllen (Orte, Figuren, Kartenausschnitt …), dann:
SERIE=dogs-of-berlin python3 scripts/fetch.py
SERIE=dogs-of-berlin python3 scripts/geocode.py
SERIE=dogs-of-berlin python3 scripts/photos.py
SERIE=dogs-of-berlin python3 scripts/build.py
scripts/deploy.sh
```

## Eigene Einträge übernehmen

```sh
python3 scripts/import_eigene.py               # zeigt neue Orte/Texte aus Abgleich und Artifact-Export
python3 scripts/import_eigene.py --uebernehmen # schreibt serien/4blocks/eigene.json
python3 scripts/build.py && scripts/deploy.sh
```

Kartendaten © OpenStreetMap-Mitwirkende (ODbL). Fotos: Wikimedia Commons, Lizenzen in der App.
