# -*- coding: utf-8 -*-

import sys
import os
import xbmcaddon
import xbmcgui
import xbmc
from urllib2 import urlopen
import xml.etree.ElementTree as ET


reload(sys)
sys.setdefaultencoding('utf8')


addon = xbmcaddon.Addon(id='script.365.epg.generator')
userpath = addon.getAddonInfo('profile')
custom_channels = xbmc.translatePath("%s/custom_channels.txt" % userpath).decode('utf-8')
channels_select_path = xbmc.translatePath("%s/select_channels.txt" % userpath).decode('utf-8')



def select():
    channels = []
    channels.append("BBC Earth")
    html = urlopen("http://programandroid.365dni.cz/android/v5-tv.php?locale=cs_CZ").read()
    root = ET.fromstring(html)
    for i in root.iter('a'):
        if 'c' in i.attrib:
            channels.append(i.find('n').text)
    try:
        ch = open(channels_select_path, "r").read()
    except:
        ch_preselect = []
    try:
        if ch == "":
            ch_preselect = []
    except:
        ch_preselect = []
    else:
        ch = ch.split("\n")[:-1]
        ch_preselect = []
        for i in ch:
            ch_preselect.append(channels.index(i))
    repair_channels = []
    dialog = xbmcgui.Dialog()
    types = dialog.multiselect("Kanály", channels, preselect=ch_preselect)
    if types is None:
        pass
    else:
        for index in types:
            repair_channels.append(channels[index])
        f = open(channels_select_path, "w")
        for x in repair_channels:
            f.write(x + "\n")
        f.close()
        select_channels = []
        f = open(custom_channels, "w")
        if "BBC Earth" in repair_channels:
            select_channels.append("0")
        for i in root.iter('a'):
            if 'c' in i.attrib:
                if i.find('n').text in repair_channels:
                    select_channels.append(i.attrib["id"])
        f.write(",".join(select_channels))
        f.close()
        xbmcgui.Dialog().notification("365 EPG Grabber","Uloženo", xbmcgui.NOTIFICATION_INFO, 4000, sound = False)
    sys.exit(0)


if __name__ == "__main__":
    select()