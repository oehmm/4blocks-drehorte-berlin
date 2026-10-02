# Drehort-Daten Dogs of Berlin (Netflix, 2018, Christian Alvart). Öffentlich sind nur wenige Drehorte
# konkret belegt; jeder Eintrag nennt seine Quelle.

S={
 'bz':['Bezirksamt Steglitz-Zehlendorf','https://www.berlin.de/ba-steglitz-zehlendorf/ueber-den-bezirk/sehens-und-wissenswertes/den-bezirk-entdecken/film-ab/bierpinsel-dogs-of-berlin-1395191.php'],
 'taz':['taz','https://taz.de/Die-Kahlschlagsanierung-wird-Serienheld/!5557473/'],
 'tb':['tittelbach.tv','https://www.tittelbach.tv/kritiken/dogs-of-berlin/'],
 'ts':['Tagesspiegel','https://www.tagesspiegel.de/gesellschaft/medien/fernsehkataloghundehutte-4018207.html'],
 'wp':['Wikipedia','https://de.wikipedia.org/wiki/Dogs_of_Berlin'],
}

# kat: polizei | wohnen | fussball | kiez
ORTE=[
 dict(id='bierpinsel',n='Bierpinsel',kat='polizei',geo='pt:bierpinsel',kiez='Steglitz',
      adr='Schloßstraße 17, 12163 Berlin',st='U Schloßstraße · S+U Rathaus Steglitz',
      rolle='Der knallbunte Pop-Art-Turm über der Schloßstraße wird in der Serie zum Sitz der Soko „Rote Karte“ des Landeskriminalamts, die den Mord an Fußballstar Orkan Erdem aufklären soll.',
      tipp='Der Turm von 1976 steht seit Jahren weitgehend leer. Am besten von der Brücke der Schloßstraße aus ansehen.',
      fig=['Erol','Kurt'],staffel='S1',q=['bz','taz']),
 dict(id='lokdepot',n='Roter Neubau Am Lokdepot',kat='wohnen',geo='pt:lokdepot',kiez='Schöneberg',
      adr='Am Lokdepot / Monumentenstraße, 10965 Berlin',st='U+S Yorckstraße',
      rolle='Aus seiner schicken Eigentumswohnung im knallroten Neubau am Lokdepot blickt Polizist Erol Birkan über die Gleise. Die preisgekrönte Wohnanlage ist komplett rot, vom gefärbten Beton bis zu den Geländern.',
      tipp='Private Wohnhäuser. Gut zu sehen vom Weg am Park am Gleisdreieck.',
      geocode='Monumentenstraße 15, 10965 Berlin',
      fig=['Erol'],staffel='S1',q=['taz']),
 dict(id='olympiastadion',n='Olympiastadion',kat='fussball',geo='pt:olympiastadion',kiez='Westend',
      adr='Olympischer Platz 3, 14053 Berlin',st='U Olympia-Stadion · S Olympiastadion',
      rolle='Hier spielt das große Fußball-Länderspiel, vor dem der Nationalspieler Orkan Erdem ermordet wird. Die Spielszenen im Stadion bilden den Rahmen der ganzen Serie.',
      alt='Die Kritiken erwähnen die Bilder vom Fußballspiel im Olympiastadion. Ob alle Stadionszenen vor Ort gedreht wurden, ist nicht belegt.',
      fig=['Erol','Kurt'],staffel='S1',q=['tb','ts']),
 dict(id='marzahn',n='Großsiedlung Marzahn',kat='wohnen',geo='pt:marzahn',radius=600,kiez='Marzahn',
      adr='Marzahner Promenade, 12679 Berlin',st='S Marzahn',
      rolle='Drehort Marzahn: In der Plattenbausiedlung wird die Leiche von Orkan Erdem gefunden, und hier lebt Kurt Grimmers zweite Familie mit seiner Geliebten Bine. Auch die Neonazis, die unter Verdacht geraten, stammen aus Marzahn.',
      alt='Die genaue Drehstelle in Marzahn ist nicht veröffentlicht. Der Kreis markiert das Zentrum der Großsiedlung.',
      fig=['Kurt','Bine'],staffel='S1',q=['ts','tb']),
 dict(id='olfe',n='Kiosk gegenüber Möbel Olfe',kat='kiez',geo='pt:olfe',kiez='Kreuzberg',
      adr='Reichenberger Straße, gegenüber Nr. 177, 10999 Berlin',st='U Kottbusser Tor',
      rolle='Ein kleiner Zigarettenladen gegenüber der Bar „Möbel Olfe“ am Kottbusser Tor ist Schauplatz einer Szene.',
      alt='Welche Szene genau, nennt die Quelle nicht. Die Position ist ungefähr.',
      geocode='Reichenberger Straße 177, 10999 Berlin',
      fig=[],staffel='S1',q=['taz']),
]

