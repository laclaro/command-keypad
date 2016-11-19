#!/usr/bin/env python

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2016 Henning Hollermann

""" A simple keypad controller that executes custom shell commands on keypress 
    website: https://laclaro.wordpress.com/
"""

import yaml
import sys, os
from optparse import OptionParser
from evdev import InputDevice, list_devices, ecodes
from select import select

__author__ = "Henning Hollermann"
__license__ = "GPLv3"
__version__ = "1.0"
__email__ = "laclaro@mail.com"

class Controller:
    def __init__(self, config, inputdevice):
        self.config = config
        self.input_device = InputDevice(inputdevice)

    """run loop, which reads from inputdevice"""
    def run(self):
        while True:
            self.handleKeypress(cmd_list_name = "cmds1")

    """execute one or several commands if matching key was pressed"""
    def handleKeypress(self, cmd_list_name):
        # wait until we can read, 2 sec timeout
        a, b, c = select([self.input_device], [], [], 2)
        if not a:
            return
        try:
            for event in self.input_device.read():
                # only track key down events
                if event.type == ecodes.EV_KEY and event.value == 1:
                    if event.code == self.config["quit_keycode"]:
                        # q pressed => quit
                        print("q pressed")
                    else:
                        # use second command list if modifier key is toggled
                        if event.code == self.config["modifier_keycode"]:
                            cmd_list_name = "cmds2"

                        # iterate over all command_list and check if a key_trigger 
                        # matches current keypress
                        action_triggered = False
                        for command in self.config["command_list"]:
                            if event.code == command["keycode"]:
                                try:
                                    # is command["cmds1"] a single command (basestring)?
                                    if isinstance(command[cmd_list_name], basestring):
                                        command[cmd_list_name] = [command[cmd_list_name]]
                                    for cmd in command[cmd_list_name]:
                                        if not os.system(cmd) == 0:
                                            print("Command: \'%s\' failed!" % cmd)
                                        else:
                                            print("%s triggered!" % command["name"])
                                    action_triggered = True
                                    break
                                except KeyError:
                                    break

                        if action_triggered == False:
                            print("Unmapped key code: %d" % event.code)
        except IOError:
            # TODO: make the script handle temporary device removal to run "standalone" without systemd
            print("Device removed. Exiting Script.")
            sys.exit()

"""Print list of devices"""
def print_input_devices():
    devices = map(InputDevice, list_devices())
    print "Error: You need to specify one of the following input devices:"
    for dev in devices:
        print('  %-20s %-32s' % (dev.fn, dev.name))
    print

# parse option and run script
parser = OptionParser()
parser.add_option("-c", "--config", dest="configfile", 
            help="load configuration from FILE", metavar="FILE")
parser.add_option("-i", "--input", dest="inputdevice", 
            help="input device to use (example /dev/input/event0)", metavar="DEVICE")
(options, args) = parser.parse_args()

# check parameters
if not options.configfile:
    print("Error: You need to specify a configuration file")
    parser.print_help()
    sys.exit(-1)
elif not options.inputdevice:
    print_input_devices()
    parser.print_help()
    sys.exit(-1)

# load config
f = open(options.configfile, 'r')
config = yaml.safe_load(f)
f.close

# start app
controller = Controller(config, options.inputdevice)
controller.run()
