
#!/usr/bin/python

"""
###########################################################################
# 外部ライブラリとしておいて、使う場合

2024/03/03  start

############################################################################
"""

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import Image
import time

# Raspberry Pi 4以降の場合、port=1を指定
serial = i2c(port=1, address=0x3C)

# その他の初期化パラメータを設定（必要に応じて）
device = ssd1306(serial, width=128, height=32) # 必要に応じ64

# # OLEDにテキストを表示する例
# with canvas(device) as draw:
#     draw.text((0, 0), "Hello, OLED!", fill="white")

def text(line1,line2,line3):
    with canvas(device) as draw:
        draw.text((0,  0), line1, fill="white")
        draw.text((0, 11), line2, fill="white")
        draw.text((0, 22), line3, fill="white")

from PIL import  ImageFont
# テキストを描画
def textTT(text,size):
    # フォントを指定
    font = ImageFont.truetype("fonts-japanese-gothic.ttf", size)
    with canvas(device) as draw:
        draw.text((0, 0), text, font=font, fill="white")

def square(x1,y1,x2,y2,color):
    if color == 0:
        #矩形の描画:
        with canvas(device) as draw:
            draw.rectangle((x1,y1,x2,y2), outline="white",fill="black")
    if color == 1:
        #矩形の描画:
        with canvas(device) as draw:
            draw.rectangle((x1,y1,x2,y2), outline="white",fill="white")

def point(x,y):
    with canvas(device) as draw:
        draw.point((x,y), fill="white") 

def line(x1,y1,x2,y2):
    with canvas(device) as draw:
        draw.line((x1,y1,x2,y2), fill="white")

def image(image):
    # 画像を2値に変換
    binary_image = image.convert("1")
    # 画像の描画
    with canvas(device) as draw:
        draw.bitmap((0, 0), binary_image, fill="white")

