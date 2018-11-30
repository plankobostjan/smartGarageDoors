#!/usr/bin/env bash

checkDirs{
if [ ! -d "$HOME/.garage"]
then
  mkdir "$HOME/.garage"
fi
if [ ! -d "$HOME/.garage/logs"]
then
  mkdir "$HOME/.garage/logs"
fi
}

moveFiles{
  cp autoClose.py .toggleGarage.py checkRelay.py checkDoor.py "$HOME/.garage"
}
