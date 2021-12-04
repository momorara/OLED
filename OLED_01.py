"""
OLED-HAT

OLEDとスイッチ2個、LED2個を実装する
デフォルト設定では、
    cpu温度を表示
    sw1押下でLED1点灯
    sw2押下でLED2点灯
    sw1,2同時押下でOLEDにシャットダウンメッセージ
    --> sw1でシャットダウン実行、sw2でシャットダウン中止
node-red画面でcpu温度表示を入力文字表示に変更
sw押下でUI変化

といった動作をするが、基本はこれを参考にユーザーで自由に使えるモノとする。

crontabで デフォルトプログラムおよびnode-redの起動、不起動を設定してもらう。

また、独立プログラムで gpio_gui.py LED_gui.py を提供する。



2021/06/01  開発開始
    01
2021/06/08  プログラムが異常停止する
            「could not convert string to float:」
            文字を数字に変換できなかったようですね。これを対処する。
            *もともと文字列なので、数字に変換せずにそままま表示することとした。
2021/06/09  フラグ用のファイルを作り、そのファイルがなければ、cpu温度を表示、
            あれば、何もしない。
            フラグは、node-redが制御し、フローから文字表示させたい時に表示文字を入れてファイルを作る
2021/06/19  キャンセル修正
2021/12/04  シャットダウン修正
            


scp -r L_remocon pi@192.168.68.126:/home/pi
scp -r OLED/*.py pi@192.168.68.138:/home/pi/OLED
scp -r OLED/*.py pi@172.20.10.6:/home/pi/OLED
"""
import RPi.GPIO as GPIO
import time
import subprocess
import sys
import datetime
import os
from nobu_LIB import Lib_OLED
import timeout_decorator
import unicodedata # 半角、全角の判定
import getpass

# ユーザー名を取得
user_name = getpass.getuser()
print('user_name',user_name)
path = '/home/' + user_name + '/OLED/' # cronで起動する際には絶対パスが必要
# path = '/home/' + 'tk' + '/L_remocon/' # systemdで起動する際にはrootになり絶対パスが必要

disp_size = 32 # or 64
iR_sensor = '4'

# 表示用LED
LED1 = 27
LED2 = 17
# SW
sw1=6
sw2=5

GPIO.setwarnings(False)
#set the gpio modes to BCM numbering
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED1,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(LED2,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup( sw1,GPIO.IN)
GPIO.setup(sw2,GPIO.IN)

###################log print#####################
# 自身のプログラム名からログファイル名を作る
import sys
args = sys.argv
logFileName = args[0].strip(".py") + "_log.csv"
print(logFileName)
# ログファイルにプログラム起動時間を記録
import csv
# 日本語文字化けするので、Shift_jisやめてみた。
f = open(logFileName, 'a')
csvWriter = csv.writer(f)
csvWriter.writerow([datetime.datetime.now(),'  program start!!'])
f.close()
#----------------------------------------------
def log_print(msg1="",msg2="",msg3=""):
    # エラーメッセージなどをプリントする際に、ログファイルも作る
    # ３つまでのデータに対応
    print(msg1,msg2,msg3)
    # f = open(logFileName, 'a',encoding="Shift_jis") 
    # 日本語文字化けするので、Shift_jisやめてみた。
    f = open(logFileName, 'a')
    csvWriter = csv.writer(f)
    csvWriter.writerow([datetime.datetime.now(),msg1,msg2,msg3])
    f.close()
################################################

#print message at the begining ---custom function
def print_message():
    log_print ('|********************************|')
    log_print ('| OLED-HAt_01.py       1         |')
    log_print ('|********************************|')
    print ('Program is start..')
    print ('Please press Ctrl+C to end the program...')

def OLED_disp(OLED_disp_text,timer=0):
    Lib_OLED.SSD1306(OLED_disp_text,disp_size)
    time.sleep(timer)

def temp_read():
    with open(path + 'cpu_temp_data.txt') as f:
        temp = f.read()
        log_print('現在温度',temp)
    return temp

def Readsw1():
    if (GPIO.input(sw1)):
        sw_ = 'on'
    else:
        sw_ = 'off'
    return sw_

def Readsw2():
    if (GPIO.input(sw2)):
        sw_ = 'on'
    else:
       sw_ = 'off'
    return sw_

#main function
def main():
    print_message()
    OLED_disp('welcom OLED-HAT',0)
    print(path)

    count = 19
    while True:

        # cpuの温度を読み取り 20回に一度 表示
        # cpuTemp = 'cpu=' + str(temp_read()) + '度'
        cpuTemp = 'cpu=' + temp_read() + '度'
        count = count + 1
        if count % 20 == 0:
            if not os.path.exists(path + 'flag.txt'):
                # フラグ確認し、フラグが無ければ、cpu温度を表示
                OLED_disp(cpuTemp,0)
            else:
                # フラグがあれば、その中身を表示
                with open(path + 'flag.txt') as f:
                    flow_str = f.read()
                OLED_disp(flow_str,0)
            count = 0

        # スイッチの状態読み取り
        sw1_ = Readsw1()
        sw2_ = Readsw2()
        if sw1_ == 'on' and sw2_ == 'on':# シャットダウン
            OLED_disp('シャットダウン',2)
            OLED_disp(' ',0)
            log_print('シャットダウン')
            OLED_disp('sw1:する sw2:戻る',2)
            cmd = ' '
            time.sleep(1)
            sw1_ = Readsw1()
            sw2_ = Readsw2()
            OLED_disp(' ',0)
            if sw2_ != 'on' and sw1_ == 'on':
                OLED_disp('シャットダウン開始',1)
                OLED_disp('.......',1)
                # 表示用LEDを点灯してみる
                GPIO.output(LED1,GPIO.HIGH) # LED1 on
                GPIO.output(LED2,GPIO.HIGH) # LED2 on
                GPIO.output(LED1,GPIO.HIGH) # LED1 on
                GPIO.output(LED2,GPIO.HIGH) # LED2 on
                OLED_disp('......',0.5)
                OLED_disp('.....',0.5)
                OLED_disp('....',0.5)
                OLED_disp('...',0.5)
                GPIO.output(LED1,GPIO.LOW) # LED1 off
                OLED_disp('..',0.5)
                OLED_disp('.',0.5)
                OLED_disp(' ',0)
                # シャットダウンする場合は # を削除
                print('シャットダウンシーケンス')
                subprocess.run('sudo shutdown now',shell=True)
            else:
                print('キャンセル')
                OLED_disp('キャンセル',1)

        if sw1_ == 'on' and sw2_ == 'off':
            GPIO.output(LED1,GPIO.HIGH)
            time.sleep(1)
            GPIO.output(LED1,GPIO.LOW)

        if sw1_ == 'off' and sw2_ == 'on':
            GPIO.output(LED2,GPIO.HIGH)
            time.sleep(1)
            GPIO.output(LED2,GPIO.LOW)

        time.sleep(0.2)



#define a destroy function for clean up everything after the script finished
def destroy_stop():
    #release resource
    GPIO.cleanup()
#
# if run this script directly ,do:
if __name__ == '__main__':
    # setup()
    try:
        main()
        GPIO.cleanup()
    #when 'Ctrl+C' is pressed,child program destroy() will be executed.
    except KeyboardInterrupt:
        destroy_stop()
    except ValueError as e:
        log_print(e)
        destroy_stop()