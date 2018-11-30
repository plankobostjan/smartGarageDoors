#!/usr/bin/env bash

check_dirs{
if [ ! -d "$HOME/.garage" ]
then
  mkdir "$HOME/.garage"
fi
if [ ! -d "$HOME/.garage/logs" ]
then
  mkdir "$HOME/.garage/logs"
fi
}

move_files{
  cp autoClose.py toggleGarage.py checkRelay.py checkDoor.py "$HOME/.garage"
}

check_dirs
move_files
