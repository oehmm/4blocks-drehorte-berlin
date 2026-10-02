# Geometrie-Helfer: Douglas-Peucker, Ringe aus OSM-Relationen, Polygone
import json,math,collections
def dp(pts,eps):
    if len(pts)<3: return pts
    keep=[False]*len(pts); keep[0]=keep[-1]=True; st=[(0,len(pts)-1)]
    while st:
        a,b=st.pop(); ax,ay=pts[a]; bx,by=pts[b]; dx,dy=bx-ax,by-ay; L=dx*dx+dy*dy; mi=-1; md=eps*eps
        for i in range(a+1,b):
            px,py=pts[i]
            if L==0: d=(px-ax)**2+(py-ay)**2
            else:
                t=max(0,min(1,((px-ax)*dx+(py-ay)*dy)/L)); d=(px-ax-t*dx)**2+(py-ay-t*dy)**2
            if d>md: md=d; mi=i
        if mi>=0: keep[mi]=True; st+=[(a,mi),(mi,b)]
    return [p for p,k in zip(pts,keep) if k]
K=math.cos(math.radians(52.49))  # wird von set_lat() angepasst
def set_lat(lat):
    global K; K=math.cos(math.radians(lat))
def proj(g): return [(p['lon']*K,p['lat']) for p in g]   # scaled so eps is isotropic
def unproj(pts): return [v for x,y in pts for v in (round(x/K,5),round(y,5))]
def simp(g,eps_m): return unproj(dp(proj(g),eps_m/111000))
def area(g):
    p=proj(g); return abs(sum(p[i][0]*p[i-1][1]-p[i-1][0]*p[i][1] for i in range(len(p))))/2*111000**2
def rings(members,role='outer'):
    segs=[m['geometry'] for m in members if m.get('type')=='way' and m.get('role',role) in (role,'') and 'geometry' in m]
    segs=[[(p['lon'],p['lat']) for p in s] for s in segs]; out=[]
    while segs:
        r=segs.pop()
        while r[0]!=r[-1]:
            for i,s in enumerate(segs):
                if s[0]==r[-1]: r+=s[1:]; break
                if s[-1]==r[-1]: r+=s[::-1][1:]; break
                if s[-1]==r[0]: r=s+r[1:]; break
                if s[0]==r[0]: r=s[::-1]+r[1:]; break
            else: break
            segs.pop(i)
        out.append([{'lon':x,'lat':y} for x,y in r])
    return out
def polys(elems,eps,minA):
    P=[]
    for e in elems:
        if e['type']=='way' and 'geometry' in e and e['geometry'][0]==e['geometry'][-1]: rs=[e['geometry']]; holes=[]
        elif e['type']=='relation': rs=rings(e['members'],'outer'); holes=rings(e['members'],'inner')
        else: continue
        for r in rs:
            if len(r)<4 or area(r)<minA: continue
            poly=[simp(r,eps)]
            for h in holes:
                if len(h)>3 and area(h)>minA and h[0]['lon']>=min(p['lon'] for p in r) and h[0]['lon']<=max(p['lon'] for p in r) and h[0]['lat']>=min(p['lat'] for p in r) and h[0]['lat']<=max(p['lat'] for p in r):
                    poly.append(simp(h,eps))
            if len(poly[0])>=6: P.append(poly)
    return P
