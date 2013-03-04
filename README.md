About
=====
The Crunchyroll.bundle Plex Media Server plugin provides access to the content 
available at Crunchyroll.com. 

Most content is available to free users in a *low resolution* format that plays 
*advertisements* throughout the episode. If don't want these ads or would 
like a higher resolution, you will need a premium account. You can start a 
14-day free trial by visiting http://www.crunchyroll.com/freetrial. 

Lastly, this plugin was coded and designed while using an Anime premium Crunchyroll
account. While most things related to Drama seem to work just fine, I have not 
extensively tested the drama side of this plugin as I have the Anime side. 

Requirements
============
This plugin **requires** a Crunchyroll.com account. You can sign up for free at 
(http://www.crunchyroll.com). When you get the plugin installed you will need
to enter your username and password into the preferences section before you will
be able to use it. 

Software Requirements:

* Plex Media Server (PMS) version 0.9.7.12 or later (http://www.plexapp.com/getplex/)
	* Tested on Windows & Mac only. May work with Linux. 
* Flash for "Other Browsers" (http://get.adobe.com/flashplayer/otherversions)

Installation
============
1. Download the latest version of the plugin from [here](https://github.com/MattRK/Crunchyroll.bundle/archive/master.zip).

2. Unzip the content into the PMS plugins directory under your user account.
	* Windows 7, Vista, or Server 2008: C:\Users\[Your Username]\AppData\Local\Plex Media Server\Plug-ins
	* Windows XP, Server 2003, or Home Server: C:\Documents and Settings\[Your Username]\Local Settings\Application Data\Plex Media Server\Plug-ins
	* Mac/Linux: ~/Library/Application Support/Plex Media Server/Plug-ins

	3. Restart PMS

Known Issues
============
- [ ] When you first start PMS you will get an "error" upon playing your first video. This is a bug in PMS that has not yet been resolved. 

To-do
====
- [ ] Add search functionality
- [ ] Add "Genres" and "Seasons" filter under Anime and Drama
- [ ] Change the available_at & free_available_at descriptions to relative datetimes rather than actual datetimes. (E.g. 2 Days rather than 2013-03-05 11:00 PM) 

Changes
=======
2013-03-03:
	* Initial Commit

Credits
=======
I want to thank pgp90 and JeremySH for their awesome plugin that has kept the 
Plex Anime & Drama community happy for the past few years. When I set out to 
help improve that plugin I had no idea that it would lead to a complete re-write 
of the code base. 