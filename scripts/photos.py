# Fotos von Wikimedia Commons laden (Liste FOTOS in serie.py), Lizenzangaben merken
# und als 720 px breite JPEGs nach out/fotos/ schreiben (macOS: sips).
# Aufruf: SERIE=<slug> python3 scripts/photos.py [ortId ...]
import json,urllib.request,urllib.parse,time,re,sys,os,subprocess
from serie_ctx import ctx
SLUG,DIR,SER=ctx()
UA={'User-Agent':'drehorte-karte/1.0 (personal project)'}
only=sys.argv[1:]
meta=json.load(open('raw/photos.json')) if os.path.exists('raw/photos.json') else {}
def get(u):
    for i in range(6):
        try: return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60).read()
        except urllib.error.HTTPError as e:
            if e.code==429: time.sleep(int(e.headers.get('Retry-After') or 10)); continue
            raise
strip=lambda s:re.sub(r'<[^>]+>','',s or '').strip()
for k,(t,exact) in SER.FOTOS.items():
    if only and k not in only: continue
    if not only and k in meta and meta[k].get('file')==t and os.path.exists(f'out/fotos/{k}.jpg'): continue
    u='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode({'action':'query','titles':'File:'+t,'prop':'imageinfo','iiprop':'url|extmetadata','iiurlwidth':900,'format':'json'})
    p=next(iter(json.loads(get(u))['query']['pages'].values()))
    if 'imageinfo' not in p: print('FEHLT',k,t); continue
    ii=p['imageinfo'][0]; em=ii['extmetadata']; time.sleep(1.5)
    open(f'raw/photos/{k}.jpg','wb').write(get(ii['thumburl']))
    subprocess.run(['sips','-s','format','jpeg','-s','formatOptions','62','--resampleWidth','720',f'raw/photos/{k}.jpg','--out',f'out/fotos/{k}.jpg'],check=True,capture_output=True)
    meta[k]={'file':t,'page':ii['descriptionurl'],'artist':strip(em.get('Artist',{}).get('value'))[:80],'lic':em.get('LicenseShortName',{}).get('value',''),'exact':exact}
    print(k,meta[k]['artist'],meta[k]['lic']); time.sleep(1.5)
json.dump(meta,open('raw/photos.json','w'),ensure_ascii=False,indent=1)
