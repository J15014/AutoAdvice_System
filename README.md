# AutoAdvice_System
now's study @ 2018

### 概要

このシステムは、Raspberry PiとDHT22温湿度センサーを用いて、部屋の気温と湿度から、１時間後に快適でなくなる時、自動で通知するために使うプログラムです。

構築手順
1. Raspberry Pi Model Bを用意します。
2. Raspbian OSをインストールします。
3. LAMP環境をRaspberry Pi上に構築します。
4. DHT22を配線します。
5. Adafruit_DHTのライブラリをダウンロードします。
6. WebUIのデータベース名などの設定をします。
7. Slack通知機能の設定をします。
