#!/usr/bin/python

#nadomestil toggleGarage.sh

import RPi.GPIO as GPIO #import the GPIO library
import time
from datetime import datetime
import os
import sys
import logging
logging.basicConfig(filename='toggleGarage.log') #določim datoteko v katero se bo shranjeval dnevnik dogodkov

homeFolder=os.environ['HOME'] #pridobim domačo mapo uporabnika, ki je pognal program
logPath=homeFolder+'/.garage/logs' #nastavim mapo v katero se bo shranjevala dnevniška datoteka
logFile=homeFolder+'/.garage/logs/toggleRelay.log'

def checkLogFilePath(): #metoda, ki preveri ali obstajajo vse ptrebne mape in jih po potrebi ustvari
    if(not os.path.exists(homeFolder+'/.garage')):
        os.mkdir(homeFolder+'/.garage')
    if(not os.path.exists(logPath)):
        os.mkdir(logPath)


GPIO.setmode(GPIO.BOARD) #nastavi način številčenja GPIO pinov
GPIO.setup(12, GPIO.OUT) #nastavi pin 12 kot izhodnega
GPIO.output(12, 0) #zapre rele
time.sleep(.5) #počaka 0.5 sekunde
GPIO.output(12, 1) #odpre rele

GPIO.cleanup() #počisti GPIO nastavitve
