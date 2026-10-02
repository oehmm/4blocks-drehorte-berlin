# Basiskarte (out/basiskarte.json) und Drehort-Daten (out/drehorte.json) einer Serie bauen.
# Aufruf: SERIE=<slug> python3 scripts/build.py
import json,math,collections,sys,os,glob
from serie_ctx import ctx
SLUG,DIR,SER=ctx(); M=SER.META
ORTE,FIG,KAT,TOUR,S=SER.ORTE,SER.FIG,SER.KAT,getattr(SER,'TOUR',[]),SER.S
import geo; geo.set_lat(M.get('lat',52.5)); from geo import *
import route; route.set_lat(M.get('lat',52.5))
def load(n): return json.load(open(f'osm/{n}.json'))['elements'] if os.path.exists(f'osm/{n}.json') else []
def extras(kind): return [e for f in sorted(glob.glob(f'osm/x*_{kind}.json')) for e in json.load(open(f))['elements']]
# eigene Einträge, die übernommen wurden (scripts/import_eigene.py)
EIG=json.load(open('eigene.json')) if os.path.exists('eigene.json') else {'orte':[],'texte':{}}
out={}
blm=extras('misc')
out['green']=polys(load('green')+[e for e in blm if 'railway' not in e['tags'] and e['tags'].get('natural')!='water'],4,1500)
wat=load('water')
out['water']=polys([e for e in wat+blm if e['tags'].get('natural')=='water'],3,400)
out['rivers']=[simp(e['geometry'],3) for e in wat if e['type']=='way' and e['tags'].get('waterway') in('river','canal') and 'geometry' in e]
rl=load('rail')
out['rail']=[simp(e['geometry'],4) for e in rl+blm if 'geometry' in e and e['tags'].get('railway') in('rail','light_rail')]
out['ubahn']=[simp(e['geometry'],4) for e in rl if 'geometry' in e and e['tags'].get('railway')=='subway']
CL={'motorway':'major','trunk':'major','primary':'major','motorway_link':'major','trunk_link':'major','primary_link':'major','secondary':'secondary','tertiary':'tertiary'}
roads=collections.defaultdict(list); labels=[]; RANK={'major':3,'secondary':2,'tertiary':2,'minor':1}; seen=set()
for e in load('roads')+extras('roads'):
    g=e.get('geometry')
    if not g: continue
    c=CL.get(e['tags']['highway'],'minor')
    roads[c].append(simp(g,2.5 if c=='minor' else 3))
    n=e['tags'].get('name')
    if n and e['tags']['highway'] not in('motorway','motorway_link','trunk_link','primary_link'):
        p=proj(g); seg=[math.dist(p[i],p[i+1])*111000 for i in range(len(p)-1)]; Lt=sum(seg)
        if Lt<90: continue
        acc=0
        for i,s in enumerate(seg):
            if acc+s>=Lt/2: break
            acc+=s
        t=(Lt/2-acc)/s if s else 0
        x=p[i][0]+(p[i+1][0]-p[i][0])*t; y=p[i][1]+(p[i+1][1]-p[i][1])*t
        ang=-math.degrees(math.atan2(p[i+1][1]-p[i][1],p[i+1][0]-p[i][0]))
        if ang>90: ang-=180
        if ang<-90: ang+=180
        key=(n,round(x/K/0.004),round(y/0.003))
        if key in seen: continue
        seen.add(key); labels.append([round(x/K,5),round(y,5),round(ang),n,RANK[c]-1 if Lt>150 else 0])
labels.sort(key=lambda l:-l[4]); out['roads']=roads; out['labels']=labels
adm=load('admin'); bez=[]; ot=[]
def centroid(r):
    P=[(p['lon'],p['lat']) for p in r]; A=cx=cy=0
    for i in range(len(P)):
        x0,y0=P[i-1];x1,y1=P[i];c=x0*y1-x1*y0;A+=c;cx+=(x0+x1)*c;cy+=(y0+y1)*c
    return [round(cx/(3*A),5),round(cy/(3*A),5)]
for e in adm:
    lv=e['tags'].get('admin_level'); rs=[r for r in rings(e['members'],'outer') if len(r)>3]
    if not rs: continue
    d={'n':e['tags']['name'],'c':centroid(max(rs,key=len)),'r':[simp(r,6) for r in rs]}
    (bez if lv=='9' else ot).append(d)
out['bezirke']=bez; out['ortsteile']=ot
def stype(t):
    if t.get('station')=='subway' or t.get('subway')=='yes': return 'U'
    if t.get('station')=='light_rail' or t.get('light_rail')=='yes' or 'S-Bahn' in t.get('network','')+t.get('operator',''): return 'S'
    return None
