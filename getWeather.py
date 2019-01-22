import requests
import json
import mysql.connector
import datetime

# OpenWeatherMap用の設定
urlbase = 'https://api.openweathermap.org/data/2.5/'
# /weather?lat={lat}&lon={lon}'
api_key = '各自取得してください'

# DarkSky用の設定
urlbase2 = 'https://api.darksky.net/forecast/'
# /Key/latitude,longitude
api_key2 = '各自取得してください'

#Dark sky https://darksky.net/dev/docs#response-format
weathers={'clear-day':1, 'clear-night':2, 'rain':3, 'snow':4, 'sleet':5, 'wind':6, 'fog':7, 'cloudy':8, 'partly-cloudy-day':9, 'partly-cloudy-night':10, 'hail':11, 'thunderstorm':12, 'tornado':13}


def main():
    lat = '34.98'
    lon = '138.38'
    # shizuoka [34.98, 138.38]

    date = datetime.datetime.now()
    date_str = date.strftime('%Y-%m-%d %H:%M:%S')

    # OpenWeatherMap
    url1 = urlbase + 'weather?lat='+ lat +'&lon='+ lon + '&appid=' +api_key +'&units=metric'

    response = requests.get(url1)

    if response.status_code != 200:
        raise Exception('return status code is {}'.format(response.status_code))

    rate = json.loads(response.text)
    open_temp = rate['main']['temp']
    # open_humid = rate['main']['humidity']

    # Forecast
    # if needed
    option = '?exclude=minutely,hourly,daily,alerts,flags'

    url2 = urlbase2 + api_key2 +'/'+lat+','+lon
    response = requests.get(url2)

    if response.status_code != 200:
        raise Exception('return status code is {}'.format(response.status_code))

    rate = json.loads(response.text)
    open_humid = rate['currently']['humidity']
    open_weather = weathers[str(rate['currently']['icon'])]

    # print(date_str)
    # print('TEMP:' + str(open_temp))
    # print('HUMID:' + str(open_humid))


    # Insert To Database
    conn = mysql.connector.connect(user='j15009', password='j15009', host='localhost', port='3306', database='live')
    cur = conn.cursor()

    sql = "insert into openweathers(temp,humid,weather,uploaded) values ("+ str(open_temp) +","+ str(open_humid) +","+ str(open_weather) +",'"+ date_str +"');"

    try:
        cur.execute(sql)
        conn.commit()
    except:
        conn.rollback()
        raise

    cur.close()
    conn.close()


if __name__ == '__main__':
    main()
