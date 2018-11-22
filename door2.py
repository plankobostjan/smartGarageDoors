#!/usr/bin/python

#Program, ki trenutno še ni v uporabi.
#Sicer namenjen prevrjanju stanja garažnih vrat (odprta/zaprta/priprta).
#Se zna v nadaljevanju zelo spremeniti.

import RPi.GPIO as GPIO #import the GPIO library
import time
import os

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)

name = "Bostjan"
print("Hello " + name + "!")

if GPIO.input(11) == False:
    print("Door is open. Closing...")
    os.system('gpio toggle 1; sleep .60; gpio toggle 1')
elif GPIO.input(13) == False:
    print("Door is closed.")
else:
    print("Door is ajar. Toggling.")
    os.system('gpio toggle 1; sleep .60; gpio toggle 1')
    time.sleep(5)
    if GPIO.input(11) == False:
        print("Door is open. Closing...")
        os.system('gpio toggle 1; sleep .60; gpio toggle 1')