ss={}
for e in load('stations'):
    t=e.get('tags',{}); n=t.get('name'); ty=stype(t)
    if not n or not ty: continue
    n=n.replace('S+U ','').replace('U ','').replace('S ','').replace('Berlin-','')
    k=(n,ty)
    if k not in ss: ss[k]=[round(e['lon'],5),round(e['lat'],5),n,ty]
out['stations']=list(ss.values())
# --- Drehorte ---
geo=json.load(open('osm/geocode.json')); poi=load('poi')+load('green')
def byname(n,typ=None):
    return [e for e in poi if e.get('tags',{}).get('name')==n and (typ is None or ('highway' in e['tags'])==(typ=='street'))]
def mid(lines):
    pts=[p for l in lines for p in l]; xs=sorted(p[0] for p in pts); ys=sorted(p[1] for p in pts)
    c=(xs[len(xs)//2],ys[len(ys)//2]); return min(pts,key=lambda p:(p[0]-c[0])**2+(p[1]-c[1])**2)
res=[]
for o in ORTE+EIG['orte']:
    typ,arg=o['geo'].split(':',1); r=dict(o); del r['geo']; r.pop('clip',None); r.pop('geocode',None)
    r['q']=[S[k] if isinstance(k,str) else k for k in o.get('q',[])]
    if o['id'] in EIG['texte']: r['rolle']=EIG['texte'][o['id']]
    if typ=='pt':
        la,lo,_=geo[arg]; r['p']=[round(lo,5),round(la,5)]
    elif typ=='street':
        lo0,lo1=(o.get('clip') or [None,None]); inside=lambda lo:(lo0 is None or lo>=lo0) and (lo1 is None or lo<=lo1)
        ls=[[(p['lon'],p['lat']) for p in e['geometry'] if inside(p['lon'])] for e in byname(arg,'street')]
        ls=[l for l in ls if len(l)>1]
        r['line']=[[v for x,y in l for v in (round(x,5),round(y,5))] for l in ls]; x,y=mid(ls); r['p']=[round(x,5),round(y,5)]
    elif typ=='area':
        es=byname(arg)
        if not es: print('MISSING',arg); continue
        pp=polys([e for e in es if 'highway' not in e['tags']],2,1000); big=max(pp,key=lambda p:len(p[0]))
        r['poly']=big; xs=big[0][0::2]; ys=big[0][1::2]; r['p']=[round(sum(xs)/len(xs),5),round(sum(ys)/len(ys),5)]
    elif typ=='corner':
        a,b=arg.split('|')
        na={(p['lon'],p['lat']) for e in byname(a,'street') for p in e['geometry']}
        nb={(p['lon'],p['lat']) for e in byname(b,'street') for p in e['geometry']}
        x,y=next(iter(na&nb)); r['p']=[round(x,5),round(y,5)]
    elif typ=='xy':
        lo,la=map(float,arg.split(',')); r['p']=[round(lo,6),round(la,6)]
    res.append(r); print(o['id'],r['p'])
# Rundgang: echte Fußwege (osm/walk.json), sonst Luftlinie
def dist(a,b): return math.hypot((a[0]-b[0])*geo.K,a[1]-b[1])*111320
by={r['id']:r for r in res}
if TOUR and os.path.exists('osm/walk.json'): rl_=route.route([by[i]['p'] for i in TOUR]); real=True
else: rl_=[{'m':round(dist(by[a]['p'],by[b]['p'])),'line':by[a]['p']+by[b]['p']} for a,b in zip(TOUR,TOUR[1:])]; real=False
def simpline(a):
    g=[{'lon':a[i],'lat':a[i+1]} for i in range(0,len(a),2)]; return simp(g,1.5)
PH=json.load(open('raw/photos.json')) if os.path.exists('raw/photos.json') else {}
for r in res:
    f=PH.get(r['id'])
    if f: r['foto']={'src':'fotos/'+r['id']+'.jpg','by':f['artist'] or 'unbekannt','lic':f['lic'],'page':f['page'],'exact':f['exact']}
meta={k:v for k,v in M.items() if k not in('bbox','extra_bboxes','walk_bbox','root')}
data={'serie':meta,'orte':res,'fig':FIG,'kat':KAT,'tour':{'ids':TOUR,'legs':[l['m'] for l in rl_],'lines':[simpline(l['line']) for l in rl_] if real else None,'real':real}}
json.dump(out,open('out/basiskarte.json','w'),separators=(',',':'),ensure_ascii=False)
json.dump(data,open('out/drehorte.json','w'),separators=(',',':'),ensure_ascii=False)
for k,v in out.items(): print(k, len(v) if not isinstance(v,dict) else {a:len(b) for a,b in v.items()})
