# 名前
Django Recipe
 
「今ある食材から簡単にレシピを検索できる」アプリを目指しています．

# 開発理由

「ご飯のメニューを決めるのが億劫」という課題を解決するために作っています．

# 開発期間

2021/8 〜 2022/3 (その後も修正中)

# 使用技術

Python, Django, 楽天レシピカテゴリ一覧 API（レシピ検索に利用）, Cloud Vision API（食材検出に利用）, ひらがな化 API （写真から食材検出の過程で，ひらがな表示に統一するために利用），PWA（スマホのホーム画面から，スマホアプリのように利用するために使用），heroku （デプロイ），Intersection Observer API （遅延読み込みで利用），

# 主要機能

- 食材名を複数選択し，その食材から作れるレシピを検索
- 食材の写真からレシピ検索
- レシピのお気に入り登録


# デモ

- 食材名を選択してレシピ検索
https://user-images.githubusercontent.com/63027348/160527704-e516f306-dd9e-4b27-8697-09ee3e3ff097.mp4

- 食材の写真からレシピ検索
https://user-images.githubusercontent.com/63027348/167299408-1c682320-e39d-4c4b-a363-0ec9a21e15bd.mp4

- お気に入りレシピ登録
https://user-images.githubusercontent.com/63027348/160526149-c16875f8-8e4a-4be5-bcc2-fd381e9b50fb.MP4

# URL

https://recipe-simple-search-app.herokuapp.com/recipe/random

# スライド
https://drive.google.com/file/d/1Rfmk2If3ajzMuS2OKbROUvW0REj89DLh/view?usp=sharing

<!--
# 名前
レシピ検索アプリ
 
手元にある食材から作れるレシピを簡単に知ることができます．
 
 
# 特徴
 
- スマホのホーム画面から，スマホアプリのように利用することができます．
- 食材の写真からレシピを検索できるようにしました．
- お気に入りのレシピを登録することもできます．

# 工夫した点

- ServiceWorker でのキャッシュ処理 と Intersection Observer API を使って，「食材名でレシピ検索」画面の食材写真の表示速度を改善した点．
__ここまでの軌跡をスライドにまとめたので，ぜひ見ていただきたいです．__

https://docs.google.com/presentation/d/1pirfZRT6MMmgtlwyGqs_thMviXgPgsMk_KKACBoaRXY/edit?usp=sharing

ServiceWorker・Intersection Observer API をそれぞれ適用した場合・そうでない場合の Lighthouse の計測結果を以下に示します．
ServiceWorker・Intersection Observer API をどちらも適用した場合に，First Contentful Paint や，Time to Interactive, Speed Index, Largest Contentful Paint が最小となることが分かります．

- ServiceWorker・Intersection Observer API をどちらも適用
![cache-lazy](https://user-images.githubusercontent.com/63027348/163294687-327e18a9-ef0f-4787-b184-249d1687df7a.png)

- ServiceWorker のみ適用
![cache-not-lazy](https://user-images.githubusercontent.com/63027348/163294772-7bfdf01f-df5f-4b2d-96c3-6c7fc5b1643e.png)

- Intersection Observer API のみ適用
![not-cache-lazy](https://user-images.githubusercontent.com/63027348/163294845-15a52266-ab5f-437a-afd3-d50ef0fb2770.png)

- どちらも適用しない
![not-cache-not-lazy](https://user-images.githubusercontent.com/63027348/163294896-9c0176b6-b4cc-431c-9d40-2503cefebe51.png)

# 開発理由

今ある食材から多くのレシピを作れるようになれば良いなと思い，作りました．

# 開発期間

2021/8 〜 2022/3 (その後も修正中)


# デモ
 
- 食材名からレシピ検索
https://user-images.githubusercontent.com/63027348/160527704-e516f306-dd9e-4b27-8697-09ee3e3ff097.mp4

- 食材の写真からレシピ検索
https://user-images.githubusercontent.com/63027348/160526750-46a37c12-9a51-41f6-8b03-dfe90adde005.mp4

- お気に入りのレシピ登録
https://user-images.githubusercontent.com/63027348/160526149-c16875f8-8e4a-4be5-bcc2-fd381e9b50fb.MP4

# URL

https://recipe-simple-search-app.herokuapp.com/recipe/random

# 使用技術

Python, Django, 楽天レシピカテゴリ一覧 API（レシピ検索に利用）, Cloud Vision API（食材検出に利用）, PWA（スマホのホーム画面から，スマホアプリのように利用するために使用），heroku （デプロイ）


 

# Requirement
 
"hoge"を動かすのに必要なライブラリなどを列挙する
 
* huga 3.5.2
* hogehuga 1.0.2
 
# Installation
 
Requirementで列挙したライブラリなどのインストール方法を説明する
 
```bash
pip install huga_package
```
 
# Usage
 
DEMOの実行方法など、"hoge"の基本的な使い方を説明する
 
```bash
git clone https://github.com/hoge/~
cd examples
python demo.py
```
 
# Note
 
注意点などがあれば書く
 
# Author
 
作成情報を列挙する
-->