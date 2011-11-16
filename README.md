#What is NiftyArticles

NiftyArticles is a small Python script which lets you identify and save articles from inside webpages. It is based on Readability.
Update 10.02.2011

#Installation

* Download NiftyArticles QT4
* Download NiftyArticles GTK
* Download readability.js
* Each version depends on readability.js, please download that file and place it in the same directory as the niftyarticle script.

#The installation details for each version is located inside the script file.
Usage (QT4 version)

To get a full list of options, run:
python niftyarticles-qt.py --help
OR if you made it executable,
/path/to/niftyarticles-qt.py --help

# save an article from ubuntu.com
python niftyarticles-qt.py -u http://www.ubuntu.com/project/derivatives
Help for the QT4 version

#The script has been developed and tested on Python 2.6.6 / Ubuntu Maverick

* Install the required packages: python-qt4 libqt4-webkit
* Ubuntu or Debian
* sudo apt-get install python2.6 python-qt4 libqt4-webkit

* (Optional) Mark the script as executable
* chmod +x niftyarticles-qt.py

##Usage Examples:
python niftyarticles-qt.py --help

# save an article from ubuntu.com
python niftyarticles-qt.py -u http://www.ubuntu.com/project/derivatives

# show the browser window, load images, enable java applets
python niftyarticles-qt.py -b -i -v -u http://www.ubuntu.com/project/canonical-and-ubuntu

# to run the script on a server with no GUI available, you must install xvfb
sudo apt-get install xvfb
# then you can do
xvfb-run -a python niftyarticles-qt.py -u http://www.ubuntu.com/project/derivatives

Webkit Reference
http://webkitgtk.org/reference/index.html

Source code (QT4)

#!/usr/bin/env python
"""
------------------------------------
NiftyArticles v0.4, Qt4 version

Made by Florentin Sardan
florentinwww (at) gmail.com

Project's page:
    http://www.betterprogramming.com/niftyarticles-extract-articles-from-any-webpage-with-python-webkit-and-readability.html
My portfolio:
    http://www.betterprogramming.com/

Readability webpage:
    http://lab.arc90.com/experiments/readability/
------------------------------------
The script has been developed and tested on Python 2.6.6 / Ubuntu Maverick

Install the required packages: python-qt4 libqt4-webkit
Ubuntu or Debian
sudo apt-get install python2.6 python-qt4 libqt4-webkit

(Optional) Mark the script as executable
chmod +x niftyarticles-qt.py

Usage Examples:
python niftyarticles-qt.py --help

# save an article from ubuntu.com
python niftyarticles-qt.py -u http://www.ubuntu.com/project/derivatives

# show the browser window, load images, enable java applets
python niftyarticles-qt.py -b -i -v -u http://www.ubuntu.com/project/canonical-and-ubuntu

# to run the script on a server with no GUI available, you must install xvfb
sudo apt-get install xvfb
# then you can do
xvfb-run -a python niftyarticles-qt.py -u http://www.ubuntu.com/project/derivatives

#Webkit Reference
http://webkitgtk.org/reference/index.html

