
#!/usr/bin/python

"""
###########################################################################
# OLEDにTTフォントを使って文字を表示

2024/03/03  start
2024/03/05  5から32ドットの文字を順次表示

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

from PIL import  ImageFont


# テキストを描画
def oled_text(text,size):
    # フォントを指定
    font = ImageFont.truetype("fonts-japanese-gothic.ttf", size)
    with canvas(device) as draw:
        draw.text((0, 0), text, font=font, fill="white")

#main function
def main():
    print ('Program is running...')
    print ('Please press Ctrl+C to end the program...')
    print("外部フォントで表示します。")
    print("30ドット以内の文字を表示できます。")
    for size in range(5,33):
        text = str(size) + "ドット"
        if size < 18:
            text = text + "の文字"
        print("文字サイズ",size)
        oled_text(text,size)
        time.sleep(1)
    time.sleep(5)
    device.clear()


if __name__ == '__main__':
    try:
        main()
    #when 'Ctrl+C' is pressed,child program destroy() will be executed.
    except KeyboardInterrupt:
        pass
    except ValueError as e:
        print(e)