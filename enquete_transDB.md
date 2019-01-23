### アンケートのDB転送
##### ファイルの実行形式、引数５個
```
python3 フルパス/transDB.py 1 2 3 4 5
```
##### 必要なライブラリ
```
import sys
import datetime
import mysql.connector
```
##### 実行時引数として受け取るデータの扱い
- アンケートを縮小したため、部屋の場所、感じる快適度、エアコン稼働中か否か、エアコンの設定温度、エアコンの運転モードだけ使用

```
argv = sys.argv
gender = 0
place = argv[1]
people = 0
comfort = argv[2]
windowopen = 0
blindopen = 0
roomtemp =0
countpc = 0
airflg = argv[3]
airtemp = argv[4]
airmode = argv[5]
```
##### 日時取得
```
date = datetime.datetime.now()
date_txt = date.strftime('%Y-%m-%d %H:%M:%S')
```
##### 環境データ接続設定と取得
```
conn = mysql.connector.connect(user='j15009', password='j15009', host='localhost', port='3306', database='live')
cur = conn.cursor()

sql = 'select temperature,humid from live.environments order by id desc limit 1;'

cur.execute(sql)

room = cur.fetchall()
print(room[0][0], room[0][1])
roomtemp = str(room[0][0])
roomhumid = str(room[0][1])
```
##### データベース接続設定（異なるDBに切り替え）
- アンケート保存のDBと環境データのDBが本研究では異なるため

```
conn = mysql.connector.connect(user='<ユーザ名>', password='<パスワード>', host='<アドレス>', port='<ポート>', database='<DB名>')
cur = conn.cursor()
```
##### SQL文の構成
```
sql = "insert into Questions("
sql += "place, "
sql += "comfort, "
sql += "roomtemp, roomhumid, airflg, airtemp, "
sql += "airmode, uploaded) values ("
sql += str(place) +","
sql += str(comfort) +","
sql += roomtemp +","+ roomhumid +","+ str(airflg) +","+ str(airtemp) +","
sql += str(airmode) +",'"+ str(date_txt) +"');"
```
##### SQL実行
```
try:
    cur.execute(sql)
    conn.commit()
except:
    conn.rollback()
    raise

cur.close()
conn.close()
```
