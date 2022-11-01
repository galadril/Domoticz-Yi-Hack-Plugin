
# Domoticz-Yi-Hack

Yi Hack Plugin for Domoticz home automation
This plugin allows you to set various configuration on Yi Cameras that have one of the next Yi Hacks installed:  

[MStar](https://github.com/roleoroleo/yi-hack-MStar/wiki/Web-services-description) 
[AllWinner](https://github.com/roleoroleo/yi-hack-Allwinner) 


## Supported cameras

See the MStar/AllWinner github pages for a list of all supported camera's 

| Camera | Yi Hack |
| --- | --- |
| **Yi 1080p Home 9FUS** | AllWinner |
| **Yi 1080p Home BFUS** | AllWinner |
| **Yi 1080p Home 4FUS** | MStar |
| **Yi 1080p Home 6FUS** | MStar |
| **Yi 1080p Home 9FUS** | MStar |
| **Yi 1080p Home BFUS** | MStar |
| **Yi 1080p Dome 6FUS** | MStar |
| **Yi 1080p Dome BFUS** | MStar |
| **Yi 1080p Home 4FUS** | MStar |
| **Yi 1080p Home 9FUS** | MStar |
| **Yi 1080p Home 6FUS** | MStar |
| **Yi 1080p Home 6FCN** | MStar |


## Key Features

* Creates four Domoticz devices per camera
  1. Turn the camera on or off
  2. Selector switch for the sensitivity mode: Low/Medium/High
  3. Set the led/ir led on or off
  4. Enable or disable 'save video on motion' mode
  
* When network connectivity is lost the Domoticz UI will optionally show the device(s) with Red banner

![devices](https://user-images.githubusercontent.com/14561640/87668218-0905ec80-c76c-11ea-9107-ff49395ffb00.png)


## Installation

Python version 3.4 or higher required & Domoticz version 3.87xx or greater.

To install:
* Go in your Domoticz directory using a command line and open the plugins directory.
* Run: ```git clone https://github.com/galadril/Domoticz-Yi-Hack-Plugin.git```
* Restart Domoticz.

In the web UI, navigate to the Hardware page.  In the hardware dropdown there will be an entry called "Yi-Hack".


## Updating

To update:
* Go in your Domoticz directory using a command line and open the plugins directory then the Domoticz-Yi-Hack-Plugin directory.
* Run: ```git pull```
* Restart Domoticz.


## Change log

| Version | Information |
| ----- | ---------- |
| 0.0.1 | Initial upload version |
| 0.0.2 | Fixed issue with empty payloads |


# Donation

If you like to say thanks, you could always buy me a cup of coffee (/beer)!   
(Thanks!)  
[![PayPal donate button](https://img.shields.io/badge/paypal-donate-yellow.svg)](https://www.paypal.me/markheinis)
