#!/usr/bin/python
import RPi.GPIO as GPIO
import time
from subprocess import call
GPIO.setmode(GPIO.BCM)

def init():
    #variables setup
    global base_dir,device_folder,device_file
    #read from config
    GPIO_VARS = ['TRIG','ECHO','RELAY','OVERRIDE_CAR','OVERRIDE_TEMP','LED_MONITOR_CAR','LED_MONITOR_TEMP','REED_OPEN','REED_CLOSED']
    TIMEOUTS_VARS = ['AJAR_TIMEOUT','CAR_STATUS_TIMEOUT','BEGIN_TEMP_WATCH','AJAR_CLOSE_ATTEMPTS']
    global GPIO_VARS_DICT, TIMEOUTS_VARS_DICT
    TIMEOUTS_VARS_DICT = dict()
    GPIO_VARS_DICT = dict()
    readConf('gpio',GPIO_VARS,GPIO_VARS_DICT)
    readConf('timeouts',TIMEOUTS_VARS,TIMEOUTS_VARS_DICT)
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
    #pushover setup
    global pushover
    pushover = Client(configParser.get('pushover', 'user_key'), api_token=configParser.get('pushover', 'api_token'))

if __name__=="__main__":

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

#print "Distance Measurement In Progress"

GPIO.setup(OVERRIDE,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
count = 0

if __name__ == __main__:
  if checkCar() < 20:
    return 1
  else:
    return 0
