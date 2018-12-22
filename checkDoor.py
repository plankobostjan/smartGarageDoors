#!/usr/bin/python

#Program, ki trenutno se ni v uporabi.
#Sicer namenjen prevrjanju stanja garaznih vrat (odprta/zaprta/priprta).
#Se zna v nadaljevanju zelo spremeniti.

import RPi.GPIO as GPIO #import the GPIO library
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)

name = "Bostjan"
print("Hello " + name + "!")

if GPIO.input(5) == False:
    print("Door is open")
elif GPIO.input(g) == False:
    print("Door is closed")
else:
    print("Door is ajar")
