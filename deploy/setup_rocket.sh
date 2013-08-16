#!/bin/sh

#
# This script makes sure that all dependencies for the ci dashboard rocket
# launcher are installed. If there is an error during setup, please try to do
# these steps manually and report the issue.
#
# Requirements:
# - sudo with all rights
# - python 2.7
# - pip (python-pib)
# - libusb installed via pip
#

echo "Installing USB launcher udev rules, to allow access by users in group 'games'."

#
# udev rules setup, inspired by https://github.com/joergschiller/stormLauncher
#

if [ -f /etc/udev/rules.d/80-launcher.rules ]; then
  sudo rm /etc/udev/rules.d/80-launcher.rules
fi
sudo cp udev/80-launcher.rules /etc/udev/rules.d/80-launcher.rules

echo "Checking current users group settings."
if ! groups | grep -q games ; then
  echo `whoami` " is not in group games, adding."
  sudo usermod -a -G games `whoami`
else
  echo `whoami` " is in group games."
fi

echo "Restarting udev service, please plug the launcher out and in again if applicable."
sudo service udev restart


#
# The following is necessary if you get the error:
#
# Traceback (most recent call last):
#   File "retaliation.py", line 83, in <module>
#     import usb.core
# ImportError: No module named core
# 
# See http://raspberrypi.stackexchange.com/questions/6774/installed-pyusb-still-importerror-no-module-named-core
#
if ! which pip ; then
  echo "Trying to install 'python-pip' to get a compatible version of 'libusb'."
  sudo apt-get install -y python-pip
else
  echo "Python pip is already installed."
fi

if ! pip search pyusb | grep -q INSTALLED ; then
  echo "'pyusb' is not installed yet via 'pip', installing."
  sudo pip install pyusb
else
  echo "'pyusb' seems to be installed using 'pip'."
fi

echo "Done."

