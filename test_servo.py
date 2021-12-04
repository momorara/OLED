#!/usr/bin/python

"""
test_servo.py

サーボーモーターのテスト

2019/11/11  一般的なサーボーモーターを制御します。
            サーボにより制御の仕方が違うので、参考にして修正してください。


scp -r GPIO  pi@192.168.68.129:/home/pi/GPIO
"""

import RPi.GPIO as GPIO
import time
import os

SERVOPin = 17

GPIO.setwarnings(False)
# GPIOのピンレイアウトを設定する
GPIO.setmode(GPIO.BCM)
# （GPIO 18）をサーボ信号線（黄色のワイヤー）に接続
# （GPIO 18) はPWM信号を送信してサーボモーションを制御します
GPIO.setup(SERVOPin, GPIO.OUT)

# menu info
print("l = 左に移動")
print("r = 右に移動")
print("m = 中央に移動")
print("t = テストシーケンス")
print("q = 停止して終了")

# （GPIO 18)で50HzのPWM信号から始めます。
# 50Hzは非常に多くのサーボで動作するはずです。
# そうでない場合は、必要に応じて周波数で選ぶことができます。	
Servo = GPIO.PWM(SERVOPin, 50)	

while True:
					

	# このコマンドは、サーボの左位置を設定します
    Servo.start(2.5)
    GPIO.cleanup()

	# ここで、はサーボが回る方向を尋ねます。
    input_data = input("回転方向選択： ") 
    print(input_data)

    GPIO.setwarnings(False)
    # GPIOのピンレイアウトを設定する
    GPIO.setmode(GPIO.BCM)
    # （GPIO 18）をサーボ信号線（黄色のワイヤー）に接続
    # （GPIO 18) はPWM信号を送信してサーボモーションを制御します
    GPIO.setup(SERVOPin, GPIO.OUT)


	# You can play with the values.
	# 7.5はほとんどの場合、中央の位置です
	# 12.5は、180度右への移動の値です
	# 2.5は、左に-90度移動した場合の値です
    if(input_data == "t"):
        print("中心位置に移動：")
        Servo.ChangeDutyCycle(7.5)
        time.sleep(2)
        print("右の位置に移動:")
        Servo.ChangeDutyCycle(12.5)
        time.sleep(2)
        print("左の位置に移動：")
        Servo.ChangeDutyCycle(2.5)
        time.sleep(2)
        # this stops the PWM signal
        #print("開始位置に戻る")


	# 右方向
    elif(input_data == "r"):

		# 移動に必要なステップ数
        steps = input("steps (1 - 10): ") 
        print( steps,"右に何ステップ?")
        stepslength = (12.5-2.5) / int(steps)
        for Counter in range(int(steps)):
            step = stepslength * (Counter + 1)+ 2.5
            if step > 2.4:
                Servo.ChangeDutyCycle(step)
                print(stepslength * (Counter + 1)+ 2.5)
                time.sleep(0.5)
			
        time.sleep(1)	

    elif(input_data == "rr"):
        Servo.ChangeDutyCycle(12.5)
        time.sleep(1)

    elif(input_data == "ll"):
        Servo.ChangeDutyCycle(2.5)
        time.sleep(1)	

    elif(input_data == "mm"):
        Servo.ChangeDutyCycle(7.5)
        time.sleep(1)	

	# move to the center position
    elif(input_data == "m"):
        print("中心位置に戻る.")
        Servo.start(7.5)
        time.sleep(1)

	
	# move to the left
    elif(input_data == "l"):
        print("最大右位置に移動してから左位置に移動する.")
        Servo.start(12.5)
        # how many steps...
        steps = input("steps (1 - 10): ") 
        print (steps, "右に何ステップ?")
        stepslength = (12.5-2.5) / int(steps)
        for Counter in range(int(steps)):
            step = 12.5 - (stepslength * (Counter + 1))
            if step > 2.4 :
                Servo.ChangeDutyCycle(step)
                print (12.5 - (stepslength * (Counter + 1)))
                time.sleep(0.5)
		
        time.sleep(1)

	
	# close program
    elif(input_data == "q"):
        print("プログラムを停止して終了.......")
        os._exit(1)
        GPIO.cleanup()
		
	# input not valid
    else:
        print("入力が無効です！")