# AutoAdvice_System
now's study @ 2018

### 概要

このシステムは、Raspberry Pi3 Model BとDHT22温湿度センサーを用いて、部屋の気温と湿度から、１時間後に快適でなくなる時、自動で通知するために使うプログラムです。

##### 構築手順
1. Raspberry Pi3 Model Bを用意します。
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
<img src='https://github.com/J15014/Images/blob/master/%E3%83%86%E3%82%99%E3%82%A3%E3%82%B9%E3%82%AF%E3%83%A6%E3%83%BC%E3%83%86%E3%82%A3%E3%83%AA%E3%83%86%E3%82%A32019-01-15%2012.07.11.png'>  
図1.　ディスクユーティリティ画像
  
exFATで初期化
<img src='https://github.com/J15014/Images/blob/master/%E3%83%86%E3%82%99%E3%82%A3%E3%82%B9%E3%82%AF%E3%83%A6%E3%83%BC%E3%83%86%E3%83%AA%E3%83%86%E3%82%A3%E8%A8%AD%E5%AE%9A%E7%94%BB%E9%9D%A2.png'>  
図2.　ディスクユーティリティ設定画面
  
ddコマンドを利用してimgファイルを書き込む。
```
~$ sudo dd bs=1m if=2018-06-27-raspbian-stretch.img of=/dev/disk2
```
  
②sshの有効化  
書き込んだSDカードをMacに接続し、ターミナルからコマンドを打つ
```
~$ touch /Volumes/boot/ssh
```
  
③Raspberry Piの起動  
Raspberry PiにOSインストール済みのmicroSDを挿す。  
ACアダプタ(MicroUSBケーブル)を挿す。
  
※電源スイッチが無い為、挿した瞬間Raspberry Piが起動する。  
緑色のLEDが点滅する。
<img src='https://github.com/J15014/Images/blob/master/RaspberryPi%E9%9B%BB%E6%BA%90.jpg'width='10'hight='10'>  
図3.　Raspberry Pi

##### 時刻の日本化
① ~$ sudo raspi-config を実行  
	以下コンソールより適切なものを選択する  
②「4 Localisation Options」　を選択  
<img src='https://github.com/J15014/Images/blob/master/Raspberrypi%E8%A8%AD%E5%AE%9A%E7%94%BB%E9%9D%A21.png'>  
図4.　Raspberry Pi 設定画面 1  
③「I2 Change Timezone」　を選択  
<img src='https://github.com/J15014/Images/blob/master/Raspberrypi%E8%A8%AD%E5%AE%9A%E7%94%BB%E9%9D%A22.png'>  
図5.　Raspberry Pi 設定画面 2  
④Asiaを選択  
⑤Tokyoを選択  
⑥Finishを選択  
Finishを選択した後、コンソールに下記図が表示される  
<img src='https://github.com/J15014/Images/blob/master/%E6%99%82%E5%88%BB%E8%A8%AD%E5%AE%9A%E5%AE%8C%E4%BA%86.png'>  
図6.　時刻設定完了後コンソール画面  
⑦dateコマンドで確認する  

