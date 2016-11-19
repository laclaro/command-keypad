command-keypad
==================

This script is used to control a keyboard or keypad to execute custom commands with every key press.

Install
-------

Make sure you have a linux system with python installed. In particular the script needs python-evdev available in many distributions repositories. Otherwise install it via pip.

	sudo pip install PyYAML evdev
	
Now you can run the controller with the sample configuration file:

	sudo ./command-keypad.py -c conf/simpleconfig.yaml
	
The evdev library captures the keyboard input on device level and needs root privileges. The above command will search for all available input devices and list them:

	Error: You need to specify one of the following input devices:
	  /dev/input/event3    ImExPS/2 Generic Explorer Mouse 
	  /dev/input/event2    AT Translated Set 2 keyboard    
	  /dev/input/event1    Sleep Button                    
	  /dev/input/event0    Power Button
	  
Select your keyboard and add the device to the command line:

	sudo ./command-keypad.py -c conf/simpleconfig.yaml -i /dev/input/event2
	
The script will now listen to your keyboard inputs. Try pressing a key to execute the mapped command. If you press a key that is not mapped, the key code will be displayed, so that you can configure this key in the yaml file.

Press 'q' to quit (see `quit_keycode` below).

Configuration
-------------

The key-to-command-mapping is configured by a text file in YAML format. The best idea is to start of from one of the configuration files within the conf/ directory. The key values are described in the following.

* `#` is the line comment character.

* `quit_keycode` denotes the keycode for executing the script.

* `modifier_keycode` identifies the modifier that enables you to switch between the two command set levels cmds1 and cmds2. This may be the numlock toggle on a small keypad.

The key-to-command-mappings are then listed in the command_list they have several key values in common:

* `name` is the human readable name of the mapping.

* `keycode` is the keycode that will trigger this command set. The easiest way to find key codes is to start the script and press the keys you want to use. If these keys are not already mapped to a command, the script will display the key code. You can then enter this code into the configuration file.

* `cmds1` is a single or even a list of shell commands that will be executed whenever the mapped key is pressed.

* `cmds2` is essentially the same as cmds1 but these commands will be triggered if the modifier key defined by modifier_keycode is toggeled.
