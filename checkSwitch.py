#!/usr/bin/python
import RPi.GPIO as GPIO
import time
from subprocess import call
GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24
OVERRIDE = 22

#print "Distance Measurement In Progress"

GPIO.setup(OVERRIDE,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
count = 0

while count < 10:
  print GPIO.input(OVERRIDE)
  time.sleep(1)
  count+=1

GPIO.cleanup()
