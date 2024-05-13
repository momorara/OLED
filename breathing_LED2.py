#!/usr/bin/python
"""
2024/02/27  pi5のためgpiozeroに置き換え
"""
from gpiozero import PWMLED
import time

led = PWMLED(27)


#print message at the begining ---custom function
def print_message():
    print ('Program is start')
    print ('Please press Ctrl+C to end the program...')

# #main function
def main():
    #print info
    print_message()

    n = 5
    while n > 0:
        print(">>   点灯 duty cycle  ")
        #increase duty cycle from 0 to 100
        for dc in range(0,100,10):
            #change duty cycle to dc
            led.value = dc/100
            time.sleep(0.1)
        led.value = 1
        time.sleep(0.5)
        print(">>   消灯 duty cycle   ")
        #decrease duty cycle from 100 to 0
        for dc in range(100,0,-10):
            #change duty cycle to dc
            led.value = dc/100
            time.sleep(0.1)
        led.value = 0
        time.sleep(0.7)
        n = n -1 

# if run this script directly ,do:
if __name__ == '__main__':
    try:
        main()
    #when 'Ctrl+C' is pressed,child program destroy() will be executed.
    except KeyboardInterrupt:
        pass
    pass
