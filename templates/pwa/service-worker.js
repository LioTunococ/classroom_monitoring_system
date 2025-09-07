// Basic service worker for CMS
const CACHE_NAME = 'cms-cache-v3';
const OFFLINE_URL = '/offline/';

// Cache core assets (app shell)
const CORE_ASSETS = [
  '/',
  OFFLINE_URL,
  '/pwa/icons/icon-192.png',
  '/pwa/icons/icon-192-maskable.png',
  '/pwa/icons/icon-512.png',
  '/pwa/icons/icon-512-maskable.png',
  '/static/pwa/manifest.webmanifest',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(CORE_ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))))
  );
  self.clients.claim();
});

// Strategy: network-first for same-origin HTML, cache-first for static assets
self.addEventListener('fetch', (event) => {
  const req = event.request;
  const url = new URL(req.url);
  if (req.method !== 'GET') return; // only GET

  // Static files: cache-first
  if (url.origin === location.origin && url.pathname.startsWith('/static/')) {
    event.respondWith(
      caches.match(req).then(cached => cached || fetch(req).then(resp => {
        const clone = resp.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(req, clone));
        return resp;
      }))
    );
    return;
  }

  // HTML navigation: network-first with offline fallback
  if (req.mode === 'navigate' || (req.headers.get('accept') || '').includes('text/html')) {
    event.respondWith(
      fetch(req).catch(() => caches.match(OFFLINE_URL))
    );
    return;
  }

  // Default: try cache, then network
  event.respondWith(
    caches.match(req).then(cached => cached || fetch(req))
  );
});

// Allow page to trigger skipWaiting via message
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
