## 環境構築

1. `docker build -t <任意のタグ名> .`でイメージをビルドする(ex. `docker build -t image-scraping .`)

## 実行方法

1. `docker run -v <本ディレクトリへのパス>:/work -it --rm <任意のタグ名> python main.py`を実行する。

2. `./images`配下に`dog`, `cat`, `rabbit`ディレクトリが順次作成され、内部に画像が格納されていくので終了まで待つ。

## 画像取得元

`https://images.search.yahoo.com/` にて検索した結果から画像 url をスクレイピングで取得している。

## トラブルシューティング

- 検索結果を変えたい => setting.json の urls を変更する。

- 保存先を変えたい => setting.json の dst を変更する

- 画像の接頭辞を変えたい => setting.json の prefix を変更する。

## 制限

`https://images.search.yahoo.com/` 以外での検索結果には対応していない(ex. Google 検索などは対象外)。
