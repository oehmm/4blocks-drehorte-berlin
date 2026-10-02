# OpenStreetMap-Daten für die Basiskarte, die Drehorte und den Rundgang laden (Overpass).
# Aufruf: SERIE=<slug> python3 scripts/fetch.py [teil ...]   (ohne Teil: alles)
import json,urllib.request,urllib.parse,sys,time
from serie_ctx import ctx
SLUG,DIR,SER=ctx(); M=SER.META; B=M['bbox']
names=set()
for o in SER.ORTE:
    typ,arg=o['geo'].split(':',1)
    if typ in('street','area'): names.add(arg)
    if typ=='corner': names.update(arg.split('|'))
rx='^('+'|'.join(n.replace('(','\\(').replace(')','\\)') for n in sorted(names))+')$' if names else '^$'
Q={
'roads':f'way["highway"~"^(motorway|trunk|primary|secondary|tertiary|residential|unclassified|living_street|motorway_link|trunk_link|primary_link|pedestrian)$"]({B});',
'green':f'(way["leisure"~"park|garden"]({B});relation["leisure"="park"]({B});way["landuse"~"cemetery|grass|allotments|forest|recreation_ground"]({B});way["natural"="wood"]({B}););',
'water':f'(way["natural"="water"]({B});relation["natural"="water"]({B});way["waterway"~"river|canal"]({B}););',
'rail':f'way["railway"~"^(rail|subway|light_rail)$"]["tunnel"!="yes"]({B});',
'admin':f'relation["boundary"="administrative"]["admin_level"~"^(9|10)$"]({B});',
'poi':f'(way["name"~"{rx}"]({B});relation["name"~"{rx}"]({B}););',
'stations':f'node["railway"="station"]({B});',
}
for i,X in enumerate(M.get('extra_bboxes',[])):
    Q[f'x{i}_roads']=f'way["highway"~"^(primary|secondary|tertiary|residential|unclassified|living_street|service|pedestrian)$"]({X});'
    Q[f'x{i}_misc']=f'(way["railway"="rail"]({X});way["natural"="water"]({X});way["leisure"~"park|garden"]({X});way["landuse"~"grass|forest|meadow|allotments"]({X});way["natural"="wood"]({X}););'
if M.get('walk_bbox'):
    W=M['walk_bbox']
    Q['walk']=f'way["highway"]["highway"!~"^(motorway|motorway_link|trunk_link|construction|proposed|raceway|bus_guideway)$"]["access"!~"^(private|no)$"]["foot"!="no"]({W});'
EP=['https://overpass-api.de/api/interpreter','https://overpass.private.coffee/api/interpreter','https://overpass.kumi.systems/api/interpreter','https://overpass-api.de/api/interpreter']
for k in (sys.argv[1:] or Q):
    q=f'[out:json][timeout:180];{Q[k]}out geom;'
    for ep in EP:
        try:
            d=urllib.request.urlopen(urllib.request.Request(ep,data=urllib.parse.urlencode({'data':q}).encode(),headers={'User-Agent':'drehorte-karte/1.0'}),timeout=200).read()
            open(f'osm/{k}.json','wb').write(d); print(k,len(json.loads(d)['elements']),flush=True); break
        except Exception as e: print(k,ep,e,flush=True); time.sleep(3)
