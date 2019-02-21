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

#fileConfig('logging_config.ini')
#logger = logging.getLogger()

GPIO.setwarnings(False)

homeFolder=os.environ['HOME'] #pridobim domačo mapo uporabnika, ki je pognal program
logPath=homeFolder+'/.garage/logs' #nastavim mapo v katero se bo shranjevala dnevniška datoteka
logFile=homeFolder+'/.garage/logs/toggleRelay.log'

def checkLogFilePath(): #metoda, ki preveri ali obstajajo vse ptrebne mape in jih po potrebi ustvari
    if(not os.path.exists(homeFolder+'/.garage')):
        os.mkdir(homeFolder+'/.garage')
    if(not os.path.exists(logPath)):
        os.mkdir(logPath)

def readConf(section, vars, val_dict):
    configParser = ConfigParser.RawConfigParser(allow_no_value=True)
    configParser.read(os.environ['HOME']+'/.garage/garage.conf')
    for value in vars:
        val_dict[value] = int(configParser.get(section, value))

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
        temp_c = int(temp_string) / 1000.0 # TEMP_STRING IS THE SENSOR OUTPUT, MAKE SURE IT'S AN INTEGER TO DO THE MATH
        temp_c = round(temp_c, 1) # ROUND THE RESULT TO 1 PLACE AFTER THE DECIMAL
        return temp_c

def blink(LED):
    GPIO.output(LED, GPIO.HIGH)  # led on
    time.sleep(.5)
    GPIO.output(LED, GPIO.LOW) # led off
    time.sleep(.5)

def toggleGarage():
    GPIO.output(GPIO_VARS_DICT['RELAY'], 0)
    time.sleep(.5)
    GPIO.output(GPIO_VARS_DICT['RELAY'], 1)

def checkDoor():
    if GPIO.input(GPIO_VARS_DICT['REED_OPEN']) == True:
        return "odprta"
    elif GPIO.input(GPIO_VARS_DICT['REED_CLOSED']) == True:
        return "zaprta"
    else:
        return "priprta"

def checkCar():
    GPIO.output(GPIO_VARS_DICT['TRIG'], False)
    time.sleep(0.001)

    GPIO.output(GPIO_VARS_DICT['TRIG'], True)
    time.sleep(0.00001)
    GPIO.output(GPIO_VARS_DICT['TRIG'], False)

    while GPIO.input(GPIO_VARS_DICT['ECHO'])==0:
      pulse_start = time.time()

    while GPIO.input(GPIO_VARS_DICT['ECHO'])==1:
      pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150

    return round(distance, 2)

def monitorCar():
    GPIO.add_event_detect(GPIO_VARS_DICT['OVERRIDE_CAR'],GPIO.RISING,bouncetime=300)
    distance = checkCar()
    for x in range(0,TIMEOUTS_VARS_DICT['CAR_STATUS_TIMEOUT']):
        if GPIO.event_detected(GPIO_VARS_DICT['OVERRIDE_CAR']):
            break
        elif checkDoor() == 'zaprta':
            break
        blink(GPIO_VARS_DICT['LED_MONITOR_CAR'])
        if (distance >=25 and checkCar() <= 20) or (distance <=20 and checkCar() >= 25):
            for i in range(0,5):
                blink(GPIO_VARS_DICT['LED_MONITOR_CAR'])
            if GPIO.event_detected(GPIO_VARS_DICT['OVERRIDE_CAR']):
                break
            elif checkDoor() != 'odprta':
                break
            if distance >=25 and checkCar() <= 20:
                toggleGarage()
                while checkDoor() != "zaprta":
                    time.sleep(5)
                time.sleep(2)
                break
            elif distance <=20 and checkCar() >= 25:
                toggleGarage()
                pushover.send_message("Avto odpeljal! Zapiram garažo!", title="Garaža")
                while checkDoor() != "zaprta":
                    time.sleep(5)
                    pushover.send_message("Avto odpeljal! Garaža zaprta!", title="Garaža")
                time.sleep(2)
                break

