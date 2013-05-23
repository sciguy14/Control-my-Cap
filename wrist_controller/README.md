CONTROL MY CAP: Wrist Controller
================================
These are the files that run on the wrist computer. They coordainte the MySQL data, tweeting, controlling the LCD, reading the buttons, and sending serial commands to the light. 

Usage Notes
-----------
* I am running Linux Occidentalis v0.2 (It has I2C support already set-up).
* Place all these files in `/home/pi/cap`.
* Rename 'sample_config.py' to 'config.py' and set the variables to the information for your MySQL Schema.  
* Make sure the `pi` user has access to the i2c bus.  By default, you must be `root`. To do this, run: `sudo adduser pi i2c`. You will need to logout and login for this to take effect.
* `/etc/rc.local` is used to initialize the system at boot.  Add the following code to `/etc/rc.local` before `exit 0` (You need to be `root` to edit this file):  

        #Disable RTS for USB0 Serial Device, if successful, start program  
        (stty -F /dev/ttyUSB0 -hup && /home/pi/cap/cap.py) || /home/pi/cap/fail.py  
This will disable RTS on the USB Serial line (This prevents the cap circuit board from reseting everytime the pySerial objects connnects). If that succeeds, the main control program is started. Otherwise, the failure is indicated by the fail script.

Necessary Packages
------------------
You will need to have the following packages installed.
* [pySerial](http://pyserial.sourceforge.net/)
* [Python MySQLdb](http://sourceforge.net/projects/mysql-python/)
* [Adafruit Raspberry Pi Libraries](https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code] (Necessary files for I2C LCD Pi Plate Communications are already included here)
* [Python Twitter Tools](http://mike.verdone.ca/twitter/)

Attribution for Packaged Library Files
--------------------------------------
### Adafruit Python Libraries
Adafruit invests time and resources providing this open source code, please support Adafruit and open-source hardware by purchasing products from Adafruit!  
Written by Limor Fried, Kevin Townsend and Mikey Sklar for Adafruit Industries. BSD license, all text above must be included in any redistribution
