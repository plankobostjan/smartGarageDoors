#!/usr/bin/python

#Program, ki trenutno še ni v uporabi.
#Sicer namenjen samodejnemu zapiranju garažnih vrat.
#Se zna v nadaljevanju zelo spremeniti.

import RPi.GPIO as GPIO #import the GPIO library
import time
import os

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)

name = "Bostjan"
print("Hello " + name + "!")

if GPIO.input(11) == False: #če se vrata odprta, jih zapri
    print("Door is open. Closing...")
    os.system('gpio toggle 1; sleep .60; gpio toggle 1')
elif GPIO.input(13) == False: #če so vrata zaprta ne naredi ničesar
    print("Door is closed.")
else:
    print("Door is ajar. Toggling.") #če so vrata priprta
    os.system('gpio toggle 1; sleep .60; gpio toggle 1') #sproži rele, da se začnejo premikati,
    time.sleep(5) #nato čakaj
    if GPIO.input(11) == False: #če so vrata odprta
        print("Door is open. Closing...")
        os.system('gpio toggle 1; sleep .60; gpio toggle 1') #jih zapri