def monitorTemp():
    time.sleep(TIMEOUTS_VARS_DICT['BEGIN_TEMP_WATCH'])
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


def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--toggle", action="store_true", help="Trigger garage doors relay.")
    parser.add_argument('-C', '--car-status', action="store_true", help="Check wether or not the car is in the garage.")
    parser.add_argument('-S', '--door-status', action="store_true", help="Preveri v kaksnem stanju so vrata.")
    args = parser.parse_args()

    if args.toggle == True:
        logging.info("Toggle garage activated.")
        if checkDoor() == 'zaprta':
            logging.info("Garage closed.")
            toggleGarage()
            logging.info("Opening garage...")
            logging.info("Waiting for garage to open.")
            for x in range(0,60):
                if checkDoor() == 'odprta':
                    logging.info("Garage opened.")
                    logging.debug("Sending push notifiaction over Pushover...")
                    pushover.send_message("Garaža odprta!", title="Garaža")
                    logging.debug("Pushover notification send.")
                    break;
                elif x == 60:
                    logging.warning("Couldn't open garage.")
                    time.sleep(1)
                time.sleep(1)
            try:
                logging.debug("Starting car starus monitoring...")
                c = Process(target=monitorCar,args=())
                c.start()
                logging.debug("Car monitoring running.")
                logging.debug("Starting temperature monitoring...")
                t = Process(target=monitorTemp,args=())
                t.start()
                logging.debug("Temperature monitoring running.")
                c.join()
                t.join()
                logging.debug("Waiting for doors to close...")
                while checkDoor() != 'zaprta':
                    time.sleep(1)
                logging.info("Doors closed.")
                logging.debug("Sending Pushover notification...")
                pushover.send_message('Garaža zaprta!',title="Garaža")
                logging.debug("Pushover notification sent.")
            except:
                print "Couldn't start thread"
        elif checkDoor() == 'odprta':
            logging.debug("Garage is open.")
            cd = Process(target=closeDoor(),args=())
            cd.start()
            cd.join(60)
        else:
            print 'doors ajar'
            doorAjar()

    elif args.car_status == True:
        if checkCar() < 15:
            print "Avto je v garaži!"
        else:
            print "Avta ni v garaži!"
    elif args.door_status == True:
        lcd.clear()
    else:
        print 'nic'
        destroy()

def closeDoor():
    toggleGarage()
    pushover.send_message("Zapiram garažo!", title="Garaža")
    for x in range(0, TIMEOUTS_VARS_DICT['AJAR_TIMEOUT']):
        if checkDoor() == 'zaprta':
            pushover.send_message("Garaža zaprta!", title="Garaža")
            time.sleep(2)
        time.sleep(1)

def doorAjar():
    for attempts in range(0, TIMEOUTS_VARS_DICT['AJAR_CLOSE_ATTEMPTS']):
        toggleGarage()
        for x in range(0, TIMEOUTS_VARS_DICT['AJAR_TIMEOUT']):
            if checkDoor() != 'priprta':
                break
            time.sleep(1)
        if checkDoor() == 'zaprta':
            break
        elif checkDoor() == 'odprta':
            closeDoor()

def destroy():
    GPIO.output(GPIO_VARS_DICT['LED_MONITOR_CAR'], GPIO.LOW)   # led off
    GPIO.output(GPIO_VARS_DICT['LED_MONITOR_TEMP'], GPIO.LOW)   # led off
    GPIO.cleanup()

