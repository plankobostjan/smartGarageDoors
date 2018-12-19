#!/usr/bin/python
import RPi.GPIO as GPIO
import time
from subprocess import call
GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24
OVERRIDE = 22

#print "Distance Measurement In Progress"

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(OVERRIDE,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

GPIO.output(TRIG, False)
#print "Waiting For Sensor To Settle"
time.sleep(2)

GPIO.output(TRIG, True)
time.sleep(0.00001)
GPIO.output(TRIG, False)

while GPIO.input(ECHO)==0:
  pulse_start = time.time()

while GPIO.input(ECHO)==1:
  pulse_end = time.time()

pulse_duration = pulse_end - pulse_start

distance = pulse_duration * 17150

distance = round(distance, 2)

print distance
print GPIO.input(OVERRIDE)

if distance < 10 and not GPIO.input(OVERRIDE):
  time.sleep(5)
  call(["/home/pi/.garage/toggleGarage.py"])

GPIO.cleanup()
