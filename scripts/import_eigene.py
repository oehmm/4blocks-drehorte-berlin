# Eigene Drehorte und geänderte Beschreibungen in die feste Liste übernehmen.
# Quellen: (1) Geräte-Abgleich (Cloudflare KV, alle Sync-Bereiche), (2) Artifact-Speicher, wenn als
# raw/artifact/orte/*.json und raw/artifact/texte/*.json exportiert. Szenenbilder werden NICHT übernommen
# (Urheberrecht). Ergebnis: serien/<slug>/eigene.json, das build.py einliest.
# Aufruf: SERIE=<slug> python3 scripts/import_eigene.py            -> nur anzeigen
#         SERIE=<slug> python3 scripts/import_eigene.py --uebernehmen  -> eigene.json schreiben
import json,os,sys,glob,subprocess,urllib.parse
from serie_ctx import ctx, ROOT
SLUG,DIR,SER=ctx()
WR=os.path.expanduser('~/debattier-coach-web/node_modules/.bin/wrangler')
def kv_ns():
    txt=open(os.path.join(ROOT,'sync-worker','wrangler.jsonc')).read()
    return txt.split('"id": "')[1].split('"')[0]
def wr(*a):
    cmd=([WR] if os.path.exists(WR) else ['npx','wrangler'])+list(a)
    return subprocess.run(cmd,capture_output=True,text=True,cwd=os.path.join(ROOT,'sync-worker'),check=True).stdout
orte,texte=[],{}
# (1) Geräte-Abgleich
try:
    ns=kv_ns(); keys=[k['name'] for k in json.loads(wr('kv','key','list','--namespace-id',ns,'--remote')) if k['name'].endswith(':index')]
    for k in keys:
        idx=json.loads(wr('kv','key','get',k,'--namespace-id',ns,'--remote') or '{}')
        orte+= [dict(v,id=i,_quelle='Abgleich') for i,v in (idx.get('orte') or {}).items()]
        texte.update({i:v['rolle'] for i,v in (idx.get('texte') or {}).items()})
    print(f'Abgleich: {len(keys)} Bereich(e)')
except Exception as e: print('Abgleich nicht lesbar:',e)
# (2) Artifact-Export
for f in glob.glob('raw/artifact/orte/*.json'):
    v=json.load(open(f)); v=v.get('data',v); orte.append(dict(v,id=os.path.basename(f)[:-5],_quelle='Artifact'))
for f in glob.glob('raw/artifact/texte/*.json'):
    v=json.load(open(f)); v=v.get('data',v); texte[os.path.basename(f)[:-5]]=v.get('rolle','')
fixed={o['id']:o for o in SER.ORTE}
neu=[]; seen=set()
for r in sorted(orte,key=lambda r:-(r.get('mt') or r.get('at') or 0)):
    if r['id'] in seen or r['id'] in fixed or not r.get('n') or not r.get('p'): continue
    seen.add(r['id']); url=r.get('qu') or ''
    host=urllib.parse.urlparse(url).hostname.replace('www.','') if url.startswith('http') else ''
    neu.append({'id':r['id'],'n':r['n'],'kat':r.get('kat') if r.get('kat') in SER.KAT else 'kiez','geo':f"xy:{r['p'][0]},{r['p'][1]}",
      'kiez':r.get('kiez') or '','adr':r.get('adr') or '','st':r.get('st') or '','rolle':r.get('rolle') or '','fig':[f for f in r.get('fig',[]) if f in SER.FIG],
      'staffel':r.get('staffel') or '','q':[[host or 'Quelle',url]] if url else [],'eingetragen':r['_quelle']})
txt={i:t for i,t in texte.items() if i in fixed and t.strip() and t.strip()!=fixed[i].get('rolle','').strip()}
print(f'\nNeue Drehorte: {len(neu)}'); [print(' -',o['n'],'·',o['adr'] or o['geo']) for o in neu]
print(f'Geänderte Beschreibungen: {len(txt)}'); [print(' -',fixed[i]['n']) for i in txt]
if '--uebernehmen' in sys.argv:
    old=json.load(open('eigene.json')) if os.path.exists('eigene.json') else {'orte':[],'texte':{}}
    ids={o['id'] for o in neu}; old['orte']=[o for o in old['orte'] if o['id'] not in ids]+neu; old['texte'].update(txt)
    json.dump(old,open('eigene.json','w'),ensure_ascii=False,indent=1)
    print(f"\neigene.json geschrieben ({len(old['orte'])} Orte, {len(old['texte'])} Texte). Danach: build.py, assemble.py, deploy.")
elif neu or txt: print('\nZum Übernehmen: mit --uebernehmen aufrufen.')
