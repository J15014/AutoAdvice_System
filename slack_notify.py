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

    slack = slackweb.Slack(url="<https://hooks.slack.com/services/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>")

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
