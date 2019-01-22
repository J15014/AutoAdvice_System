import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import datetime
# mysql connect
import mysql.connector

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# read data using pin 14
# instance = DHT22.DHT22(pin=14)
sensor = Adafruit_DHT.DHT22

pin =15

time_count = 1
count = 0

total_temp = 0
total_humid = 0



while True:

    humidity, temperature =Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        # print("Last valid input: " + str(datetime.datetime.now()))
        # print("Temperature: %d C" % result.temperature)
        # print("Humidity: %d %%" % result.humidity)
        total_temp += temperature
        total_humid += humidity

	date = datetime.datetime.now()
	date_txt = date.strftime('%Y-%m-%d %H:%M:%S')

        count += 1

        if count == time_count:

            conn = mysql.connector.connect(user='j15009', password='j15009', host='localhost', port='3306', database='live')
            cur = conn.cursor()

            sql = "insert into environments(temperature,humid,uploaded) values ("+ str(total_temp / count) +","+ str(total_humid / count) +",'"+ date_txt +"');"

            try:
                cur.execute(sql)
                conn.commit()
            except:
                conn.rollback()
                raise

            cur.close()
            conn.close()

            break

    time.sleep(1)
