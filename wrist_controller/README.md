CONTROL MY CAP: Wrist Controller
================================
These are the files that run on the wrist computer. They coordainte the MySQL data, tweeting, controlling the LCD, reading the buttons, and sending serial commands to the light. 

Usage Notes
-----------
* I am running Linux Occidentalis v0.2 (It has I2C support already set-up).
* Place all these files in `/home/pi/cap`.
* Create a local MySQL database table called "config" with just two columns:
    * option(Varchar 16)
    * value (Varchar 16)
* In the "config" table, create three entries and load them with the defaults:
    * option = "brightness", value = "10"
	* option = "mode", value = "9"
	* option = "last_tweeted", value = "0"
* Sign up for a Twitter Dev account, and [create an API app](https://dev.twitter.com/apps).  Give it read/write access and note the `Consumer Key` and the `Consumer Secret`.
* Rename 'sample_config.py' to 'config.py' and set the variables to the information for your MySQL Schema. Set the key info for your Twitter App.
* Make sure the `pi` user has access to the i2c bus.  By default, you must be `root`. To do this, run: `sudo adduser pi i2c`. You will need to logout and login for this to take effect.
* You need to SSH into the wrist computer and run command.py one time to complete the steps for twitter OAuth authentication.  You only need to do this once.
* `/etc/rc.local` is used to initialize the system at boot.  Add the following code to `/etc/rc.local` before `exit 0` (You need to be `root` to edit this file):  

        #Init SQL database mode to "off" state
		/home/pi/cap/boot.py

		#Get the Commander Program running the in the background.
		/home/pi/cap/command.py >>/var/www/log.txt &

		#Disable RTS for USB0 Serial Device, if successful, start program
		(stty -F /dev/ttyUSB0 -hup && /home/pi/cap/cap.py) || /home/pi/cap/fail.py

  
First, this boot script will set the mode to "off", incase you are operating off a wifi network. Then, `rc.local` will start running the command program in the background.  It will log to a txt file that you can view from a browser on a device connected to the same network.  This is useful for spotting bugs. Then, `rc.local` will disable RTS on the USB Serial line (This prevents the cap circuit board from reseting everytime the pySerial objects connnects). If that succeeds, the main control program is started. Otherwise, the failure is indicated by the fail script.
* You will want the computer to automatically associate with a wifi network on boot. Follow [these instructions](http://www.geeked.info/raspberry-pi-add-multiple-wifi-access-points/) to install wpa-supplicant, run it in background mode at boot, and generate the pre-shared keys for your WPA-protected networks.

Necessary Packages
------------------
You will need to have the following packages installed.
* [pySerial](http://pyserial.sourceforge.net/)
* [Python MySQLdb](http://sourceforge.net/projects/mysql-python/)
* [Adafruit Raspberry Pi Libraries](https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code) (Necessary files for I2C LCD Pi Plate Communications are already included here)
* [Python Twitter Tools](http://mike.verdone.ca/twitter/)

Attribution for Packaged Library Files
--------------------------------------
### Adafruit Python Libraries
Adafruit invests time and resources providing this open source code, please support Adafruit and open-source hardware by purchasing products from Adafruit!  
Written by Limor Fried, Kevin Townsend and Mikey Sklar for Adafruit Industries. BSD license, all text above must be included in any redistribution
