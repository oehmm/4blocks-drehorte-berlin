import functools,json,urllib.request,urllib.parse,sys,time
B='52.445,13.340,52.532,13.480'
Q={
'roads':f'way["highway"~"^(motorway|trunk|primary|secondary|tertiary|residential|unclassified|living_street|motorway_link|trunk_link|primary_link|pedestrian)$"]({B});',
'green':f'(way["leisure"~"park|garden"]({B});relation["leisure"="park"]({B});way["landuse"~"cemetery|grass|allotments|forest|recreation_ground"]({B});way["natural"="wood"]({B}););',
'water':f'(way["natural"="water"]({B});relation["natural"="water"]({B});way["waterway"~"river|canal"]({B}););',
'rail':f'way["railway"~"^(rail|subway|light_rail)$"]["tunnel"!="yes"]({B});',
'admin':f'relation["boundary"="administrative"]["admin_level"~"^(9|10)$"]({B});',
'poi':f'(way["name"~"Michael-Bohnen-Ring|Görlitzer Park|Volkspark Hasenheide|Kottbusser Tor"]({B});node["name"="Kottbusser Tor"]["railway"="station"]({B});relation["name"~"Görlitzer Park|Hasenheide"]({B});way["name"~"^(Sonnenallee|Karl-Marx-Straße|Hermannstraße|Fuldastraße|Donaustraße)$"]["highway"]({B}););',
'stations':f'node["railway"="station"]({B});',
}
EP=['https://overpass.private.coffee/api/interpreter','https://overpass-api.de/api/interpreter']
for k in (sys.argv[1:] or Q):
    q=f'[out:json][timeout:180];{Q[k]}out geom;'
    for ep in EP:
        try:
            d=urllib.request.urlopen(urllib.request.Request(ep,data=urllib.parse.urlencode({'data':q}).encode(),headers={'User-Agent':'4blocks-karte/1.0'}),timeout=200).read()
            open(f'osm/{k}.json','wb').write(d); print(k,len(json.loads(d)['elements'])); break
        except Exception as e: print(k,ep,e); time.sleep(3)
