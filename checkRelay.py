#!/usr/bin/python

#Program namenjen preklopu releja iz zaprtega v odprto stanje, ce je le ta predolgo zaprt
#Uporabljen kot resitev problema #1 (glej BUGS.md)

import RPi.GPIO as GPIO #import the GPIO library
import time
import datetime
from datetime import datetime
import os
import logging
logging.basicConfig(filename='logs/checkRelay.log')

homeFolder=os.environ['HOME']
path=homeFolder+'/.garage/logs'

def checkLogFilePath():
    if(not os.path.exists(homeFolder+'/.garage')):
        os.mkdir(homeFolder+'/.garage')
    if(not os.path.exists(path)):
        os.mkdir(path)

logger=logging.getLogger(__name__)

checkLogFilePath()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
GPIO.output(12, GPIO.HIGH)

while True:
    if GPIO.input(12) == False:
        time.sleep(1.5)
        if GPIO.input(12) == False:
            logger.warning('Relay closed for too long.')
            GPIO.output(12, not GPIO.input(12))
            logger.info('Relay opened automatically.')
    time.sleep(.5)
GPIO.cleanup()
