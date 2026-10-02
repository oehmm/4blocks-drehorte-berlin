# Hilfe bei der Fotoauswahl: Commons-Bilder in der Nähe jedes Drehorts auflisten (raw/photo_search.json).
import json,urllib.request,urllib.parse,time
from serie_ctx import ctx
SLUG,DIR,SER=ctx()
UA={'User-Agent':'drehorte-karte/1.0 (personal project)'}
def api(base,**p):
    p.update(format='json'); u=base+'?'+urllib.parse.urlencode(p)
    for i in range(4):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30))
        except Exception as e: print('retry',e); time.sleep(3*(i+1))
d=json.load(open('out/drehorte.json')); res={}
for o in d['orte']:
    g=api('https://commons.wikimedia.org/w/api.php',action='query',list='geosearch',gscoord=f"{o['p'][1]}|{o['p'][0]}",gsradius=150,gsnamespace=6,gslimit=25)
    res[o['id']]=[(x['title'],round(x['dist'])) for x in g['query']['geosearch']]
    print(o['id'],len(res[o['id']])); time.sleep(1)
json.dump(res,open('raw/photo_search.json','w'),ensure_ascii=False,indent=1)
