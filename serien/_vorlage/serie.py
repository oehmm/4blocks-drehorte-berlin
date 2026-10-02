# Vorlage für eine neue Serie. Kopieren nach serien/<slug>/serie.py und ausfüllen.
# Alles, was die App über die Serie wissen muss, steht hier. Code muss nicht angepasst werden.

# Quellen: Kürzel -> [Name, Link]. In ORTE über q=['kürzel'] referenzieren.
S={
 'bsp':['Beispielquelle','https://example.org/drehorte'],
}

# Drehorte. geo bestimmt die Position:
#   'pt:<schlüssel>'      Adresse aus adr wird per Nominatim gesucht (scripts/geocode.py)
#   'street:<Straße>'     ganze Straße als Linie (optional clip=[min_lon,max_lon])
#   'area:<Name>'         Park/Platz als Fläche (OSM-Name)
#   'corner:<A>|<B>'      Kreuzung zweier Straßen
#   'xy:<lon>,<lat>'      feste Koordinaten
# Optionale Felder: radius (Meter, Kreis um den Punkt), tipp, alt (Hinweis zu Quellenlage), geocode (Suchtext statt adr)
ORTE=[
 dict(id='beispiel1',n='Beispiel-Café',kat='kiez',geo='pt:beispiel1',kiez='Mitte',
      adr='Musterstraße 1, 10115 Berlin',st='U Musterplatz',
      rolle='Was hier gedreht wurde, welche Szene, wer zu sehen ist.',
      fig=['Held'],staffel='S1',q=['bsp']),
]

# Figuren: kurzer Schlüssel -> Angaben. Schlüssel in ORTE.fig verwenden.
FIG={
 'Held':dict(name='Max Muster',actor='Schauspielerin/Schauspieler',rolle='Hauptfigur',bio='Zwei, drei Sätze zur Figur.'),
}

# Arten von Schauplätzen: Schlüssel -> [Bezeichnung, Farb-Token aus der Seite]
# Verfügbare Tokens: --k-clan --k-revier --k-justiz --k-glamour --k-kiez --k-umland
KAT={
 'kiez':['Straßen & Kiez','--k-kiez'],
}

# Rundgang: Orts-IDs in Gehreihenfolge (leer lassen, wenn es keinen gibt)
TOUR=[]

# Fotos von Wikimedia Commons: Ort -> [Dateiname ohne "File:", 1 = zeigt den Drehort / 0 = Umgebung]
FOTOS={}

META=dict(
  slug='vorlage', short='Serie',
  title='Serie Drehorte Berlin', h1='Serie', h1b='Drehorte',
  eyebrow='Sender · Jahre · Stadt',
  intro='Ein Satz, worum es geht.',
  description='Die Drehorte der Serie auf einer Karte.',
  credit='Serie (Sender / Produktion)',
  note='Bitte Anwohner respektieren.',
  sources=[[S[k][0],S[k][1]] for k in S],
  tourTab='Rundgang', tourTitle='Rundgang', tourIntro='Start, Ziel, Länge.',
  store='serie',  idb='serie',       # eindeutig je Serie, danach nie mehr ändern
  lat=52.52,
  bbox='52.50,13.36,52.54,13.42',    # Basiskarte (S,W,N,O), möglichst eng um die Orte
  extra_bboxes=[],                   # Zusatzausschnitte für weit entfernte Orte
  walk_bbox='',                      # Fußwegenetz für den Rundgang (leer: Luftlinie)
  maxBounds=[[52.45,13.25],[52.60,13.55]],
  admin_label=None,                  # Bezirksnamen, die beschriftet werden (None: alle)
  root=False,                        # False: Handy-App unter docs/<slug>/
)