# Figuren (Besetzung laut Wikipedia und tittelbach.tv)
FIG={
 'Erol':dict(name='Erol Birkan',actor='Fahri Yardım',rolle='Polizist, türkischstämmig',
   bio='Erol ist Polizist mit türkischen Wurzeln und ermittelt mit Kurt Grimmer im Mord an Orkan Erdem. Er ist schwul und wuchs im selben Kiez auf wie der Chef eines arabischen Clans.'),
 'Kurt':dict(name='Kurt Grimmer',actor='Felix Kramer',rolle='Ermittler der Mordkommission',
   bio='Kurt stammt aus dem Osten Berlins, ist spielsüchtig und führt ein Doppelleben zwischen seiner Familie und seiner Geliebten in Marzahn. Er ermittelt mit Erol Birkan.'),
 'Paula':dict(name='Paula Grimmer',actor='Katharina Schüttler',rolle='Kurts Frau',bio='Paula ist Kurt Grimmers Frau.'),
 'Bine':dict(name='Sabine „Bine“ Ludar',actor='Anna Maria Mühe',rolle='Kurts Geliebte',bio='Bine ist Kurt Grimmers Geliebte, mit der er in Marzahn eine zweite Familie hat.'),
 'Tarik':dict(name='Tarik-Amir',actor='Sinan Farhangmehr',rolle='Clanchef',bio='Tarik-Amir ist der Chef eines arabischen Clans und kennt Erol aus Kindertagen.'),
 'Eva':dict(name='Kurts Mutter',actor='Katrin Sass',rolle='Kurts Mutter',bio='Kurt Grimmers Mutter.'),
}

KAT={
 'polizei':['Polizei & Ermittlung','--k-justiz'],
 'wohnen':['Wohnorte der Figuren','--k-clan'],
 'fussball':['Fußball','--k-revier'],
 'kiez':['Straßen & Kiez','--k-kiez'],
}

TOUR=[]  # die Orte liegen zu weit auseinander für einen Rundgang

FOTOS={
 'bierpinsel':['B-Steglitz Okt12 Bierpinsel.jpg',1],
 'lokdepot':['Monumentenstraße, Berlin (13452628113).jpg',0],
 'olympiastadion':['Olympiastadion Berlin 2015.jpg',1],
 'marzahn':['Plattenbau Marzahn.jpg',0],
 'olfe':['Moebel olfe reichenbach-str-177 2023-09-03.png',0],
}

META=dict(
  slug='dogs-of-berlin', short='Dogs of Berlin',
  title='Dogs of Berlin Drehorte', h1='Dogs of Berlin', h1b='Drehorte',
  eyebrow='Netflix · 2018 · Berlin',
  intro='Schauplätze der Netflix-Serie um den Mord an Fußballstar Orkan Erdem, vom Bierpinsel bis nach Marzahn.',
  description='Die Berliner Drehorte der Netflix-Serie Dogs of Berlin auf einer Karte, mit Fotos und Figuren.',
  credit='Dogs of Berlin (Netflix / Syrreal Entertainment)',
  note='Einige Orte sind Wohnhäuser. Bitte nur von der Straße aus ansehen und die Bewohner in Ruhe lassen.',
  sources=[[S[k][0],S[k][1]] for k in ('bz','taz','tb','ts')],
  tourTab='Rundgang', tourTitle='', tourIntro='',
  store='dob', idb='dogs-of-berlin',
  lat=52.50,
  bbox='52.440,13.225,52.555,13.580',
  road_classes='motorway|trunk|primary|secondary|tertiary|motorway_link|trunk_link|primary_link',
  extra_bboxes=['52.452,13.312,52.462,13.330','52.487,13.360,52.498,13.380','52.508,13.225,52.522,13.255','52.536,13.535,52.552,13.565','52.495,13.410,52.505,13.428'],
  walk_bbox='',
  maxBounds=[[52.40,13.15],[52.60,13.65]],
  admin_label=None,
  root=False,
)
