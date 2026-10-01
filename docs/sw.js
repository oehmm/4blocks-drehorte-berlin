// Offline-Speicher: Seite aus dem Netz (Fallback Cache), Daten und Fotos aus dem Cache.
const VERSION = '20261001100641';
const CORE = ['./', 'index.html', 'basiskarte.json', 'drehorte.json', 'manifest.webmanifest', 'icon-192.png', "fotos/amtsgericht.jpg","fotos/blackwhite.jpg","fotos/daimler.jpg","fotos/elsalam.jpg","fotos/estrel.jpg","fotos/goerli.jpg","fotos/hasenheide.jpg","fotos/hermannstr.jpg","fotos/highdeck.jpg","fotos/jva.jpg","fotos/kms.jpg","fotos/kotti.jpg","fotos/private.jpg","fotos/rathaus.jpg","fotos/sonnenallee.jpg","fotos/stuttgarter.jpg","fotos/teppich.jpg"];
self.addEventListener('install', e => {
  e.waitUntil(caches.open('core-' + VERSION).then(c => Promise.all(CORE.map(u => c.add(u).catch(() => null)))).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== 'core-' + VERSION && k !== 'ext').map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  const url = new URL(e.request.url);
  if (url.origin !== location.origin) {             // Leaflet & Schriften: Cache zuerst
    if (/cdnjs\.cloudflare\.com|fonts\.(googleapis|gstatic)\.com/.test(url.hostname))
      e.respondWith(caches.open('ext').then(async c => (await c.match(e.request)) ||
        fetch(e.request).then(r => { if (r.ok || r.type === 'opaque') c.put(e.request, r.clone()); return r; })));
    return;
  }
  if (e.request.mode === 'navigate') {
    e.respondWith(fetch(e.request).then(r => { caches.open('core-' + VERSION).then(c => c.put('index.html', r.clone())); return r; })
      .catch(() => caches.match('index.html')));
    return;
  }
  e.respondWith(caches.match(e.request).then(m => m || fetch(e.request)));
});
