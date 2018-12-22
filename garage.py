#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import argparse
import os
import time
import glob
from RPLCD.gpio import CharLCD
from multiprocessing import Process

TRIG = 11
ECHO = 20
RELAY = 16
OVERRIDE_CAR = 26
OVERRIDE_TEMP = 12
LED_MONITOR_CAR = 13
LED_MONITOR_TEMP = 21
REED_OPEN = 5
REED_CLOSED = 6

car_status_changed_wait = 30


def lcd_write(line1, line2):
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string(line1)
    lcd.cursor_pos = (1, 0)
    lcd.write_string(line2)

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
        return temp_c

def blink(LED):
    GPIO.output(LED, GPIO.HIGH)  # led on
    time.sleep(.5)
    GPIO.output(LED, GPIO.LOW) # led off
    time.sleep(.5)

def toggleGarage():
    GPIO.output(RELAY, 0)
    time.sleep(.5)
    GPIO.output(RELAY, 1)

def checkDoor():
    if GPIO.input(REED_OPEN) == True:
        return "odprta"
    elif GPIO.input(REED_CLOSED) == True:
        return "zaprta"
    else:
        return "priprta"

def checkCar():
    GPIO.output(TRIG, False)
    time.sleep(0.001)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO)==0:
      pulse_start = time.time()

    while GPIO.input(ECHO)==1:
      pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150

    return round(distance, 2)

def monitorCar():
    GPIO.add_event_detect(OVERRIDE_CAR,GPIO.RISING,bouncetime=300)
    distance = checkCar()
    for x in range(0,20):
        if GPIO.event_detected(OVERRIDE_CAR):
            lcd_write("Preklic cakanja","na avto!")
            time.sleep(2)
            lcd_write("Garaza","ostaja " + checkDoor() + "!")
            time.sleep(2)
            break
        if x % 5 == 0:
            if distance <= 20:
                lcd_write("Cakam ali bo","avto odpeljal...")
            else:
                lcd_write("Cakam ali bo","avto prakiral...")
        blink(LED_MONITOR_CAR)
        if (distance >=25 and checkCar() <= 20) or (distance <=20 and checkCar() >= 25):
            time.sleep(5)
            if distance >=25 and checkCar() <= 20:
                lcd.clear()
                lcd_write("Avto parkiran.","Zapiram garazo!")
                toggleGarage()
                time.sleep(2)
                break
            elif distance <=20 and checkCar() >= 25:
                lcd.clear()
                lcd_write("Avto odpeljal!", "Zapiram garazo!")
                toggleGarage()
                time.sleep(2)
                break
    #if checkCar() <= 20:
    #    lcd_write("Avto ni odpeljal...","Garaza " + checkDoor() + ".")
    #    time.sleep(5)
    #else:
    #    lcd_write("Avto ni parkiral...","Garaza " + checkDoor() + ".")
    #    time.sleep(5)

def monitorTemp():
    time.sleep(5)
    GPIO.add_event_detect(OVERRIDE_TEMP,GPIO.RISING,bouncetime=300)
    while 1:
        if GPIO.event_detected(OVERRIDE_TEMP):
            lcd_write("Preklic cakanja","neustrezne temp!")
            time.sleep(2)
            lcd_write("Garaza","ostaja " + checkDoor() + "!")
            time.sleep(2)
            break
        blink(LED_MONITOR_TEMP  )
        temp = read_temp()
        lcd_write("Trenutna temp.:",str(temp)+unichr(223)+"C")
        if temp < 17:
            lcd_write("Garaza prehladna!","Zapiram garazo!")
            toggleGarage()
            while checkDoor() != "zaprta":
                time.sleep(1)
            lcd_write("Garaza zaprta!",'')
            time.sleep(2)
            break;
        elif temp > 25:
            lcd_write("Garaza pretopla!","Zapiram garazo!")
            toggleGarage()
            while checkDoor() != "zaprta":
                time.sleep(1)
            lcd_write("Garaza zaprta!",'')
            time.sleep(2)
            break;

def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--toggle", action="store_true", help="Trigger garage doors relay.")
    parser.add_argument('-C', '--car-status', action="store_true", help="Check wether or not the car is in the garage.")
    parser.add_argument('-S', '--door-status', action="store_true", help="Preveri v kaksnem stanju so vrata.")
    args = parser.parse_args()

    if args.toggle == True:
        if checkDoor() == 'zaprta':
            lcd_write("Odpiram garazo!",'')
            toggleGarage()
            for x in range(0,60):
                if checkDoor() == 'odprta':
                    break;
                elif x == 60:
                    exit(0)
                time.sleep(1)
            try:
                c = Process(target=monitorCar,args=())
                c.start()
                t = Process(target=monitorTemp,args=())
                t.start()
                t.join()
                destroy()
                #thread.start_new_thread( monitorTemp,("thread_check_temp", 1,))
            except:
                print "Couldn't start thread"
                destroy()
        elif checkDoor() == 'odprta':
            lcd_write("Zapiram garazo!",'')
            toggleGarage()
            time.sleep(2)
            lcd.clear()
            destroy()
        else:
            lcd_write("Garaza priprta!","Premikam vrata!")
            toggleGarage()
            time.sleep(2)
            lcd.clear()
            destroy()

    elif args.car_status == True:
        if checkCar() < 15:
            print "Avto je v garaži!"
        else:
            print "Avto ni v garaži!"
    elif args.door_status == True:
        lcd_write("Garaza " + checkDoor() + "." ,'')
        time.sleep(2)
        lcd.clear()
        destroy()

def destroy():
    lcd_write("Ojla! Sem Elza,","pametna garaza!")
    GPIO.output(LED_MONITOR_CAR, GPIO.LOW)   # led off
    GPIO.output(LED_MONITOR_TEMP, GPIO.LOW)   # led off
    GPIO.cleanup()

def setup():
    global lcd,base_dir,device_folder,device_file
    #GPIO setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(OVERRIDE_CAR,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(OVERRIDE_TEMP,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(LED_MONITOR_CAR, GPIO.OUT)   # Set LedPin's mode is output
    GPIO.setup(LED_MONITOR_TEMP, GPIO.OUT)   # Set LedPin's mode is output
    GPIO.setup(RELAY, GPIO.OUT)
    GPIO.setup(REED_OPEN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(REED_CLOSED, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    #LCD setup
    lcd = CharLCD(cols=16, rows=2, pin_rs=25, pin_e=24, pins_data=[23,17,18,22],numbering_mode=GPIO.BCM)
    #temp sensor setup
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'
    lcd_write("Ojla! Sem Elza,","pametna garaza!")

if __name__=="__main__":
    try:
        setup()
        arguments()
    except KeyboardInterrupt:
        destroy()