def setup():
    #variables setup
    global lcd,base_dir,device_folder,device_file
    #read from config
    logging.debug("Setting variables for reading from config file...")
    GPIO_VARS = ['TRIG','ECHO','RELAY','OVERRIDE_CAR','OVERRIDE_TEMP','LED_MONITOR_CAR','LED_MONITOR_TEMP','REED_OPEN','REED_CLOSED']
    TEMP_VARS = ['MAX_TEMP','MIN_TEMP']
    TIMEOUTS_VARS = ['AJAR_TIMEOUT','CAR_STATUS_TIMEOUT','BEGIN_TEMP_WATCH','AJAR_CLOSE_ATTEMPTS']
    LCD_VARS = ['cols','rows','pin_rs','pin_e','d4','d5','d6','d7']
    global GPIO_VARS_DICT, TEMP_VARS_DICT, TIMEOUTS_VARS_DICT, LCD_VARS_DICT
    TEMP_VARS_DICT = dict()
    TIMEOUTS_VARS_DICT = dict()
    GPIO_VARS_DICT = dict()
    LCD_VARS_DICT = dict()
    logging.debug("Variables for reading from config file set.")
    logging.debug("Reading GPIO configuration..."")
    readConf('gpio',GPIO_VARS,GPIO_VARS_DICT)
    logging.debug("Finished reading GPIO configuration")
    logging.debug("Reading temperature configuration..."")
    readConf('temperature',TEMP_VARS,TEMP_VARS_DICT)
    logging.debug("Finished reading temperature configuration")
    logging.debug("Reading timeouts configuration..."")
    readConf('timeouts',TIMEOUTS_VARS,TIMEOUTS_VARS_DICT)
    logging.debug("Finished reading timeouts configuration")
    logging.debug("Reading LCD configuration..."")
    readConf('lcd',LCD_VARS,LCD_VARS_DICT)
    logging.debug("Finished reading LCD configuration")
    #GPIO setup
    logging.debug("Setting up GPIO...")
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
    GPIO.setwarnings(False)
    logging.debug("GPIO setup finished.")
    #LCD setup
    logging.debug("Setting up LCD...")
    lcd = CharLCD(cols=LCD_VARS_DICT['cols'], rows=LCD_VARS_DICT['rows'], pin_rs=LCD_VARS_DICT['pin_rs'], pin_e=LCD_VARS_DICT['pin_e'], pins_data=[LCD_VARS_DICT['d4'],LCD_VARS_DICT['d5'],LCD_VARS_DICT['d6'],LCD_VARS_DICT['d7']],numbering_mode=GPIO.BCM)
    logging.debug("LCD setup finished.")
    #temp sensor setup
    logging.debug("Setting up temperature sensor...")
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'
    logging.debug("Temperature sensor setup finished.")
    #pushover setup
    logging.debug("Setting up Pushover...")
    configParser = ConfigParser.RawConfigParser(allow_no_value=True)
    configParser.read(os.environ['HOME']+'/.garage/garage.conf')
    global pushover
    pushover = Client(configParser.get('pushover', 'user_key'), api_token=configParser.get('pushover', 'api_token'))
    logging.debug("Pushover sertup finished.")

if __name__=="__main__":
    try:
        logging.debug("Checking if /tmp/LCD_temp.pid exists...")
        if os.path.isfile("/tmp/LCD_temp.pid"):
            logging.debug("/tmp/LCD_temp.pid exists.")
            logging.debug("Killing LCD_temperature.py...")
            os.system("kill $(cat /tmp/LCD_temp.pid)")
            logging.debug("LCD_temperature.py killed.")
            logging.debug("Removing /tmp/LCD_temp.pid...")
            os.unlink("/tmp/LCD_temp.pid")
            logging.debug("/tmp/LCD_temp.pid removed.")
        #m = Process(target=mainScreen,args=())
        setup()
        lcd.clear()
        #m.start()
        logging.debug("Starting temperature_LCD.py...")
        os.system('python temperature_LCD.py &')
        logging.debug("LCD_temperature running.")
        arguments()
        #m.join()
    except KeyboardInterrupt:
        destroy()
    finally:
        destroy()
        if os.path.isfile("/tmp/LCD_temp.pid"):
            os.system("kill $(cat /tmp/LCD_temp.pid)")
            os.unlink("/tmp/LCD_temp.pid")
        os.system('python temperature_LCD.py &')
#os.system('python temperature_LCD.py &')
