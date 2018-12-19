#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import argparse
GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24
RELAY = 18
OVERRIDE = 22
LED = 17

car_status_changed_wait = 300

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

def blink(LED, time):
    distance = checkCar()
    count = 0
    GPIO.output(LED, GPIO.HIGH) # Set LedPin high(+3.3V) to turn on led
    for count in range(0, time):
        GPIO.output(LED, GPIO.HIGH)  # led on
        time.sleep(1)
        GPIO.output(LED, GPIO.LOW) # led off
        time.sleep(1)
        if count % 10 == 0:
            if checkCar() > (distance + 1) or checkCar() > (distance + 1):
                toggleGarage()
                GPIO.output(LED, GPIO.LOW)   # led off
                GPIO.cleanup()
                break
    GPIO.output(LED, GPIO.LOW)   # led off
    GPIO.cleanup()

def toggleGarage():
    GPIO.output(RELAY, 0)
    time.sleep(.5)
    GPIO.output(RELAY, 1)
    GPIO.cleanup()

    if checkCar() < 15:
        print "Avto je v garaži!"
        print "Čakam, če bo avto zapustil garažo!"
        blink(17, 60)
    else:
        print "Avta ni v garaži!"
        print "Čakam, če bo avto prišel v garažo!"
        blink(17, 60)

def checkCar():
    GPIO.output(TRIG, False)
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

    destroy()
    return round(distance, 2)

def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--toggle", action="store_true", help="Trigger garage doors relay.")
    parser.add_argument('-C', '--car-status', action="store_true", help="Check wether or not the car is in the garage.")
    args = parser.parse_args()

    if args.toggle == True:
        toggleGarage()
    elif args.car_status == True:
        if checkCar() < 15:
            print "Avto je v garaži!"
        else:
            print "Avto ni v garaži!"

def destroy():
    GPIO.output(LED, GPIO.LOW)   # led off
    GPIO.output(RELAY,GPIO.LOW)
    GPIO.cleanup()

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(OVERRIDE,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(LED, GPIO.OUT)   # Set LedPin's mode is output
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RELAY, GPIO.OUT)

if __name__=="__main__":
    try:
        arguments()
    except KeyboardInterrupt:
        destroy()
