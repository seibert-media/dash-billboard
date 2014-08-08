#!/usr/bin/python
#
# Original work Copyright 2011 PaperCut Software Int. Pty. Ltd. http://www.papercut.com/
#                              https://github.com/codedance/Retaliation
# Modified work Copyright 2013 //SEIBERT/MEDIA GmbH https://www.seibert-media.net
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
# 

############################################################################
# 
# RETALIATION or zuechtigen.py - A Jenkins "Extreme Feedback" Contraption
#
#    Lava Lamps are for pussies! Retaliate to a broken build with a barrage 
#    of foam missiles.
#
# Steps to use:
#
#  1.  Mount your Dream Cheeky Thunder USB missile launcher in a central and 
#      fixed location.
#
#  2.  Copy this script onto the system connected to your missile lanucher.
#
#  3.  Modify your `COMMAND_SETS` in the `zuechtigen.py` script to define 
#      your targeting commands for each one of your build-braking coders 
#      (their user ID as listed in Jenkins).  A command set is an array of 
#      move and fire commands. It is recommend to start each command set 
#      with a "zero" command.  This parks the launcher in a known position 
#      (bottom-left).  You can then use "up" and "right" followed by a 
#      time (in milliseconds) to position your fire.
# 
#      You can test a set by calling zuechtigen.py with the target name. 
#      e.g.:  
#
#           zuechtigen.py "[developer's user name]"
#
#      Trial and error is the best approch. Consider doing this secretly 
#      after hours for best results!
#
#  4.  Setup the Jenkins "notification" plugin. Define a UDP endpoint 
#      on port 22222 pointing to the system hosting this script.
#      Tip: Make sure your firewall is not blocking UDP on this port.
#
#  5.  Start listening for failed build events by running the command:
#          zuechtigen.py stalk
#      (Consider setting this up as a boot/startup script. On Windows 
#      start with pythonw.exe to keep it running hidden in the 
#      background.)
#
#  6.  Wait for DEFCON 1 - Let the war games begin!
#
#
#  Requirements:
#   * A Dream Cheeky Thunder USB Missile Launcher
#   * Python 2.6+
#   * Python PyUSB Support and its dependencies 
#      http://sourceforge.net/apps/trac/pyusb/
#      (on Mac use brew to "brew install libusb")
#   * Should work on Windows, Mac and Linux
#
#  Author:  Chris Dance <chris.dance@papercut.com>
#  Version: 1.0 : 2011-08-15
#
#  Modified for dash-billboard: Benjamin Peter <bpeter@seibert-media.net>
#                               2013-07-13
#
############################################################################

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import Log
import Device
import Config
import Stalk
#import Guard
import CommandSet

def usage():
    print "Usage: zuechtigen.py [command] [value]"
    print ""
    print "   commands:"
    print "     stalk - sit around waiting for a Jenkins CI failed build"
    print "             notification, then attack the perpetrator!"
    print "     guard - sits around and waits for faces(!) to shoot at, needs a camera"
    print ""
    print "     up    - move up <value> milliseconds"
    print "     down  - move down <value> milliseconds"
    print "     right - move right <value> milliseconds"
    print "     left  - move left <value> milliseconds"
    print "     fire  - fire <value> times (between 1-4)"
    print "     zero  - park at zero position (bottom-left)"
    print "     pause - pause <value> milliseconds"
    print "     led   - turn the led on or of (1 or 0)"
    print ""
    print "     <command_set_name> - run/test a defined COMMAND_SET"
    print "             e.g. run:"
    print "                  zuechtigen.py 'chris'"
    print "             to test targeting of chris as defined in your command set."
    print ""



def main(args):
  if len(args) < 2:
    usage()
    sys.exit(1)

  Log.log("setting up usb device")

  device = Device.Device()
  device.setup()

  if args[1] == "stalk":
    Log.log("polling and waiting for failed builds ...")
    Stalk.Stalk(device).poll_commit_status()
    # Will never return
    return
  elif args[1] == "guard":
    Log.log("guarding and waiting for faces *muhahahaha* ...")
    Guard.Guard(device, Config.CAM_DEVICE_INDEX).start()
    # Will never return
    return
  else:
    # Process any passed commands or command_sets
    command = args[1]
    value = 0
    if len(args) > 2:
      value = int(args[2])
    
    CommandSet.run(device, command, value)

if __name__ == '__main__':
  main(sys.argv)

