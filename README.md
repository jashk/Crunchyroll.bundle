About
=====
This plugin provides access to the content available at Crunchyroll.com. The plugin has been fully tested on both Windows and Mac. (I haven't tested it on Linux yet) This plugin does require the user to have a crunchyroll.com account, though one can be created for free at http://www.crunchyroll.com. Premium content and higher resolutions are available for premium accounts.

Please note that this plugin was coded and designed using an Anime premium Crunchyroll account. While most things related to Drama seem to work just fine, I have not extensively tested the drama side of this plugin as much as I have the Anime side. 

While this plugin is considered stable, there will always be bugs. Please submit bugs via the Github issue tracker on this page. I would also love to hear feedback and/or suggestions. 

Requirements
============
This plugin **requires** a Crunchyroll.com account. You can sign up for free at http://www.crunchyroll.com. When you get the plugin installed you will need to enter your username and password into the preferences section before you will be able to use it. 

Software Requirements:

* Plex Media Server (PMS) version 0.9.7.12 or later (http://www.plexapp.com/getplex/)
	* Tested on Windows & Mac only. May work with Linux. 
* Flash for "Other Browsers" (http://get.adobe.com/flashplayer/otherversions)

Installation
============
1. Download the latest version of the plugin from [here](https://github.com/MattRK/Crunchyroll.bundle/archive/v1.1.0.zip).

2. Unzip the content into the PMS plugins directory under your user account.
	* Windows 7, Vista, or Server 2008: C:\Users\[Your Username]\AppData\Local\Plex Media Server\Plug-ins
	* Windows XP, Server 2003, or Home Server: C:\Documents and Settings\[Your Username]\Local Settings\Application Data\Plex Media Server\Plug-ins
	* Mac/Linux: ~/Library/Application Support/Plex Media Server/Plug-ins

3. Rename the unzipped folder from "Crunchyroll.bundle-vx.x.x" to "Crunchyroll.bundle"

4. Restart PMS

Known Issues
============
* When you first start PMS you will get an "error" upon playing your first video. This is a bug in PMS that has not yet been resolved. You shouldn't see the error again unless you restart PMS. 

Frequently Asked Questions
==========================
**Q: I selected 1080P or 720P but the video is played in a lower resolution**

A: Not all content on Crunchyroll has HD quality videos available. This plugin will try to play content at the resolution you select. However, if a particular resolution is not available, it will play the next highest resolution available. You should also know that this plugin will only be able to show you content and resolutions you pay for. If you try to play a drama video at 720P but only pay for an Anime account, you will only be able to watch the 360P resolution video with ads. 

**Q: How do i hide mature content?**
A: You can choose what type of content to show by changing the Mature Content Filter setting found under "Account Settings" > "Video Preferences" of the http://www.crunchyroll.com website. 

To-do
====
- [ ] Add search functionality
- [x] Add "Genres" and "Seasons" filter under Anime and Drama
- [x] Add a new primary section called "Pop"
- [ ] Change the available_at & free_available_at descriptions to relative datetimes rather than actual datetimes. (E.g. 2 Days rather than 2013-03-05 11:00 PM) 
- [ ] Switch from Webkit to RTMP to improve quality
- [ ] Add support for Simulcast countdowns 
- [ ] Add resume/restart prefrence

Changes
=======
v1.0.1:
* Added more metadata to each video

v1.0.0:
* Initial release

Credits
=======
I want to thank pgp90 and JeremySH for their awesome plugin that has kept the Plex Anime & Drama community happy for the past few years. When I set out to help improve that plugin I had no idea that it would lead to a complete re-write of the code base. 