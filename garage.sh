#!/bin/bash

#BASH skripta, ki jo trenutno uporabljam za odpiranje/zapiranje garažnih vrat preko svojega telefona
#Potrebne izboljšave (glej bugs.md)

if ping -c 1 192.168.0.9 &> /dev/null
then
    termux-tts-speak 'Garage doors moving...'&
    sleep .5
    termux-notification --title Garage --content 'Opening/closing garage.' --sound
    termux-toast 'Opening/closing garage!'
    sshpass -p "passwd" ssh pi@192.168.0.9 'gpio toggle 1; sleep .6; gpio toggle 1;'
else
    termux-tts-speak 'Garage computer not available.'
    termux-notification --title Garage --content 'Garage computer not available.'
    termux-toast 'Garage computer not available!'
fi