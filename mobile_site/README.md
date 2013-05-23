CONTROL MY CAP: Mobile Site
======================================
These are the files that power the mobile site.  They are running on a remote cloud server. Python 2.6 is used, and the MySQLdb library must be installed. 

Usage Notes
-----------
To use this, you will need to rename 'sample_config.py' in the cgi-bin to 'config.py' and set the variables to the information for your MySQL Schema.  
  
You should have on MySQL database table setup as follows:
* index (autoincrementing & primary key)
* time (MySQL timestamp default)
* name (Varchar, Length 16)
* twitter (Varchar, Length 16)
* color (char, Length 7)
* tweeted (boolean, default=0)

Useful Links & Resources
------------------------
* (JQuery Mobile)[http://jquerymobile.com/]
* (JQUery MiniColors)[https://github.com/claviska/jquery-miniColors]
* (Python MySQLdb)[http://sourceforge.net/projects/mysql-python/]
