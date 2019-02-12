# AutoAdvice_System
now's study @ 2018

### 概要

このシステムは、Raspberry PiとDHT22温湿度センサーを用いて、部屋の気温と湿度から、１時間後に快適でなくなる時、自動で通知するために使うプログラムです。

##### 構築手順
1. Raspberry Pi Model Bを用意します。
2. Raspbian OSをインストールします。
3. LAMP環境をRaspberry Pi上に構築します。
4. DHT22を配線します。
5. Adafruit_DHTのライブラリをダウンロードします。
6. WebUIのデータベース名などの設定をします。
7. Slack通知機能の設定をします。

##### Raspberry Pi上のサーバファイル
1. cake.zipはCakePHPを利用したグラフ表示のためのファイルが詰まっている
2. enquete.zipはアンケートページのためのファイルが詰まっている。

##### Raspberry Pi OSのインストール手順
microSDをフォーマット → OSインストール用ソフトの書き込み →Raspberry PiにmicroSDをセットインストール
①SDカードをフォーマット
「macの場合」
ディスクユーティリティで初期化

図4-1.　ディスクユーティリティ画像
exFATで初期化
