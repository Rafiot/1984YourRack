#!/usr/bin/env bash

cat /boot/config.txt |grep start_x=1  > /dev/null; check_cam_enable=$?
which pip3 > /dev/null ; check_pip3=$?

rpiFW=$(/opt/vc/bin/vcgencmd version |grep version |cut -f2 -d\ )
machineArch=$(uname -m)

if [ "$machineArch" == "armv7l" ]; then
	echo "armv7l detected"
	sudo apt install -y libopenjp2-7-dev libtiff5-dev libatlas-base-dev
fi

if [ "$check_pip3" != "0" ]; then
    sudo apt install -y python3-pip tmux
fi

which virtualenv > /dev/null ; check_venv=$?

if [ "$check_venv" != "0" ]; then
    echo "Installing virtualenv module"
    sudo apt install -y virtualenv
else
    echo "virtualenv module installed"
fi

if [ -d myPiMotion ]; then
    echo "We have a virtualenv, updating dependencies"
    . myPiMotion/bin/activate
    pip install -U picamera pillow numpy
else
    echo "Creating venv"
    virtualenv -p python3 myPiMotion
    . myPiMotion/bin/activate
    pip install picamera pillow numpy
fi


if [ "$check_cam_enable" != "0" ]; then
    read -p 'Enable camera, maybe ssh, fix locale and update the firmware, hit enter to continue.'
    sudo raspi-config
fi
sudo JUST_CHECK=1 rpi-update ; check_rpiFW=$?
if [ "$check_rpiFW" != "0" ]; then
    sudo rpi-update
else
    echo "Your firmware is up-to-date, hash: ${rpiFW}"
fi
