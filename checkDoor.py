#!/usr/bin/python

#Program, ki trenutno še ni v uporabi.
#Sicer namenjen prevrjanju stanja garažnih vrat (odprta/zaprta/priprta).
#Se zna v nadaljevanju zelo spremeniti.

import RPi.GPIO as GPIO #import the GPIO library
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)

name = "Bostjan"
print("Hello " + name + "!")

if GPIO.input(11) == False:
    print("Door is open")
elif GPIO.input(13) == False:
    print("Door is closed")
else:
    print("Door is ajar")
