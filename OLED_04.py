
#!/usr/bin/python

"""
###########################################################################
# OLEDに画像を表示

2024/03/02  start
2024/03/03  pngファイルをOLED上に表示し、白黒反転します。

############################################################################
"""

from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import Image
import time

# SSD1306 ディスプレイの初期化
device = ssd1306(port=1, address=0x3C)
# device = ssd1306(port=1, address=0x3C, width=128, height=32)

def oled_image(image):
    # 画像を2値に変換
    binary_image = image.convert("1")

    # # 2値画像の保存（オプション）
    # binary_image.save("binary_image.png")

    # 画像の描画
    with canvas(device) as draw:
        draw.bitmap((0, 0), binary_image, fill="white")
    time.sleep(4)

    # 2値画像を白黒反転
    inverted_image = Image.eval(binary_image, lambda x: 255 - x)

    # 画像の描画
    with canvas(device) as draw:
        draw.bitmap((0, 0), inverted_image, fill="white")
    time.sleep(4)
    device.clear()


# #main function
def main():
    print ('Program is running...')
    print ('Please press Ctrl+C to end the program...')
    
    # 画像ファイルの読み込み
    image = Image.open("kingyo.png")
    # 画像の表示
    oled_image(image)

    # 画像ファイルの読み込み
    image = Image.open("shiyachi.png")
    # 画像の表示
    oled_image(image)

    # 画像ファイルの読み込み
    image = Image.open("tonbo.png")
    # 画像の表示
    oled_image(image)

    # 画像ファイルの読み込み
    image = Image.open("keybord.png")
    # 画像の表示
    oled_image(image)

if __name__ == '__main__':
    try:
        main()
    #when 'Ctrl+C' is pressed,child program destroy() will be executed.
    except KeyboardInterrupt:
        pass
    except ValueError as e:
        print(e)