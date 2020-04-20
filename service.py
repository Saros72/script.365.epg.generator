# -*- coding: utf-8 -*-

import xbmcaddon
import sys
import xbmc


addon = xbmcaddon.Addon(id='script.365.epg.generator')


def update():
    if addon.getSetting("start_enabled") == "true":
        xbmc.executebuiltin('RunAddon("script.365.epg.generator")')
        if addon.getSetting("auto_enabled") == "true":
            xbmc.executebuiltin('RunScript("special://home/addons/script.365.epg.generator/runner.py")')
        else:
            sys.exit(0)
    else:
        if addon.getSetting("auto_enabled") == "true":
            xbmc.executebuiltin('RunScript("special://home/addons/script.365.epg.generator/runner.py")')
        else:
            sys.exit(0)


if __name__ == '__main__':
    update()