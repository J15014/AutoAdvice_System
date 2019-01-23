## AutoRegression_temp_humid (分析)


### 1. 概要
- センサー等を用いて取得したデータをデータベースから取り出し、ARモデルを用いた分析を行い、15分後の推定温度あるいは湿度を出す。
- それを推定データとして、データベースに格納する。


### 2. プログラム
- #### インポート
~~~
import datetime
import mysql.connector
~~~

- #### 関数
    - データの追加
~~~
    def add_data(value, data):
        array = [0]
        array[0] = value
        for i in range(99):
            array.append(data[i])
        return array
~~~
    - データの計算
~~~
    def calculation(coefficient, data):
        predict = 0
        for raw in range(100):
            predict += coefficient[raw] * data[raw]
        return predict
~~~
    - データの挿入あるいは更新
~~~
    def transfer(cur, conn, predtime, predtemp, predhumid):
        sql_check = "select count(*) from arpredicts where pdatetime
        between '" + str(predtime - datetime.timedelta(minutes=5)) +
        "' and '"+ str(predtime + datetime.timedelta(minutes=5)) +"'
        order by pdatetime desc;"

        cur.execute(sql_check)
        check_pred = cur.fetchone()

        print("pred check 0:not exist  1:exist   " + str(check_pred[0]))

        if check_pred[0] is 0:
            # 挿入先が存在しないときは挿入
            sql = "insert into arpredicts (predtemp,predhumid,pdatetime)
            values('"+ str(predtemp)+"' , '"+ str(predhumid) +"' ,
            '"+ str(predtime) +"');"

            try:
                cur.execute(sql)
                conn.commit()
            except:
                conn.rollback()
                raise
        else:
            # 挿入先が存在するときは更新
            sql = "update arpredicts set predtemp = '"+ str(predtemp)
            +"' , predhumid = '"+ str(predhumid) +"' where pdatetime
            between '" + str(predtime - datetime.timedelta(minutes=5))
            + "' and '"+ str(predtime + datetime.timedelta(minutes=5)) +"'
            limit 1;"

            try:
                cur.execute(sql)
                conn.commit()
            except:
                conn.rollback()
                raise
