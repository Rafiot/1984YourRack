#!/usr/bin/env bash

cat /boot/config.txt |grep start_x=1  > /dev/null; check_cam_enable=$?
which pip3 > /dev/null ; check_pip3=$?

rpiFW=$(/opt/vc/bin/vcgencmd version |grep version |cut -f2 -d\ )

if [ "$check_pip3" != "0" ]; then
    sudo apt install python3-pip tmux
fi

echo "Running pip3 freeze, this might take some time." ; pip3 freeze |grep virtualenv  > /dev/null; check_venv=$?
echo "Done freezing"

if [ "$check_venv" != "0" ]; then
    echo "Installing virtualenv module"
    pip3 install -U virtualenv
else
    echo "virtualenv module installed"
fi

if [ -d myPiMotion ]; then
    echo "We have a virtualenv, updating dependencies"
    . myPiMotion/bin/activate
    pip install -U picamera pillow
else
    echo "Creating venv"
    virtualenv myPiMotion
    . myPiMotion/bin/activate
    pip install picamera pillow
fi


if [ "$check_cam_enable" != "0" ]; then
    read -p 'Enable camera and update the firmware, hit enter to continue.'
    sudo raspi-config
fi
sudo JUST_CHECK=1 rpi-update ; check_rpiFW=$?
if [ "$check_rpiFW" != "0" ]; then
    sudo rpi-update
else
    echo "Your firmware is up-to-date, hash: ${rpiFW}"
fi
