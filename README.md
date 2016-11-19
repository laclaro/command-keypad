command-keypad
==================

This script is used to control a keyboard or keypad to execute custom commands with every key press.

Install
-------

Make sure you have a linux system with python installed. In particular the script needs python-evdev available in many distributions repositories. Otherwise install it via pip.

	sudo pip install PyYAML evdev
	
Now you can run the controller with the sample configuration file:

	sudo ./command-keypad.py -c layout-novatek.yaml
	
The evdev library captures the keyboard input on device level and needs root privileges. The above command will search for all available input devices and list them:

	Error: You need to specify one of the following input devices:
	  /dev/input/event3    ImExPS/2 Generic Explorer Mouse 
	  /dev/input/event2    AT Translated Set 2 keyboard    
	  /dev/input/event1    Sleep Button                    
	  /dev/input/event0    Power Button
	  
Select your keyboard and add the device to the command line:

	sudo ./command-keypad.py -c layout-novatek.yaml -i /dev/input/event2
	
The controller will play the first scene. You should see the DMX values change in ola_dmxmonitor. Try changing scenes with the number keys. If you press a key that is not mapped to a scene, the key code will be displayed, so that you can configure this key in the yaml file.

Press 'q' to quit.

Configuration
-------------

