# Adressen der Punkt-Drehorte (geo='pt:<schlüssel>') per Nominatim in Koordinaten umrechnen.
# Bereits bekannte Schlüssel in osm/geocode.json bleiben erhalten (Handkorrekturen gehen nicht verloren).
import json,os,time,urllib.request,urllib.parse
from serie_ctx import ctx
SLUG,DIR,SER=ctx()
out=json.load(open('osm/geocode.json')) if os.path.exists('osm/geocode.json') else {}
for o in SER.ORTE:
    typ,key=o['geo'].split(':',1)
    if typ!='pt' or key in out: continue
    q=o.get('geocode') or o['adr'].split(' (')[0]
    u='https://nominatim.openstreetmap.org/search?'+urllib.parse.urlencode({'q':q,'format':'json','limit':1})
    r=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'drehorte-karte/1.0 (personal project)'})))
    out[key]=[float(r[0]['lat']),float(r[0]['lon']),r[0]['display_name']] if r else None
    print(key,out[key]); time.sleep(1.1)
json.dump(out,open('osm/geocode.json','w'),ensure_ascii=False,indent=1)
