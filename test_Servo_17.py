#!/usr/bin/python
"""
2024/02/27  pi5のためgpiozeroに置き換え
2024/02/29  Servoのテストプログラム
"""
from gpiozero import Servo
import time

servo = Servo(17)

#print message at the begining ---custom function
def print_message():
    print ('Program is start')
    print ('Please press Ctrl+C to end the program...')


# #main function
def main():
    #print info
    print_message()

    # max min mid で制御
    print("最小 position")
    servo.min()
    time.sleep(3)

    print("中間 position")
    servo.mid()
    time.sleep(3)

    print("最大 position")
    servo.max()
    time.sleep(3)
    print()

    # -1 (最小) から 1 (最大) までのスケールでサーボを特定の位置に移動することもできますvalue。0 は中間点です。
    print("最小 position")
    servo.value = -1
    time.sleep(3)

    print("中間 position")
    servo.value = 0
    time.sleep(3)

    print("最大 position")
    servo.value = 1
    time.sleep(3)

# if run this script directly ,do:
if __name__ == '__main__':
    try:
        main()
    #when 'Ctrl+C' is pressed,child program destroy() will be executed.
    except KeyboardInterrupt:
        pass
    pass
