CONTROL MY CAP
==============
This Repo is still a work in progress!  Completion expected by May 25th, 2013.
------------------------------------------------------------------------------

These are the open design files for my "Control My Cap" project, which will enable crowd control of a high-intensity LED array mounted on my mortar board for my graduation from the Masters in Electrical and Computer Engineering Program at Cornell University.
  
The system is setup as follows:  
* A mobile-optimized website built using Jquery Mobile UI & a Python/MySQL backend sits on a cloud server.
* People visit the website and enter a twitter handle or name, plus a color (chosen from a palet).
* After picking a color, ajax calls are used to pass the information to a python script on the server via JSON messages.
* The python script on the cloud server adds information about the color request (ID, time, name, twitter_ID, and color) to a MySQL database that resides on the same cloud server.  Also included in each table entry is a "tweeted" column, which will get to "TRUE" once the system has tweeted that user's color selection (we only want this to happen once, even if we are doing a cycle)
* The graduate (that's me) is equipped with a 15V rechargable laptop battery, a high-intensity LED cap fixture, and a Raspberry Pi computer + LCD/button "Pi Plate" (the Wrist Interface)
* The Wrist interface is strapped to the graduate's wrist, and has uses the LCD to show system status.  Operation modes can be adjusted with buttons on the unit.  The Wrist controller is running [Linux Occidentalis v0.2](http://learn.adafruit.com/adafruit-raspberry-pi-educational-linux-distro/occidentalis-v0-dot-2).  It also has a Wifi USB dongle, and a USB-Serial Adapter attached.
* The USB-Serial adapter cable runs up the sleeve from the Write Computer to the LED array on the cap to send control commands (the cap runs an ATmega listening for Serial commands).
* Power runs from the wrist computer to the laptop battery pack where a 5V regulated supply is available.
* The battery pack is in a small drawstring backpack. It sends power the to wrist interface (5V), and up to the cap (15V).
* The wrist interface auto-runs a control program on boot.  It constantly checks the remote MySQL database, and updates its internal queue when the MySQL database gets updated.  The queue is then used to send color commands to the cap. When a new color is received, and it has not been tweeted yet, the wrist computer sends out a tweet and updates the database state variable.
  
Note:  I am opening as many files as I can.  Part of my design utilizes firmware and electronics from a another project of mine that I cannot (yet) open source.  You can sign up to learn more about it here: http://www.sunnlight.com.  

Included Folders and Repo Contents
----------------------------------

### /3D_printed_cap_holder
These are the 3D-printed design files for the mechanical PCB holder that sits on my head.

### /3D_printed_wrist_mount
These are the 3D-printed design files for the wrist-mounting unit. This enclosure houses and protects a Raspberry Pi, as well as an Adafruit LCD Pi-Plate.

### /mobile_site
These are the files that power the www.controlmycap.com mobile site. The front end is HTML+CSS+Jquery Mobile UI. It talks to a Python/MySQL backend via JSON AJAX calls.

### /wrist_controller
These are the linux scripts that run on the Raspberry Pi that is strapped to my wrist.

License
-------
This work is licensed under a Creative Commons Attribution-ShareAlike 3.0 Unported License.  
Please share improvements or remixes with the community, and attribute me (Jeremy Blum, http://www.jeremyblum.com) when reusing portions of my code.
http://creativecommons.org/licenses/by-sa/3.0/deed.en_US
