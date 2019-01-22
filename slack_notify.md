### Slack通知機能
cronで15分毎起動する設定<br>
その時点での1時間後の不快指数に応じて通知する

### Slack Incomming Webhooksを登録する
1. Slackのアプリで、「Add an app or custom integration」を押す。<br>
2. ブラウザが立ち上がり、右上にある「Build your own」を押す。<br>
3. 「Make a custom integration」を押す。<br>
4. 「Incoming Webhook」を押す。<br>
5. 投稿先のチャンネルを選んで作成すると、URLが出てくるのでコピーしておく。


slack_notify.py

```
import slackweb
import mysql.connector
#-*- coding: utf-8 -*-

def slack_alert(msg):
    slack.notify(
        text ="1時間後" + msg,
        username = "通知君",
        icon_emoji = ":waxing_crescent_moon:"
    )

conn = mysql.connector.connect(user='j15009', password='j15009', host='localhost', port='3306', database='live')

cur = conn.cursor()

sql = "select predcomfort from arpredicts where id = (select max(id) from arpredicts);"

message = ""

try:
    cur.execute(sql)
    result = cur.fetchall()
    # print(result[0][0])
    comfort = result[0][0]

    slack = slackweb.Slack(url="< **コピーしたURL** >")

    if comfort < 55:
        message = "寒くなるだろう"
        slack_alert(message)
    elif comfort < 60:
        message = "肌寒くなるだろう"
        slack_alert(message)
    elif comfort < 75:
        pass
    elif comfort < 80:
        message = "やや暑くなるだろう"
        slack_alert(message)
    elif comfort < 85:
        message = "暑くて汗がでるだろう"
        slack_alert(message)
    else:
        message = "暑くてたまらないだろう"
        slack_alert(message)

except:
    pass

cur.close()
conn.close()
```
