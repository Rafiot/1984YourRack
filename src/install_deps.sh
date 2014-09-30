#!/usr/bin/bash

sudo apt-get install tmux

read -p 'Enable camera and update the firmware, hit enter to continue.'

sudo raspi-config

sudo rpi-update


