import json,math,collections,sys
sys.path.insert(0,'scripts'); from orte import ORTE,FIG,KAT,TOUR,S
exec(open('scripts/_ref_base.py').read().split('out={}')[0].replace('48.14','52.49'))  # dp/simp/rings/polys helpers
def load(n): return json.load(open(f'osm/{n}.json'))['elements']
out={}
out['green']=polys(load('green'),4,1500)
wat=load('water')
out['water']=polys([e for e in wat if e['tags'].get('natural')=='water'],3,400)
out['rivers']=[simp(e['geometry'],3) for e in wat if e['type']=='way' and e['tags'].get('waterway') in('river','canal') and 'geometry' in e]
rl=load('rail')
out['rail']=[simp(e['geometry'],4) for e in rl if 'geometry' in e and e['tags'].get('railway') in('rail','light_rail')]
out['ubahn']=[simp(e['geometry'],4) for e in rl if 'geometry' in e and e['tags'].get('railway')=='subway']
CL={'motorway':'major','trunk':'major','primary':'major','motorway_link':'major','trunk_link':'major','primary_link':'major','secondary':'secondary','tertiary':'tertiary'}
roads=collections.defaultdict(list); labels=[]; RANK={'major':3,'secondary':2,'tertiary':2,'minor':1}; seen=set()
for e in load('roads'):
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
CLIP={'Sonnenallee':lambda lo,la:lo<13.462,'Karl-Marx-Straße':lambda lo,la:True,'Hermannstraße':lambda lo,la:True}
res=[]
for o in ORTE:
    typ,arg=o['geo'].split(':',1); r=dict(o); del r['geo']; r['q']=[S[k] for k in o['q']]
    if typ=='pt':
        la,lo,_=geo[arg]; r['p']=[round(lo,5),round(la,5)]
    elif typ=='street':
        ls=[[(p['lon'],p['lat']) for p in e['geometry'] if CLIP[arg](p['lon'],p['lat'])] for e in byname(arg,'street')]
        ls=[l for l in ls if len(l)>1]
        r['line']=[[v for x,y in l for v in (round(x,5),round(y,5))] for l in ls]; x,y=mid(ls); r['p']=[round(x,5),round(y,5)]
    elif typ=='area':
        es=byname(arg)
        if not es: print('MISSING',arg); continue
        if arg=='Michael-Bohnen-Ring':
            ls=[[(p['lon'],p['lat']) for p in e['geometry']] for e in es if 'geometry' in e]; x,y=mid(ls)
            r['p']=[round(x,5),round(y,5)]; r['radius']=180
        else:
            pp=polys([e for e in es if 'highway' not in e['tags']],2,1000); big=max(pp,key=lambda p:len(p[0]))
            r['poly']=big; xs=big[0][0::2]; ys=big[0][1::2]; r['p']=[round(sum(xs)/len(xs),5),round(sum(ys)/len(ys),5)]
    elif typ=='corner':
        a,b=arg.split('|')
        na={(p['lon'],p['lat']) for e in byname(a,'street') for p in e['geometry']}
        nb={(p['lon'],p['lat']) for e in byname(b,'street') for p in e['geometry']}
        x,y=next(iter(na&nb)); r['p']=[round(x,5),round(y,5)]
    res.append(r); print(o['id'],r['p'])
# Tour: Fußweg-Luftlinie + Distanz
def dist(a,b): return math.hypot((a[0]-b[0])*K,a[1]-b[1])*111000
by={r['id']:r for r in res}; legs=[round(dist(by[a]['p'],by[b]['p'])) for a,b in zip(TOUR,TOUR[1:])]
PH=json.load(open('raw/photos.json'))
for r in res:
    f=PH.get(r['id'])
    if f: r['foto']={'src':'fotos/'+r['id']+'.jpg','by':f['artist'] or 'unbekannt','lic':f['lic'],'page':f['page'],'exact':f['exact']}
data={'orte':res,'fig':FIG,'kat':KAT,'tour':{'ids':TOUR,'legs':legs}}
json.dump(out,open('site/basiskarte.json','w'),separators=(',',':'),ensure_ascii=False)
json.dump(data,open('site/drehorte.json','w'),separators=(',',':'),ensure_ascii=False)
for k,v in out.items(): print(k, len(v) if not isinstance(v,dict) else {a:len(b) for a,b in v.items()})
