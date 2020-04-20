# -*- coding: utf-8 -*-

import xbmcaddon
import sys
import xbmc
import time
import xbmcgui
from datetime import datetime, timedelta

addon = xbmcaddon.Addon(id='script.365.epg.generator')

def update():
    if addon.getSetting("notice") == "true":
        xbmcgui.Dialog().notification("365 EPG Grabber","Akualizace: " + addon.getSetting("auto_time"), xbmcgui.NOTIFICATION_INFO, 4000, sound = False)
    while True:
        time.sleep(1)
        if addon.getSetting("auto_enabled") == "true":
            if addon.getSetting("auto_time") + ":00" == datetime.now().strftime("%H:%M:%S"):
                xbmc.executebuiltin('RunAddon("script.365.epg.generator")')
        else:
            break
    xbmcgui.Dialog().notification("365 EPG Grabber","Vypnutá automatická aktualizace", xbmcgui.NOTIFICATION_INFO, 4000, sound = False)
    sys.exit(0)


if __name__ == '__main__':
    update()