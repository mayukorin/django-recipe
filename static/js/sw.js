const CACHE_NAME = 'django-recipe-cache-v1';

const urlsToCache = [
    '../images/あじ.jpg',
    '../images/アボカド.jpg',
    '../images/いか.jpg',
    '../images/イワシ.jpg',
    '../images/エビ.jpg',
    '../images/かき.jpg',
    '../images/かに.jpg',
    '../images/かぼちゃ.jpg',
    '../images/キャベツ.jpg',
    '../images/きゅうり.jpg',
    '../images/ごぼう.jpg',
    '../images/サーモン・サケ.jpg',
    '../images/さつまいも.jpg',
    '../images/じゃがいも.jpg',
    '../images/さんま.jpg',
    '../images/ソーセージ・ウィンナー.jpg',
    '../images/その他のさかな.jpg',
    '../images/その他の魚介.jpg',
    '../images/その他の肉.jpg',
    '../images/たこ.jpg',
    '../images/たら.jpg',
    '../images/トマト.jpg',
    '../images/なす.jpg',
    '../images/にんじん.jpg',
    '../images/ハム.jpg',
    '../images/ひき肉.jpg',
    '../images/ぶり.jpg',
    '../images/ブロッコリー.jpg',
    '../images/ベーコン.jpg',
    '../images/ほうれん草.jpg',
    '../images/マグロ.jpg',
    '../images/貝類.jpg',
    '../images/牛肉.jpg',
    '../images/鶏肉.jpg',
    '../images/小松菜.jpg',
    '../images/鯛.jpg',
    '../images/大根.jpg',
    '../images/豚肉.jpg',
    '../images/肉類全て.jpg',
    '../images/白菜.jpg',
    '../images/明太子・魚卵.jpg',
];

self.addEventListener('install', (event) => {
  console.log("okay");
    event.waitUntil(
      caches
        .open(CACHE_NAME)
        .then((cache) => {
          return cache.addAll(urlsToCache);
        })
    );
});

self.addEventListener('fetch', (event) => {
});