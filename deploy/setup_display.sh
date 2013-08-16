#!/bin/sh

#
# This script makes sure that all requirements for the ci dashboard display
# are installed. If there is an error during setup, please try to do these
# steps manually and report the issue.
#
# Requirements:
# - sudo configured to allow everything
# - X configured and running
# - LXDE as X session manager
#    (or configure the autostart functionality yourself)
# - midori
# - ttf-mscorefonts-installer
#

echo "Checking if midori is installed."
if ! which midori; then
  echo "midori is not installed, installing."
  sudo apt-get install -y midori
else
  echo "midori is installed."
fi

echo "Installing mscorefonts."
sudo apt-get install -y ttf-mscorefonts-installer

echo "Installing dash-billboard start command to /usr/bin."
chmod a+x dash-billboard
if [ -f /usr/bin/dash-billboard ]; then
  sudo rm /usr/bin/dash-billboard
fi
sudo ln -s $PWD/dash-billboard /usr/bin

echo "Adding dash-billboard command into LXDE autostart. ~/.config/lxsession/LXDE/autostart"
mkdir -p $HOME/.config/lxsession/LXDE
touch $HOME/.config/lxsession/LXDE/autostart
if ! grep -q dash-billboard $HOME/.config/lxsession/LXDE/autostart; then
  echo "dash-billboard" >> "$HOME/.config/lxsession/LXDE/autostart"
fi

echo "Placing midori configuration file to ~/.config"

# Place midori configuration (configuration has to be used in favor of using command line
# options, since same origin policy is not settable in midori 4.x via command line and
# command line and config file options can't be mixed. Therefore everything is specified
# via config file.
if [ -f $HOME/.config/midori/config ]; then
  rm $HOME/.config/midori/config
fi
sudo ln -s $PWD/midori_config $HOME/.config/midori/config

echo "Done."

