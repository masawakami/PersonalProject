# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 09:17:11 2019
RaspberryPi Zero and 3 B+
温度、湿度センサーのテスト
@author: Souichirou Kikuchi
"""

import RPi.GPIO as GPIO
from time import sleep
import dht11 # 温湿度センサーモジュール
import datetime # 時間取得
import csv # csv
import boto3
# form setenv import ACCESS_ID1, SECRET_ACCESS_KEY1, DEFAULT_REGION1

TEMP_SENSOR_PIN = 4 # 温湿度センサーのピンの番号
INTERVAL = 600 # 監視間隔（秒）
RETRY_TIME = 2 # dht11から値が取得できなかった時のリトライまので秒数
MAX_RETRY = 10 # dht11から温湿度が取得できなかった時の最大リトライ回数

# 不快指数の計算
A = 0.81
B = 0.01
C = 0.99
D = 14.3
E = 46.3
Discomfort = 0

# 失敗カウント
i = 0

class EnvSensorClass: # 温湿度センサークラス
    def GetTemp(self): # 温湿度を取得
        instance = dht11.DHT11(pin=TEMP_SENSOR_PIN)
        retry_count = 0
        while True: # MAX_RETRY回まで繰り返す
            retry_count += 1
            result = instance.read()
            if result.is_valid(): # 取得できたら温度と湿度を返す
                return result.temperature, result.humidity
            elif retry_count >= MAX_RETRY:
                return 99.9, 99.9 # MAX_RETRYを過ぎても取得できなかった時に温湿度99.9を返す
            sleep(RETRY_TIME)

GPIO.setwarnings(False) # GPIO.cleanup()をしなかった時のメッセージを非表示にする
GPIO.setmode(GPIO.BCM) # ピンをGPIOの番号で指定

#main
try:
    if __name__ == "__main__":
        env = EnvSensorClass()
        while True:
            temp, hum = env.GetTemp() # 温湿度を取得
            if temp != 99.9:
                Discomfort = A * temp + B * hum * (C * temp - D) + E
                if Discomfort > 85: # 不快指数の判定
                    Est = "暑くてたまらない"
                elif Discomfort > 79:
                    Est = "暑くて汗が出る"
                elif Discomfort > 74:
                    Est = "やや暑い"
                elif Discomfort > 69:
                    Est = "暑くない"
                elif Discomfort > 64:
                    Est = "快い"
                elif Discomfort > 59:
                    Est = "何も感じない"
                elif Discomfort > 54:
                    Est = "肌寒い"
                else:
                    Est = "寒い"
                date = datetime.datetime.now()
                print("時間 = "+ date.strftime("%Y/%m/%d-%H:%M:%S"))
                print("温度 = ", temp, "C")
                print("湿度 = ", hum, "％")
                print("不快指数 = ", round(Discomfort))
                print(Est)

                with open("./data/environment_data.csv","a") as f:
                    writer = csv.writer(f)
                    writer.writerow([date.strftime("%Y/%m/%d-%H:%M:%S"),temp,hum,round(Discomfort)])

                LocalFilePath = "/home/pi/codes/piper/DHT11_Python/data/environment_data.csv" # csvファイルの保存先
                Dest_Bucket_Name = "personalproject-ms1"
                Dest_Bucket_Key_Name = "environment_data.csv"

                s3 = boto3.resource('s3')
                s3.meta.client.upload_file(LocalFilePath, Dest_Bucket_Name, Dest_Bucket_Key_Name)
                sleep(INTERVAL)
            else:
                i = i + 1 # カウントアップ
                print("リトライ", i , "回目") # リトライ回数のカウント
                sleep(INTERVAL)
except KeyboardInterrupt:
    pass
GPIO.cleanup()
