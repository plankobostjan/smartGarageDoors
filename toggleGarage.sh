#!/usr/bin/env bash

gpio toogle 1
sleep .6
gpio toggle 1
printf "Script ran on $(date +'%a %d %b %Y at %T') by $1.\n" >> $HOME/.garage/toggleGarage.log
