
#!/usr/bin/python

"""
###########################################################################
# OLEDに四角、点、線を表示

2024/03/02  start
2024/03/05  デモを増やした

############################################################################
"""

from luma.core.render import canvas
from luma.oled.device import ssd1306
import time

# SSD1306 ディスプレイの初期化
# device = ssd1306(port=1, address=0x3C)
# serial = i2c(port=1, address=0x3C)
# device = ssd1306(serial, width=128, height=32) # 必要に応じ64
device = ssd1306(port=1, address=0x3C, width=128, height=32)

def oled_square(x1,y1,x2,y2,color):
    if color == 0:
        #矩形の描画:
        with canvas(device) as draw:
            draw.rectangle((x1,y1,x2,y2), outline="white",fill="black")
    if color == 1:
        #矩形の描画:
        with canvas(device) as draw:
            draw.rectangle((x1,y1,x2,y2), outline="white",fill="white")

def oled_point(x,y):
    with canvas(device) as draw:
        draw.point((x,y), fill="white") 

def oled_line(x1,y1,x2,y2):
    with canvas(device) as draw:
        draw.line((x1,y1,x2,y2), fill="white")

# 複数の画像を書く場合は、withの中で処理
# with canvas(device) as draw:
#     draw.point((1, 1), fill="white")
#     draw.point((127, 1), fill="white")
#     draw.point((1, 63), fill="white")
#     draw.point((127, 63), fill="white")


def main():
    print ('Program is running...')
    print ('Please press Ctrl+C to end the program...')

    print("四角を描画")
    oled_square(0, 0, 127, 31,1)
    time.sleep(3)
    oled_square(0, 0, 127, 31,0)
    time.sleep(3)
    device.clear()
    for x in range(0,127,5):
        oled_square(0, 10, x, 21,1)
        time.sleep(0.1)
    time.sleep(2)
    for x in range(0,127,5):
        xx = 0
        if x > 20:
            xx = x -20
        oled_square(xx ,10, x, 21,1)
        time.sleep(0.1)
    time.sleep(2)

    print("点を描画")
    oled_point(0, 0)
    time.sleep(3)
    oled_point(127, 0)
    time.sleep(3)
    oled_point(0, 31)
    time.sleep(3)
    oled_point(127, 31)
    time.sleep(3)

    print("線を描画")
    oled_line(0, 0, 127, 31)
    time.sleep(3)
    oled_line(127, 0, 0, 31)
    time.sleep(3)

    device.clear()

if __name__ == '__main__':
    try:
        main()
    #when 'Ctrl+C' is pressed,child program destroy() will be executed.
    except KeyboardInterrupt:
        pass
    except ValueError as e:
        print(e)