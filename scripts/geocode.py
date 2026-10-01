import json,time,urllib.request,urllib.parse
Q={
 'elsalam':'Wildenbruchstraße 68, 12045 Berlin',
 'estrel':'Sonnenallee 225, 12057 Berlin',
 'stuttgarter':'Stuttgarter Straße 47, 12059 Berlin',
 'kotti':'Adalbertstraße 96, 10999 Berlin',
 'jva':'Alt-Moabit 12a, 10559 Berlin',
 'amtsgericht':'Turmstraße 91, 10559 Berlin',
 'daimler':'Alte Potsdamer Straße 5, 10785 Berlin',
 'private':'Britzer Damm 115, 12347 Berlin',
 'blackwhite':'Sonnenallee 72, 12045 Berlin',
 'rathaus':'Karl-Marx-Straße 83, 12043 Berlin',
}
out={}
for k,q in Q.items():
    u='https://nominatim.openstreetmap.org/search?'+urllib.parse.urlencode({'q':q,'format':'json','limit':1})
    r=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'4blocks-karte/1.0 (personal project)'})))
    out[k]=[float(r[0]['lat']),float(r[0]['lon']),r[0]['display_name']] if r else None
    print(k,out[k]); time.sleep(1.1)
json.dump(out,open('osm/geocode.json','w'),ensure_ascii=False,indent=1)
