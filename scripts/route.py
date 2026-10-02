# Fußwege zwischen Rundgang-Stationen: Dijkstra auf dem OSM-Wegenetz (osm/walk.json)
import json,math,heapq
K=math.cos(math.radians(52.48))
def set_lat(lat):
    global K; K=math.cos(math.radians(lat))
def dist(a,b): return math.hypot((a[0]-b[0])*K,a[1]-b[1])*111320
W={'footway':.92,'pedestrian':.9,'path':.95,'living_street':.95,'residential':1,'service':1.05,'steps':1.4,'cycleway':1.1,
   'primary':1.12,'secondary':1.08,'tertiary':1.03,'unclassified':1,'track':1.05,'trunk':1.3,'primary_link':1.15,'secondary_link':1.1,'tertiary_link':1.05,'corridor':1}
def graph():
    pos={}; adj={}; snap=set()
    for e in json.load(open('osm/walk.json'))['elements']:
        if e['type']!='way' or 'geometry' not in e: continue
        f=W.get(e['tags'].get('highway'),1.1)
        ids=e['nodes']; g=e['geometry']
        if e['tags'].get('name') and e['tags'].get('highway') not in ('service','steps','corridor'): snap.update(ids)
        for i,(n,p) in enumerate(zip(ids,g)):
            pos[n]=(p['lon'],p['lat'])
            if i:
                m=ids[i-1]; d=dist(pos[m],pos[n])
                adj.setdefault(m,[]).append((n,d,d*f)); adj.setdefault(n,[]).append((m,d,d*f))
    return pos,adj,snap
def nearest(pos,p,snap): return min(snap,key=lambda n:(pos[n][0]-p[0])**2*K*K+(pos[n][1]-p[1])**2)
def path(pos,adj,a,b):
    best={a:0}; prev={}; h=[(0,a)]
    while h:
        c,n=heapq.heappop(h)
        if n==b: break
        if c>best[n]: continue
        for m,d,w in adj.get(n,()):
            nc=c+w
            if nc<best.get(m,1e18): best[m]=nc; prev[m]=n; heapq.heappush(h,(nc,m))
    seq=[b]
    while seq[-1]!=a: seq.append(prev[seq[-1]])
    seq.reverse(); pts=[pos[n] for n in seq]
    return pts,sum(dist(pts[i],pts[i+1]) for i in range(len(pts)-1))
def route(stops):
    pos,adj,snap=graph(); legs=[]
    for a,b in zip(stops,stops[1:]):
        na,nb=nearest(pos,a,snap),nearest(pos,b,snap)
        pts,m=path(pos,adj,na,nb)
        pts=[a]+pts+[b]; m+=dist(a,pos[na])+dist(pos[nb],b)
        legs.append({'m':round(m),'line':[v for x,y in pts for v in (round(x,5),round(y,5))]})
    return legs
