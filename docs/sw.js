/**
 * SERVICE WORKER FOR DAILY NEWS DIGEST
 * Provides offline functionality and caching for accessibility
 */

const CACHE_NAME = 'news-digest-v1';
const STATIC_CACHE = 'news-digest-static-v1';

// Files to cache for offline use
const STATIC_FILES = [
    '/',
    '/index.html',
    '/css/newspaper.css',
    '/js/accessibility.js',
    '/manifest.json'
];

// Install event - cache static files
self.addEventListener('install', function(event) {
    console.log('📦 Service Worker: Installing...');
    
    event.waitUntil(
        caches.open(STATIC_CACHE)
            .then(function(cache) {
                console.log('📦 Service Worker: Caching static files');
                return cache.addAll(STATIC_FILES);
            })
            .then(function() {
                console.log('✅ Service Worker: Static files cached');
                return self.skipWaiting();
            })
    );
});

// Activate event - clean up old caches
self.addEventListener('activate', function(event) {
    console.log('🚀 Service Worker: Activating...');
    
    event.waitUntil(
        caches.keys()
            .then(function(cacheNames) {
                return Promise.all(
                    cacheNames.map(function(cacheName) {
                        if (cacheName !== CACHE_NAME && cacheName !== STATIC_CACHE) {
                            console.log('🗑️ Service Worker: Deleting old cache', cacheName);
                            return caches.delete(cacheName);
                        }
                    })
                );
            })
            .then(function() {
                console.log('✅ Service Worker: Activated');
                return self.clients.claim();
            })
    );
});

// Fetch event - serve from cache with network fallback
self.addEventListener('fetch', function(event) {
    const request = event.request;
    const url = new URL(request.url);
    
    // Handle different types of requests
    if (request.method !== 'GET') {
        return;
    }
    
    // Cache strategy based on file type
    if (isStaticFile(url.pathname)) {
        // Static files: Cache first, network fallback
        event.respondWith(cacheFirst(request));
    } else if (isAudioFile(url.pathname)) {
        // Audio files: Network first, cache fallback
        event.respondWith(networkFirstWithCache(request));
    } else if (isHTMLFile(url.pathname)) {
        // HTML files: Network first, cache fallback
        event.respondWith(networkFirstWithCache(request));
    } else {
        // Everything else: Network only
        event.respondWith(fetch(request));
    }
});

// Cache first strategy for static files
function cacheFirst(request) {
    return caches.match(request)
        .then(function(cachedResponse) {
            if (cachedResponse) {
                return cachedResponse;
            }
            
            return fetch(request)
                .then(function(networkResponse) {
                    // Cache successful responses
                    if (networkResponse.status === 200) {
                        const responseClone = networkResponse.clone();
                        caches.open(STATIC_CACHE)
                            .then(function(cache) {
                                cache.put(request, responseClone);
                            });
                    }
                    return networkResponse;
                })
                .catch(function() {
                    // Return offline page if available
                    if (request.destination === 'document') {
                        return caches.match('/offline.html');
                    }
                });
        });
}

// Network first with cache fallback
function networkFirstWithCache(request) {
    return fetch(request)
        .then(function(networkResponse) {
            // Cache successful responses
            if (networkResponse.status === 200) {
                const responseClone = networkResponse.clone();
                caches.open(CACHE_NAME)
                    .then(function(cache) {
                        cache.put(request, responseClone);
                    });
            }
            return networkResponse;
        })
        .catch(function() {
            // Fallback to cache
            return caches.match(request)
                .then(function(cachedResponse) {
                    if (cachedResponse) {
                        return cachedResponse;
                    }
                    
                    // Return offline page for HTML requests
                    if (request.destination === 'document') {
                        return caches.match('/offline.html');
                    }
                    
                    // Return offline audio message for audio requests
                    if (isAudioFile(request.url)) {
                        return new Response('Audio not available offline', {
                            status: 503,
                            statusText: 'Service Unavailable'
                        });
                    }
                });
        });
}

// Helper functions
function isStaticFile(pathname) {
    return pathname.includes('/css/') || 
           pathname.includes('/js/') || 
           pathname.includes('/images/') ||
           pathname.endsWith('.css') ||
           pathname.endsWith('.js') ||
           pathname.endsWith('.png') ||
           pathname.endsWith('.jpg') ||
           pathname.endsWith('.svg') ||
           pathname.endsWith('.ico');
}

function isAudioFile(pathname) {
    return pathname.endsWith('.mp3') || 
           pathname.endsWith('.wav') || 
           pathname.endsWith('.ogg') ||
           pathname.includes('/audio/');
}

function isHTMLFile(pathname) {
    return pathname.endsWith('.html') || 
           pathname === '/' ||
           !pathname.includes('.');
}

// Background sync for analytics (if needed)
self.addEventListener('sync', function(event) {
    if (event.tag === 'background-sync') {
        event.waitUntil(doBackgroundSync());
    }
});

function doBackgroundSync() {
    // Could be used for analytics or usage tracking
    console.log('📊 Service Worker: Background sync triggered');
    return Promise.resolve();
}

// Push notifications (for future use)
self.addEventListener('push', function(event) {
    if (event.data) {
        const data = event.data.json();
        const options = {
            body: data.body || 'New daily news digest available',
            icon: '/images/icon-192.png',
            badge: '/images/badge-72.png',
            tag: 'news-digest',
            requireInteraction: false,
            actions: [
                {
                    action: 'listen',
                    title: '🎧 Listen Now',
                    icon: '/images/play-icon.png'
                },
                {
                    action: 'download',
                    title: '⬇️ Download',
                    icon: '/images/download-icon.png'
                }
            ]
        };
        
        event.waitUntil(
            self.registration.showNotification(data.title || 'Daily News Digest', options)
        );
    }
});

// Notification click handling
self.addEventListener('notificationclick', function(event) {
    event.notification.close();
    
    if (event.action === 'listen') {
        event.waitUntil(
            clients.openWindow('/?action=play')
        );
    } else if (event.action === 'download') {
        event.waitUntil(
            clients.openWindow('/?action=download')
        );
    } else {
        event.waitUntil(
            clients.openWindow('/')
        );
    }
});

console.log('🔧 Service Worker: Loaded and ready');
