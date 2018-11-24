#!/usr/bin/python

#isto kot toggleGarage.sh, vendar napisano v Pythonu
#v prihodnosti bo verjetno povsem nadmostil toggleGarage.sh

import RPi.GPIO as GPIO #import the GPIO library
import time
import datetime
from datetime import datetime
import os

path='/home/pi/.garage/logs'
file='/home/pi/.garage/logs/checkRelay.log'

def checkLogFilePath():
    if(not os.path.exists('/home/pi/.garage')):
        os.mkdir('/home/pi/.garage')
    if(not os.path.exists(path)):
        os.mkdir(path)

def writeLog(task):
    time=datetime.now()
    with open(file, 'a+') as log:
        log.write('[' + str(time) +']' + ' => ' + task + '\n')
checkLogFilePath)()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
GPIO.output(12, 0)
time.sleep(.5)
GPIO.output(12, 1)
writeLog('Garage doors activated.')
GPIO.cleanup()
