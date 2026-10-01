import json,urllib.request,urllib.parse,time,re,sys,os
UA={'User-Agent':'4blocks-karte/1.0 (personal project)'}
PICK={
 'highdeck':['High-Deck-Siedlung Berlin-Neukölln 01.jpg',1],
 'sonnenallee':['Sonnenallee Berlin-Neukölln 2020-06-26 01.jpg',1],
 'blackwhite':['Sonnenallee Berlin-Neukölln 2020-06-26 02.jpg',0],
 'elsalam':['Neukölln Wildenbruchstraße.JPG',0],
 'stuttgarter':['Neukölln Stuttgarter Straße.JPG',0],
 'teppich':['Berlin-Neukölln, Fuldastraße.JPG',0],
 'rathaus':['Berlin Neukoelln Rathaus asv2021-03 img1.jpg',1],
 'kms':['Karl-Marx-Straße, Berlin-Neukölln, Bild 1.jpg',1],
 'hermannstr':['Berlin Neukoelln 10Hermannstrasse.JPG',1],
 'hasenheide':['Volkspark Hasenheide.jpg',1],
 'estrel':['Berlin Estrel Neukölln asv2023-11.jpg',1],
 'private':['Britzer Damm - Wohnblock - geo.hlipp.de - 35492.jpg',0],
 'kotti':['Cafe-kotti adalbertstr-96 von der brücke aus 2023-09-03.png',1],
 'goerli':['Görlitzer Park, Berlin.jpg',1],
 'daimler':['Berlin - Weinhaus Huth.jpg',1],
 'jva':['Berlin Jail Moabit Front Dec 2004b.jpg',1],
 'amtsgericht':['Berlin-Kriminalgericht Moabit-Turmstr-Nr91-08-2023-gje.jpg',1],
}
only=sys.argv[1:]
meta=json.load(open('raw/photos.json')) if os.path.exists('raw/photos.json') else {}
def get(u):
    for i in range(6):
        try: return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60).read()
        except urllib.error.HTTPError as e:
            if e.code==429: time.sleep(int(e.headers.get('Retry-After') or 10)); continue
            raise
for k,(t,exact) in PICK.items():
    if only and k not in only: continue
    u='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode({'action':'query','titles':'File:'+t,'prop':'imageinfo','iiprop':'url|extmetadata','iiurlwidth':900,'format':'json'})
    p=next(iter(json.loads(get(u))['query']['pages'].values()))
    if 'imageinfo' not in p: print('MISSING',k,t); continue
    ii=p['imageinfo'][0]; em=ii['extmetadata']
    strip=lambda s:re.sub(r'<[^>]+>','',s or '').strip()
    time.sleep(1.5)
    open(f'raw/photos/{k}.jpg','wb').write(get(ii['thumburl']))
    meta[k]={'file':t,'page':ii['descriptionurl'],'artist':strip(em.get('Artist',{}).get('value'))[:80],'lic':em.get('LicenseShortName',{}).get('value',''),'exact':exact}
    print(k,meta[k]['artist'],meta[k]['lic']); time.sleep(1.5)
json.dump(meta,open('raw/photos.json','w'),ensure_ascii=False,indent=1)
