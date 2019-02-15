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
from pushover import Client
import ConfigParser
import io
import logging
from logging.config import fileConfig

def readConf(section, vars, val_dict):
    configParser = ConfigParser.RawConfigParser(allow_no_value=True)
    configParser.read(os.environ['HOME']+'/.garage/garage.conf')
    for value in vars:
        val_dict[value] = int(configParser.get(section, value))

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
        temp_c = int(temp_string) / 1000.0 # TEMP_STRING IS THE SENSOR OUTPUT, MAKE SURE IT'S AN INTEGER TO DO THE MATH
        temp_c = round(temp_c, 1) # ROUND THE RESULT TO 1 PLACE AFTER THE DECIMAL
        return temp_c

def blink(LED):
    GPIO.output(LED, GPIO.HIGH)  # led on
    time.sleep(.5)
    GPIO.output(LED, GPIO.LOW) # led off
    time.sleep(.5)

def checkDoor():
    if GPIO.input(GPIO_VARS_DICT['REED_OPEN']) == True:
        return "odprta"
    elif GPIO.input(GPIO_VARS_DICT['REED_CLOSED']) == True:
        return "zaprta"
    else:
        return "priprta"

def toggleGarage():
    GPIO.output(GPIO_VARS_DICT['RELAY'], 0)
    time.sleep(.5)
    GPIO.output(GPIO_VARS_DICT['RELAY'], 1)

def monitorTemp():
    time.sleep(int(TIMEOUTS_VARS_DICT['BEGIN_TEMP_WATCH']))
    GPIO.add_event_detect(GPIO_VARS_DICT['OVERRIDE_TEMP'],GPIO.RISING,bouncetime=300)
    count = 0
    while 1:
        blink(GPIO_VARS_DICT['LED_MONITOR_TEMP'])
        if GPIO.event_detected(GPIO_VARS_DICT['OVERRIDE_TEMP']):
            break
        elif checkDoor() == 'zaprta':
            break
        temp = read_temp()
        if temp < TEMP_VARS_DICT['MIN_TEMP']:
            toggleGarage()
            pushover.send_message("Temperatura v garaži prenizka! Zapiram garažo!", title="Garaža prehladna!")
            while checkDoor() != "zaprta":
                time.sleep(1)
            pushover.send_message("Garaža zaprta zaradi prenizke temperature!", title="Garaža zarta!")
            time.sleep(2)
            break;
        elif temp > TEMP_VARS_DICT['MAX_TEMP']:
            toggleGarage()
            pushover.send_message("Temperatura v garaži previsoka! Zapiram garažo!", title="Garaža pretopla!")
            while checkDoor() != "zaprta":
                time.sleep(1)
            pushover.send_message("Garaža zaprta zaradi previsoke temperature!", title="Garaža zarta!")
            time.sleep(2)
            break;
        count += 1

def init():
    #variables setup
    global lcd,base_dir,device_folder,device_file
    #read from config
    GPIO_VARS = ['TRIG','ECHO','RELAY','OVERRIDE_CAR','OVERRIDE_TEMP','LED_MONITOR_CAR','LED_MONITOR_TEMP','REED_OPEN','REED_CLOSED']
    TEMP_VARS = ['MAX_TEMP','MIN_TEMP']
    TIMEOUTS_VARS = ['AJAR_TIMEOUT','CAR_STATUS_TIMEOUT','BEGIN_TEMP_WATCH','AJAR_CLOSE_ATTEMPTS']
    LCD_VARS = ['cols','rows','pin_rs','pin_e','d4','d5','d6','d7']
    global GPIO_VARS_DICT, TEMP_VARS_DICT, TIMEOUTS_VARS_DICT, LCD_VARS_DICT
    TEMP_VARS_DICT = dict()
    TIMEOUTS_VARS_DICT = dict()
    GPIO_VARS_DICT = dict()
    LCD_VARS_DICT = dict()
    readConf('gpio',GPIO_VARS,GPIO_VARS_DICT)
    readConf('temperature',TEMP_VARS,TEMP_VARS_DICT)
    readConf('timeouts',TIMEOUTS_VARS,TIMEOUTS_VARS_DICT)
    readConf('lcd',LCD_VARS,LCD_VARS_DICT)
    #GPIO setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_VARS_DICT['TRIG'],GPIO.OUT)
    GPIO.setup(GPIO_VARS_DICT['ECHO'],GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(GPIO_VARS_DICT['OVERRIDE_CAR'],GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(GPIO_VARS_DICT['OVERRIDE_TEMP'],GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(GPIO_VARS_DICT['LED_MONITOR_CAR'], GPIO.OUT)   # Set LedPin's mode is output
    GPIO.setup(GPIO_VARS_DICT['LED_MONITOR_TEMP'], GPIO.OUT)   # Set LedPin's mode is output
    GPIO.setup(GPIO_VARS_DICT['RELAY'], GPIO.OUT)
    GPIO.setup(GPIO_VARS_DICT['REED_OPEN'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(GPIO_VARS_DICT['REED_CLOSED'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    #LCD setup
    lcd = CharLCD(cols=LCD_VARS_DICT['cols'], rows=LCD_VARS_DICT['rows'], pin_rs=LCD_VARS_DICT['pin_rs'], pin_e=LCD_VARS_DICT['pin_e'], pins_data=[LCD_VARS_DICT['d4'],LCD_VARS_DICT['d5'],LCD_VARS_DICT['d6'],LCD_VARS_DICT['d7']],numbering_mode=GPIO.BCM)
    #temp sensor setup
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'
    #pushover setup
    configParser = ConfigParser.RawConfigParser(allow_no_value=True)
    configParser.read(os.environ['HOME']+'/.garage/garage.conf')
    global pushover
    pushover = Client(configParser.get('pushover', 'user_key'), api_token=configParser.get('pushover', 'api_token'))

def destroy():
    GPIO.output(GPIO_VARS_DICT['LED_MONITOR_TEMP'], GPIO.LOW)   # led off
    GPIO.cleanup()

if __name__=="__main__":
    try:
        init()
        monitorTemp()
        destroy()
    except KeyboardInterrupt:
        destroy()
