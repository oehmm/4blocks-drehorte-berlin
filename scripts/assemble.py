# site/4blocks-karte.html (Artifact-Fassung) -> docs/ (GitHub Pages, Handy-App/PWA)
import os,shutil,time,glob,json
P=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D=P+'/docs'
shutil.rmtree(D,ignore_errors=True); os.makedirs(D+'/fotos')
s=open(P+'/site/4blocks-karte.html').read()
s=s.replace('<meta charset="utf-8">\n','').replace('<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n','')
head='''<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="Die Berliner Drehorte der Serie 4 Blocks auf einer Karte.">
<meta name="theme-color" content="#121417">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="4 Blocks">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}</style>
'''
reg="<script>if('serviceWorker' in navigator&&location.protocol==='https:'){addEventListener('load',()=>navigator.serviceWorker.register('sw.js').catch(()=>{}));}</script>\n"
open(D+'/index.html','w').write('<!doctype html>\n<html lang="de">\n<head>\n'+head+'</head>\n<body>\n'+s+'\n'+reg+'</body>\n</html>\n')
for f in ('basiskarte.json','drehorte.json'): shutil.copy(P+'/site/'+f,D)
fotos=sorted(os.path.basename(f) for f in glob.glob(P+'/site/fotos/*.jpg'))
for f in fotos: shutil.copy(P+'/site/fotos/'+f,D+'/fotos/')
for f in ('manifest.webmanifest','icon.svg','icon-192.png','icon-512.png','apple-touch-icon.png'): shutil.copy(P+'/pwa/'+f,D)
open(D+'/sw.js','w').write(open(P+'/pwa/sw.js').read().replace('__VERSION__',time.strftime('%Y%m%d%H%M%S')).replace('__FOTOS__',','.join(json.dumps('fotos/'+f) for f in fotos)))
open(D+'/.nojekyll','w').close()
print('docs/ gebaut:',len(os.listdir(D)),'Dateien,',len(fotos),'Fotos')
