#!/usr/bin/python

#nadomestil toggleGarage.sh

import RPi.GPIO as GPIO #import the GPIO library
import time
from datetime import datetime
import os

homeFolder=os.environ['HOME']
logPath=homeFolder+'/.garage/logs'
logFile=homeFolder+'/.garage/logs/toggleRelay.log'

def checkLogFilePath():
    if(not os.path.exists(homeFolder+'/.garage')):
        os.mkdir(homeFolder+'/.garage')
    if(not os.path.exists(logPath)):
        os.mkdir(logPath)

def writeLog(task):
    time=datetime.now()
    with open(logFile, 'a+') as log:
        log.write('[' + str(time) +']' + ' => ' + task + '\n')

checkLogFilePath()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
GPIO.output(12, 0)
time.sleep(.5)
GPIO.output(12, 1)
writeLog('Garage doors activated by ' + str(sys.argv[1]) + '.')
GPIO.cleanup()
