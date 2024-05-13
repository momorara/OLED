
#!/usr/bin/python

"""
###########################################################################
# OLEDデモ

2024/03/02  start

############################################################################
"""

import random
from time import sleep
from luma.core.render import canvas
from luma.oled.device import ssd1306

# SSD1306 ディスプレイの初期化
device = ssd1306(port=1, address=0x3C)
# device = ssd1306(port=1, address=0x3C, width=128, height=32)

# 描画対象の図形の数
num_shapes = 30

def main():
    print ('Program is running...')
    print ('Please press Ctrl+C to end the program...')
    # デモプログラムの実行
    try:
        for _ in range(20):  # 50回のアニメーションループ
            with canvas(device) as draw:
                for _ in range(num_shapes):
                    # ランダムな座標と白または黒の色で直線、矩形、円を描画
                    x, y = random.randint(0, 127), random.randint(0, 50)
                    color = "white" if random.choice([True, False]) else "black"
                    shape_type = random.choice(["line", "rectangle", "ellipse", "point"])

                    if shape_type == "line":
                        draw.line((x, y, x + 10, y + 10), fill=color)
                    elif shape_type == "rectangle":
                        draw.rectangle((x, y, x + 10, y + 10), outline=color, fill=color)
                    elif shape_type == "ellipse":
                        draw.ellipse((x, y, x + 10, y + 10), outline=color, fill=color)
                    elif shape_type == "point":
                        draw.point((x, y), fill=color)

            sleep(0.2)  # アニメーションのためのウェイト

    finally:
        # ディスプレイをクリアして終了
        device.clear()


if __name__ == '__main__':
    try:
        main()
    #when 'Ctrl+C' is pressed,child program destroy() will be executed.
    except KeyboardInterrupt:
        pass
    except ValueError as e:
        print(e)
