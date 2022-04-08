const CACHE_NAME = 'django-recipe-caches-v2';
const urlsToCache = [
  'static/images/あじ.jpg',
  'static/images/アボカド.jpg',
  'static/images/いか.jpg',
  'static/images/イワシ.jpg',
  'static/images/エビ.jpg',
  'static/images/かき.jpg',
  'static/images/かに.jpg',
  'static/images/かぼちゃ.jpg',
  'static/images/キャベツ.jpg',
  'static/images/きゅうり.jpg',
  'static/images/ごぼう.jpg',
  'static/images/サーモン・サケ.jpg',
  'static/images/さつまいも.jpg',
  'static/images/じゃがいも.jpg',
  'static/images/さんま.jpg',
  'static/images/ソーセージ・ウィンナー.jpg',
  'static/images/その他のさかな.jpg',
  'static/images/その他の魚介.jpg',
  'static/images/その他の肉.jpg',
  'static/images/たこ.jpg',
  'static/images/たら.jpg',
  'static/images/トマト.jpg',
  'static/images/なす.jpg',
  'static/images/にんじん.jpg',
  'static/images/ハム.jpg',
  'static/images/ひき肉.jpg',
  'static/images/ぶり.jpg',
  'static/images/ブロッコリー.jpg',
  'static/images/ベーコン.jpg',
  'static/images/ほうれん草.jpg',
  'static/images/マグロ.jpg',
  'static/images/貝類.jpg',
  'static/images/牛肉.jpg',
  'static/images/鶏肉.jpg',
  'static/images/小松菜.jpg',
  'static/images/鯛.jpg',
  'static/images/大根.jpg',
  'static/images/豚肉.jpg',
  'static/images/肉類全て.jpg',
  'static/images/白菜.jpg',
  'static/images/明太子・魚卵.jpg',
];
self.addEventListener('install', (event) => {
 console.log('install');
 event.waitUntil(
   caches
     .open(CACHE_NAME)
     .then((cache) => {
       return cache.addAll(urlsToCache);
     })
 );
});
self.addEventListener('fetch', (event) => {
 console.log('fetch');
 event.respondWith(
   caches
     .match(event.request)
     .then((response) => {
       return response ? response : fetch(event.request);
     })
 );
});