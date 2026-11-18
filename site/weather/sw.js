/* Sly Weather service worker: maakt de app offline bruikbaar en installeerbaar.
   De pagina zelf: meteen uit de cache (geen wachten op een trage verbinding), en op de achtergrond een nieuwe versie ophalen;
   is die anders, dan krijgt de pagina een seintje en toont een knop om te laden. Zonder cache gewoon van het netwerk.
   Weerdata (Open-Meteo, Buienradar) gaat altijd rechtstreeks naar het netwerk en wordt hier nooit opgeslagen. */
const CACHE = 'sly-weather-v2';
const SHELL = ['./', 'manifest.webmanifest', 'icon-192.png', 'icon-512.png', 'icon-maskable-512.png', 'apple-touch-icon.png'];
self.addEventListener('install', e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
const stamp = r => r && (r.headers.get('etag') || r.headers.get('last-modified') || r.headers.get('content-length'));
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (url.origin !== location.origin || e.request.method !== 'GET') return; // externe data: niet onderscheppen, niet bewaren
  if (e.request.mode === 'navigate') {
    /* Eén pagina, ook met ?tile=...: altijd onder './' bewaard */
    const net = fetch(e.request).then(async r => {
      if (r.ok) { const c = await caches.open(CACHE), old = await c.match('./'); await c.put('./', r.clone());
        if (old && stamp(old) !== stamp(r)) { const cl = await self.clients.matchAll({type: 'window'}); cl.forEach(w => w.postMessage({type: 'updated'})); } }
      return r;
    });
    e.waitUntil(net.catch(() => {}));
    e.respondWith(caches.match('./').then(hit => hit || net).catch(() => net));
    return;
  }
  e.respondWith(fetch(e.request).then(r => { if (r.ok) { const copy = r.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); } return r; })
    .catch(() => caches.match(e.request)));
});
