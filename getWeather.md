# getWeather

### 1.概要
- 外気温度・湿度・天気をAPIを利用して取得する為のプログラム

### 2. インポート , 変数宣言等
- インポート　
    ~~~  
        import requests
        import json
        import mysql.connector
        import datetime
    ~~~      
- 変数宣言　<br>
・OpenWeatherMapのAPIを使用するためのベースURL
    ~~~
    urlbase = 'https://api.openweathermap.org/data/2.5/'
    # /weather?lat={lat}&lon={lon}'
    api_key = '取得したAPIキー'
    ~~~
・Dark skyのAPIを使用するためのベースURL
    ~~~
    urlbase2 = 'https://api.darksky.net/forecast/'
    # /Key/latitude,longitude
    api_key2 = '取得したAPIキー'
    ~~~
・Dark skyの天気判別用辞書データ(参考サイト)
    ~~~
    #Dark sky https://darksky.net/dev/docs#response-format
    weathers={'clear-day':1, 'clear-night':2, 'rain':3, 'snow':4, 'sleet':5, 'wind':6,
    'fog':7, 'cloudy':8, 'partly-cloudy-day':9, 'partly-cloudy-night':10, 'hail':11,
    'thunderstorm':12, 'tornado':13}
    ~~~

### 3. プログラム本文
- 緯度・経度の代入
    ~~~
        lat = '34.98'
        lon = '138.38'
        # shizuoka [34.98, 138.38]
    ~~~
- 日付・時間の取得
    ~~~
        date = datetime.datetime.now()
        date_str = date.strftime('%Y-%m-%d %H:%M:%S')
    ~~~
- 外気温度・湿度の取得
    ~~~
        # OpenWeatherMapのAPIのベースURL
        url1 = urlbase + 'weather?lat='+ lat +'&lon='+ lon +
                                    '&appid=' +api_key +'&units=metric'
        # レスポンスデータ取得
        response = requests.get(url1)

        # レスポンスの有無判定
        if response.status_code != 200:
            raise Exception('return status code is {}'.format(response.status_code))

        # json形式を分解し気温データを取得
        rate = json.loads(response.text)
        open_temp = rate['main']['temp']

        # Forecast
        # Dark skyのAPIのベースURL
        url2 = urlbase2 + api_key2 +'/'+lat+','+lon
        response = requests.get(url2)

        # レスポンスの有無判定
        if response.status_code != 200:
            raise Exception('return status code is {}'.format(response.status_code))

        # json形式を分解して湿度・天気データを取得
        rate = json.loads(response.text)
        open_humid = rate['currently']['humidity']
        open_weather = weathers[str(rate['currently']['icon'])]

        # デバッグ用
        # print(date_str)
        # print('TEMP:' + str(open_temp))
        # print('HUMID:' + str(open_humid))
    ~~~

- データベースへの挿入
    ~~~
        # Insert To Database
        conn = mysql.connector.connect(user='j15009',
            password='j15009',
            host='localhost',
            port='3306',
            database='live')

        cur = conn.cursor()

        sql = "insert into openweathers(temp,humid,weather,uploaded) values
            ("+ str(open_temp) +","+ str(open_humid) +","
            - str(open_weather) +",'"+ date_str +"');"

        try:
            cur.execute(sql)
            conn.commit()
        except:
            conn.rollback()
            raise

        cur.close()
        conn.close()
    ~~~

### 4.備考
気象情報API比較してみた<br>
https://qiita.com/Barbara/items/93ae7969691164c7c2bc<br>
参考にして気温をOpenWeatherMap、湿度・天気をDark skyを使うことにした