~~~
- #### 本プログラム
~~~
  #
  # 室内気温自己回帰モデルの計算開始
  # a:室内気温自己回帰モデル計算用係数(20件)
  #
  a = [
      0.049643488,
      -0.142968696,
      0.144780507,
      -0.041845698,
      -0.119256862,
      0.011075968,
      0.106320543,
      0.092912269,
      -0.100997805,
      0.108984568,
      -0.103279867,
      0.059581665,
      -0.001641631,
      0.037398642,
      -0.096233029,
      0.021952302,
      0.114638369,
      -0.012408893,
      -0.088078599,
      -0.007527659,
      -0.001025588,
      0.009868722,
      0.038451848,
      0.023985138,
      -0.032642228,
      -0.022768856,
      -0.01059351,
      0.020559004,
      0.028479969,
      -0.049987733,
      -0.020670348,
      0.057164398,
      0.044407984,
      -8.52335E-05,
      -0.056549216,
      -0.018606033,
      0.038335437,
      -0.008450741,
      -0.006967455,
      -0.004136943,
      0.016429691,
      -0.003743888,
      0.004688568,
      -0.025729441,
      0.014099188,
      0.027559498,
      -0.015136274,
      -0.013520953,
      0.010057704,
      -0.052091822,
      0.054282376,
      -0.007243412,
      -0.011581216,
      0.000235152,
      0.025518745,
      -0.056186418,
      0.046290013,
      0.003842748,
      0.012672675,
      -0.057326111,
      -0.011895871,
      0.077678325,
      0.03144621,
      -0.106976139,
      -0.04385755,
      0.158747493,
      0.02355849,
      -0.140899225,
      0.00416816,
      0.020653213,
      0.122711142,
      -0.13244089,
      0.051214057,
      -0.09785207,
      0.076683908,
      0.123223621,
      -0.199380756,
      0.054898728,
      0.063276565,
      0.008562045,
      -0.057973712,
      -0.046023256,
      0.031142919,
      0.006538097,
      -0.046846382,
      0.097111237,
      -0.013784303,
      0.005542974,
      -0.138554937,
      0.086653014,
      0.030575681,
      0.072797822,
      -0.070974771,
      -0.18127385,
      0.12979379,
      0.254937686,
      -0.185239865,
      -0.283307683,
      0.084850582,
      1.105766368
  ]
  # データ取得時が降順なので後ろから配列に入れる
  a.reverse()

  # 直近5時間のデータを取得
  raws = []
  conn = mysql.connector.connect(user='j15009', password='j15009', host='localhost', port='3306', database='live')
  cur = conn.cursor()
  sql = "select temperature,humid,uploaded from environments order by id desc limit 1500;"
  cur.execute(sql)
  # 出力したすべての行を配列化
  raw_data = cur.fetchall()

  # 直近5時間を15分毎のデータだけを抽出し、配列へ格納
  cnt = 0
  for val in raw_data:
      if cnt % 15 == 0:
          raws.append(val[0])
      cnt += 1

  print(raws)
  # 最新の時間を取得
  last_datetime = raw_data[0][2]
  print("last datetime    : "+ str(last_datetime))

  # 15分先の室内気温を予測
  predict_15m = calculation(a, raws)
  # 15分後の日時を設定
  predict_15_datetime = last_datetime + datetime.timedelta(minutes = 15)
  print("15 minutes later : "+ str(predict_15_datetime) + " : " + str(predict_15m) +" C")

  # 予測値を含めた計算用配列
  raws = add_data(predict_15m, raws)
  predict_30m = calculation(a, raws)
  # 30分後の日時を設定
  predict_30_datetime = predict_15_datetime + datetime.timedelta(minutes = 15)
  print("30 minutes later : "+ str(predict_30_datetime) + " : " +  str(predict_30m) +" C")

  # 45分後
  raws = add_data(predict_30m, raws)
  predict_45m = calculation(a, raws)
  # 30分後の日時を設定
  predict_45_datetime = predict_30_datetime + datetime.timedelta(minutes = 15)
  print("45 minutes later : "+ str(predict_45_datetime) + " : " +  str(predict_45m) +" C")

  # 1時間後
  raws = add_data(predict_45m, raws)
  predict_1h = calculation(a, raws)
  # 30分後の日時を設定
  predict_1h_datetime = predict_45_datetime + datetime.timedelta(minutes = 15)
  print("1h minutes later : "+ str(predict_1h_datetime) + " : " +  str(predict_1h) +" C")

  #
  # 室内気温自己回帰モデルによる予測終了

  #
  # 室内湿度自己回帰モデル開始
  # b:室内湿度自己回帰モデル計算用係数(20件)
  #
  b = [
      0.005278561,
      -0.023399655,
      -0.05403589,
      0.069012198,
      -0.061007493,
      0.025958833,
      0.067262516,
      -0.013704623,
      -0.078684613,
      0.071347234,
      -0.116254154,
      0.158174669,
      -0.039665057,
      -0.047742768,
      -0.058124428,
      0.00629633,
      0.073166247,
      0.015233888,
      -0.021508915,
      0.02005021,
      0.009097221,
      -0.027217978,
      -0.015692476,
      -0.014785155,
      -0.009224511,
      0.077528018,
      -0.099147336,
      0.096524689,
      0.013782622,
      -0.082893583,
      0.057992917,
      0.038499864,
      -0.035079899,
      7.70868E-05,
      -0.023350501,
      -0.005026705,
      0.011793414,
      0.009299983,
      -0.018750484,
      0.016356308,
      0.000593201,
      0.004284011,
      0.000694814,
      0.026708876,
      -0.01657569,
      0.014065024,
      -0.019034278,
      -0.033303871,
      0.032119166,
      0.054662829,
      -0.102534195,
      0.070153749,
      -0.07206286,
      0.004781305,
      0.098744807,
      -0.112603197,
      0.077855462,
      -0.024384095,
      -0.029664952,
      0.093250666,
      -0.06273733,
      -0.008016443,
      -0.037679948,
      0.034344803,
      0.034860333,
      0.028922348,
      -0.045718357,
      -0.016533393,
      0.02901311,
      0.003465084,
      0.03942196,
      -0.084773525,
      -0.044488876,
      0.145483481,
      -0.056009413,
      0.081672564,
      -0.167754054,
      0.095406445,
      0.021420696,
      -0.023201931,
      -0.00903943,
      -0.061698722,
      -0.031299093,
      0.062409978,
      -0.013541174,
      0.049326759,
      -0.073051245,
      0.028534704,
      0.063292701,
      0.002373298,
      -0.019204375,
      -0.069594381,
      -0.035809849,
      0.060396475,
      0.129474047,
      -0.121712979,
      0.040906648,
      0.100748847,
      -0.070031189,
      0.936368672
  ]
  # データ取得時が降順なので後ろから配列に入れる
  b.reverse()

  # 直近5時間のデータを取得
  raws_humid = []
  # 直近5時間を15分毎のデータだけを抽出し、配列へ格納
  cnt = 0
  for val in raw_data:
      if cnt % 15 == 0:
          raws_humid.append(val[1])
      cnt += 1

  print(raws_humid)

  # 15分先の室内気温を予測
  predict_15m_humid = calculation(b, raws_humid)

  # 15分後の日時を表示
  print("15 minutes later : "+ str(predict_15_datetime) + " : " + str(predict_15m_humid) +" %")

  # 予測値を含めた計算用配列
  raws_humid = add_data(predict_15m_humid, raws_humid)

  # 30分先の室内気温を15分先のデータを利用して予測
  predict_30m_humid = calculation(b, raws_humid)
  # 30分後の日時を表示
  print("30 minutes later : "+ str(predict_30_datetime) + " : " +  str(predict_30m_humid) +" %")

  # 45分後
  raws_humid = add_data(predict_30m_humid, raws_humid)
  predict_45m_humid = calculation(b, raws_humid)
  # 45分後の日時を設定
  print("45 minutes later : "+ str(predict_45_datetime) + " : " +  str(predict_45m_humid) +" %")

  # 1時間後
  raws_humid = add_data(predict_45m_humid, raws_humid)
  predict_1h_humid = calculation(b, raws_humid)
  # 30分後の日時を設定
  print("1h minutes later : "+ str(predict_1h_datetime) + " : " +  str(predict_1h_humid) +" %")

  #
  # 室内湿度自己回帰モデルによる予測終了
  #

  ####################################
  #
  # 書き込み処理
  #
  ####################################

  #
  ############# pred 15 ###############
  #
  # テーブル名はテスト用にARモデルはarpredicts
  # ARMAモデルはarmapredictsとしている
  # 本番環境は predictions
  #
  # print(last_datetime + datetime.timedelta(minutes=10))
  # print(last_datetime + datetime.timedelta(minutes=20))
  # 15分先と30分先を求めるため、次回の15分先が既に存在する可能性が高い
  # そのための確認処理：挿入か更新に振り分ける
  # 15分先の結果があるか(ターゲットとなる15分後の前後5分以内に収まる時間の有無を)確認
  transfer(cur, conn, predict_15_datetime, predict_15m, predict_15m_humid)
  transfer(cur, conn, predict_30_datetime, predict_30m, predict_30m_humid)
  transfer(cur, conn, predict_45_datetime, predict_45m, predict_45m_humid)
  transfer(cur, conn, predict_1h_datetime, predict_1h, predict_1h_humid)

  # SQL操作終了
  cur.close()
  conn.close()
~~~

### 3. 備考
自己回帰モデル用の変数はExcelで算出
