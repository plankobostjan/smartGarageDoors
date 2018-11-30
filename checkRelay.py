#!/usr/bin/python

#Program namenjen preklopu releja iz zaprtega v odprto stanje, če je le ta predolgo zaprt
#Uporabljen kot rešitev problema #1 (glej BUGS.md)

import RPi.GPIO as GPIO #import the GPIO library
import time
import datetime
from datetime import datetime
import os
import logging
logging.basicConfig(filename='checkRelay.log')

homeFolder=os.environ['HOME']
path=homeFolder+'/.garage/logs'
file=homeFolder+'/.garage/logs/checkRelay.log'

def checkLogFilePath():
    if(not os.path.exists(homeFolder+'/.garage')):
        os.mkdir(homeFolder+'/.garage')
    if(not os.path.exists(path)):
        os.mkdir(path)

def writeLog(task):
    time=datetime.now()
    with open(file, 'a+') as log:
        log.write('[' + str(time) +']' + ' => ' + task + '\n')

logger=logging.getLogger(__name__)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
GPIO.output(12, GPIO.HIGH)

while True:
    if GPIO.input(12) == False:
        time.sleep(1.5)
        if GPIO.input(12) == False:
            #writeLog('Relay closed for too long.')
            logger.warning('Relay closed for too long.')
            GPIO.output(12, not GPIO.input(12))
            #writeLog('Relay opened automatically.')
            logger.info('Relay opened automatically.')
    time.sleep(.5)
GPIO.cleanup()
