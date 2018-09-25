#inkyOBD

Small python script to gather OBD2 data via a clone ELM327 usb adapter and rpi ZERO W to output to a Pimoroni InkyPhat e-Ink screen.

Works well, looks good just a very low refresh rate.

Usage:
  1. Place inkyOBD.py and errorBG.png in /home/pi
  2. Add <code>python inkyOBD.py</code> in pi user .bashrc
  3. Using raspi-config, set pi user to auto-login
  4. Shutdown rpi 
  5. Connect ELM327 usb adapter 
  6. Power it up and watch it to it's thing

Short video of it in action 
https://youtu.be/nuqoGRrBhuo

Dependencies                                            
Python https://www.python.org/                          
Inkyphat https://github.com/pimoroni/inky-phat          
Python-OBD https://python-obd.readthedocs.io/en/latest/ 
Raspbian Jessie https://www.raspberrypi.org/downloads/  
