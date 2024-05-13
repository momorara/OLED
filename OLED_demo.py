
#!/usr/bin/python

"""
###########################################################################

2024/03/03  lib_oledを使うデモ

############################################################################
"""

import lib_oled
import time
from PIL import Image

#main function
def main():
    print ('Program is running...')
    print ('Please press Ctrl+C to end the program...')

    line1 = "01234567890123456789"
    line2 = "abcdefghijklmnopqrstu"
    line3 = "ABCDEFGHIJKLMNOPQRSTU"
    lib_oled.text(line1,line2,line3)
    time.sleep(3)

    lib_oled.textTT("テスト",25)
    time.sleep(3)

    lib_oled.square(0, 0, 127, 31,0)
    time.sleep(3)
    lib_oled.point(50,10)
    time.sleep(3)
    lib_oled.line(127, 0, 0, 31)
    time.sleep(3)

    image = Image.open("tonbo.png")
    lib_oled.image(image)
    time.sleep(3)

if __name__ == '__main__':
    try:
        main()
    #when 'Ctrl+C' is pressed,child program destroy() will be executed.
    except KeyboardInterrupt:
        pass
    except ValueError as e:
        print(e)
