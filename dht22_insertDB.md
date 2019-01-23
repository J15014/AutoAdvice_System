#### GPIO,DHT22に必要なライブラリ
```
import RPi.GPIO as GPIO
import Adafruit_DHT
```
#### 時間管理用ライブラリ
```
import datetime
```
#### mysql 接続用ライブラリ
```
import mysql.connector
```
#### GPIOポートの初期化
```
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
```
#### センサー種別を指定し、センサーを接続しているピンを設定
```
sensor = Adafruit_DHT.DHT22
pin = 15
```
#### 気温・湿度の取得と現在時刻の取得
```
total_temp, total_humid = 0
humidity, temperature =Adafruit_DHT.read_retry(sensor, pin)
if humidity is not None and temperature is not None:
    total_temp += temperature
    total_humid += humidity
date = datetime.datetime.now()
date_txt = date.strftime('%Y-%m-%d %H:%M:%S')
```
#### データベースへ転送
```
conn = mysql.connector.connect(user='<ユーザ名>', password='<パスワード>', host='<アドレス>', port='<>ポート', database='<DB名>')
cur = conn.cursor()
sql = "insert into environments(temperature,humid,uploaded) values ("+ str(total_temp) +","+ str(total_humid) +",'"+ date_txt +"');"
try:
    cur.execute(sql)
    conn.commit()
except:
    conn.rollback()
    raise
cur.close()
conn.close()
```

