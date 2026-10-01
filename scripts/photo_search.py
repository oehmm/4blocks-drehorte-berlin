import json,urllib.request,urllib.parse,time
UA={'User-Agent':'4blocks-karte/1.0 (personal project)'}
def api(base,**p):
    p.update(format='json'); u=base+'?'+urllib.parse.urlencode(p)
    for i in range(4):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30))
        except Exception as e: print('retry',e); time.sleep(3*(i+1))
d=json.load(open('site/drehorte.json'))
WD={'highdeck':'High-Deck-Siedlung','estrel':'Estrel Berlin','jva':'Justizvollzugsanstalt Moabit','amtsgericht':'Kriminalgericht Moabit','goerli':'Görlitzer Park','hasenheide':'Volkspark Hasenheide','kotti':'Neues Kreuzberger Zentrum','rathaus':'Rathaus Neukölln','sonnenallee':'Sonnenallee','kms':'Karl-Marx-Straße (Berlin)','hermannstr':'Hermannstraße (Berlin)','daimler':'Haus Huth'}
res={}
for o in d['orte']:
    r={'p18':None,'geo':[]}
    if o['id'] in WD:
        s=api('https://www.wikidata.org/w/api.php',action='wbsearchentities',search=WD[o['id']],language='de',limit=3)
        for h in s.get('search',[]):
            e=api('https://www.wikidata.org/w/api.php',action='wbgetclaims',entity=h['id'],property='P18')
            c=e.get('claims',{}).get('P18')
            if c: r['p18']=[h['id'],h.get('description',''),c[0]['mainsnak']['datavalue']['value']]; break
            time.sleep(1)
    g=api('https://commons.wikimedia.org/w/api.php',action='query',list='geosearch',gscoord=f"{o['p'][1]}|{o['p'][0]}",gsradius=120,gsnamespace=6,gslimit=25)
    r['geo']=[(x['title'],round(x['dist'])) for x in g['query']['geosearch']]
    res[o['id']]=r; print(o['id'],r['p18'],len(r['geo'])); time.sleep(1)
json.dump(res,open('raw/photo_search.json','w'),ensure_ascii=False,indent=1)
