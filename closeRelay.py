#!/usr/bin/python

#Program namenjen preklopu releja iz zaprtega v odprto stanje, če je le ta predolgo odprt
#Uporabljen kot rešitev problema #1 (glej bugs.md)

import RPi.GPIO as GPIO #import the GPIO library
import time
import datetime
import os

now = datetime.datetime.now()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
GPIO.output(12, GPIO.HIGH)

while True:
    if GPIO.input(12) == False:
        time.sleep(1.5)
        if GPIO.input(12) == False:
            GPIO.output(12, not GPIO.input(12))
    time.sleep(.5)
GPIO.cleanup()
