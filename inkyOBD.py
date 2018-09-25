#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
**********************************************************
*Filename inkyOBD.py                                     *
*Written by Rick Spooner <Spoonieau>                     *
*Github https://github.com/spoonieau                     *
*Date 23/09/18                                           *
*License Under GPL3                                      *
                                                         *
*The e-Ink Inkyphat Displays looked cool so I ordered one*
*to play around with and inkyOBD is the result. Looks    *
*cool and works great but the e-Ink display is not really*
*meant to be used for a real time display tho.           *
*                                                        *
*Dependencies                                            *
*Python https://www.python.org/                          *
*Inkyphat https://github.com/pimoroni/inky-phat          *
*Python-OBD https://python-obd.readthedocs.io/en/latest/ *
*Raspbian Jessie https://www.raspberrypi.org/downloads/  *
**********************************************************
'''

#To fix the UnicodeDecodeError with ELM327 usb clone adaptors 
#Follow https://github.com/brendan-w/python-OBD/issues/101

import inkyphat
from PIL import ImageFont
from PIL import Image
import obd
from obd import OBDStatus
import time
import sys

#Get around the 'UnicodeDecodeError: 'ascii' codec can't decode byte 0xfc in position 4:' issiue
reload(sys)
sys.setdefaultencoding('utf-8')

#Turn Debugging to console ON
obd.logger.setLevel(obd.logging.DEBUG)
#Turn Debugging to console OFF
#obd.logger.removeHandler(obd.console_handler)

#Set inkyphat screen type
inkyphat.set_colour("red")

#Set font and size (using inbuilt fonts)
font = ImageFont.truetype(inkyphat.fonts.FredokaOne, 20)

#Request and Recive data from the adaptor 
def getData():
    while (connOBD.status() == OBDStatus.CAR_CONNECTED):
    
        voltCmd = obd.commands.CONTROL_MODULE_VOLTAGE
        print("Sent CONTROL_MODULE_VOLTAGE")
        voltResp = connOBD.query(voltCmd)
        volts = (str(voltResp.value)[0:4])
        print("Recived " + volts)

        tempCmd = obd.commands.COOLANT_TEMP
        print("Sent COOLANT_TEMP") 
        tempResp = connOBD.query(tempCmd)
        temp = (str(tempResp.value)[0:2])
        print("Recived " + temp)
    
        loadCmd = obd.commands.ABSOLUTE_LOAD
        print("Sent ABSOLUTE_LOAD")
        loadResp = connOBD.query(loadCmd)
        load = (str(loadResp.value)[0:2])
        print("Recived " + load)
    
        airTempCmd = obd.commands.INTAKE_TEMP
        print("Sent INTAKE_TEMP")
        airResp = connOBD.query(airTempCmd)
        airTemp = (str(airResp.value)[0:2])
        print("Recived " + airTemp)
        
        timingCmd = obd.commands.TIMING_ADVANCE
        print("Sent TIMING_ADVANCE")
        timingResp = connOBD.query(timingCmd)
        timing = (str(timingResp.value)[0:2])
        print("Recived " + timing)
    
        displayVals(vVolts = volts, vTemp = temp, vLoad = load, vAirTemp = airTemp, vTiming = timing)
        time.sleep(3)
    else:
        disError(msg = "Error getting data")
        time.sleep(5)
        sys.exit()
    

#Create Display Strings and display on the inkyPhat 
def displayVals(vVolts, vTemp, vLoad, vAirTemp, vTiming):
    disVolts = "VOLTS: " + vVolts + "V"
    disTemp = "COOLANT: " + vTemp + "C" + u"\xb0"
    disLoad = "ABS LOAD: " + vLoad + "%"
    disAirTemp = "AIR TEMP: " + vAirTemp + "C" + u"\xb0"
    disTiming = "TIMING ADV: " + vTiming + u"\xb0"
    
    inkyphat.set_image(Image.open("/home/pi/errorBG.png"))

    inkyphat.text((1, 0), disVolts, inkyphat.BLACK, font)
    inkyphat.text((1, 20), disTemp, inkyphat.BLACK, font)
    inkyphat.text((1, 40), disLoad, inkyphat.BLACK, font)
    inkyphat.text((1, 60), disAirTemp, inkyphat.BLACK, font)
    inkyphat.text((1, 80), disTiming, inkyphat.BLACK, font)
    inkyphat.show()
    
    #Display error messages 
def disError(msg):
    inkyphat.set_image(Image.open("/home/pi/errorBG.png"))
    w, h = font.getsize(msg)
    x1 = (inkyphat.WIDTH / 2) - (w / 2)
    y1 = (inkyphat.HEIGHT / 2) - (h / 2)
    inkyphat.text((x1, y1), msg, inkyphat.BLACK, font)
    inkyphat.show()

#----------Program Starts Hear----------
disError(msg = "Trying To Connect!!!!")
    
connOBD = obd.OBD()

if (connOBD.status() == OBDStatus.CAR_CONNECTED):
    print("Auto Connection created @" + connOBD.port_name())
    print("Connected using the " + connOBD.protocol_name())
    getData()
else:
    print("Problem with creating a auto connection")
    time.sleep(3)
    disError(msg = "Error!! Not Connected")
    sys.exit

