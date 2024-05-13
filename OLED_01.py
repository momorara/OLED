
#!/usr/bin/python

"""
###########################################################################
# OLEDに文字を表示

2024/03/02  start
2024/03/03  OLED組み込みフォントを使用して文字を表紙する。
            ただし、文字が小さく、英数字のみ、反面文字数は多く表示できます。

############################################################################
"""

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
import time

# Raspberry Pi 4以降の場合、port=1を指定
serial = i2c(port=1, address=0x3C)

# その他の初期化パラメータを設定（必要に応じて）
device = ssd1306(serial, width=128, height=32) # 必要に応じ64

# # OLEDにテキストを表示する例
# with canvas(device) as draw:
#     draw.text((0, 0), "Hello, OLED!", fill="white")

def oled_text(line1,line2,line3):
    with canvas(device) as draw:
        draw.text((0,  0), line1, fill="white")
        draw.text((0, 11), line2, fill="white")
        draw.text((0, 22), line3, fill="white")

#main function
def main():
    print ('Program is running...')
    print ('Please press Ctrl+C to end the program...')
    print("内部フォントで表示します。")
    line1 = "01234567890123456789"
    line2 = "abcdefghijklmnopqrstu"
    line3 = "ABCDEFGHIJKLMNOPQRSTU"
    print(line1)
    print(line2)
    print(line3)
    oled_text(line1,line2,line3)
    time.sleep(5)
    device.clear()
    line1 = "0123456"
    line2 = "a      klmnopqrstu"
    line3 = "ABCDEFG     NOPQRSTU"
    oled_text(line1,line2,line3)
    time.sleep(5)

if __name__ == '__main__':
    try:
        main()
    #when 'Ctrl+C' is pressed,child program destroy() will be executed.
    except KeyboardInterrupt:
        pass
    except ValueError as e:
        print(e)
