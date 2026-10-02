# Handy-App (PWA) einer Serie bauen: Seitenvorlage site/4blocks-karte.html + Daten aus serien/<slug>/out
# -> docs/ (Serie mit root=True) bzw. docs/<slug>/. Aufruf: SERIE=<slug> python3 scripts/assemble.py
import os,shutil,time,glob,json
from serie_ctx import ctx, ROOT
SLUG,DIR,SER=ctx(); M=SER.META; P=ROOT; SRC=os.path.join(DIR,'out')
D=P+'/docs' if M.get('root') else P+'/docs/'+SLUG
if M.get('root'):   # nur die eigenen Dateien ersetzen, Unterordner anderer Serien behalten
    os.makedirs(D,exist_ok=True)
    for f in os.listdir(D):
        q=os.path.join(D,f)
        if os.path.isdir(q) and os.path.isfile(os.path.join(P,'serien',f,'serie.py')): continue
        shutil.rmtree(q) if os.path.isdir(q) else os.remove(q)
else: shutil.rmtree(D,ignore_errors=True)
os.makedirs(D+'/fotos',exist_ok=True)
s=open(P+'/site/4blocks-karte.html').read()
s=s.replace('<title>4 Blocks Drehorte Berlin</title>','<title>'+M['title']+'</title>')
s=s.replace('<meta charset="utf-8">\n','').replace('<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n','')
head='''<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="__DESC__">
<meta name="theme-color" content="#121417">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="__SHORT__">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}</style>
'''
head=head.replace('__DESC__',M.get('description',M['title']).replace('"','&quot;')).replace('__SHORT__',M.get('short',M['title']))
reg="""<script>if('serviceWorker' in navigator&&location.protocol==='https:'){
  const had=!!navigator.serviceWorker.controller; let done=false;
  navigator.serviceWorker.addEventListener('controllerchange',()=>{ if(had&&!done){ done=true; location.reload(); } });
  addEventListener('load',()=>navigator.serviceWorker.register('sw.js').then(r=>{ r.update(); document.addEventListener('visibilitychange',()=>{ if(document.visibilityState==='visible') r.update().catch(()=>{}); }); }).catch(()=>{}));
}</script>
"""
open(D+'/index.html','w').write('<!doctype html>\n<html lang="de">\n<head>\n'+head+'</head>\n<body>\n'+s+'\n'+reg+'</body>\n</html>\n')
for f in ('basiskarte.json','drehorte.json'): shutil.copy(SRC+'/'+f,D)
fotos=sorted(os.path.basename(f) for f in glob.glob(SRC+'/fotos/*.jpg'))
for f in fotos: shutil.copy(SRC+'/fotos/'+f,D+'/fotos/')
for f in ('icon.svg','icon-192.png','icon-512.png','apple-touch-icon.png'): shutil.copy(P+'/pwa/'+f,D)
man=json.load(open(P+'/pwa/manifest.webmanifest')); man.update(name=M['title'],short_name=M.get('short',M['title']),description=M.get('description',M['title']))
json.dump(man,open(D+'/manifest.webmanifest','w'),ensure_ascii=False,indent=2)
open(D+'/sw.js','w').write(open(P+'/pwa/sw.js').read().replace('__VERSION__',time.strftime('%Y%m%d%H%M%S')).replace('__FOTOS__',','.join(json.dumps('fotos/'+f) for f in fotos)))
open(P+'/docs/.nojekyll','w').close()
print(os.path.relpath(D,P)+'/ gebaut:',len(os.listdir(D)),'Dateien,',len(fotos),'Fotos')
