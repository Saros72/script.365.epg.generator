# -*- coding: utf-8 -*-

import sys
import os
import xmltv
import xbmcaddon
import xbmcgui
import xbmc
from ftplib import FTP
from urllib2 import urlopen, Request
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from urllib import urlencode


reload(sys)
sys.setdefaultencoding('utf8')
addon = xbmcaddon.Addon(id='script.365.epg.generator')
download_path = addon.getSetting("folder")
userpath = addon.getAddonInfo('profile')
custom_channels = xbmc.translatePath("%s/custom_channels.txt" % userpath).decode('utf-8')


def upload(notice):
    if addon.getSetting("ftp_enabled") == "true":
        ftp = FTP()
        ftp.set_debuglevel(2)
        ftp.connect(addon.getSetting("ftp_server"), addon.getSetting("ftp_port"))
        ftp.login(addon.getSetting("ftp_login"), addon.getSetting("ftp_password"))
        ftp.cwd(addon.getSetting("ftp_folder"))
        file = open(download_path + addon.getSetting("file_name"),'rb')
        ftp.storbinary('STOR ' + addon.getSetting("file_name"), file)
        file.close()
        ftp.quit()
        if notice == 1:
            xbmcgui.Dialog().notification("365 EPG Generator","Hotovo, nahráno na server", xbmcgui.NOTIFICATION_INFO, 4000, sound = False)
    else:
        if notice == 1:
            xbmcgui.Dialog().notification("365 EPG Grabber","Hotovo, uloženo ve složce", xbmcgui.NOTIFICATION_INFO, 4000, sound = False)


def bbc():
    headers = {"Accept-Language": "cs-CZ,en-US;q=0.9", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9","Referer":"https://www.satelitnatv.sk/tv-program/bbc-earth/", "Host": "www.satelitnatv.sk", "Content-type" : "application/x-www-form-urlencoded", "origin" : "https://www.satelitnatv.sk", "except-encoding" : "gzip, deflate"}
    programmes2 = []
    now = datetime.now()
    if addon.getSetting("day_enabled") == "true":
        de = -1
    else:
        de = 0
    for i in range(de, int(addon.getSetting("num_days"))):
        next_day = now + timedelta(days = i)
        date = next_day.strftime("%d.%m.%Y")
        data = urlencode({'datum' : date, 'casOd' : 'cely_den', 'channel[]' : 'BBC Earth', 'channels_sub' : 'Submit'})
        req = Request("https://satelitnatv.sk/tv-program/bbc-earth/", data, headers)
        res = urlopen(req).read()
        soup = BeautifulSoup(res, 'html.parser')
        items = soup.find_all('td',onclick=True)
        for x in items:
            name = x["onclick"].split("'")[1]
            desc = x["onclick"].split("'")[15]
            date = (x["onclick"].split("'")[13]).split(".")
            date = date[2] + date[1] + date[0]
            start_time = date + x["onclick"].split("'")[7].replace(":", "") + "00"
            stop_time = date + x["onclick"].split("'")[9].replace(":", "") + "00"
            programm = {'channel': '0-bbc-earth', 'start': start_time + " +0200", 'stop': stop_time + " +0200", 'title': [(name, u'')], 'desc': [(desc, u'')]}
            if programm not in programmes2:
                programmes2.append(programm)
    for x in range(0, len(programmes2)):
        try:
            programmes2[x]["stop"]  = programmes2[x + 1]["start"]
        except: pass
    return programmes2


def get_channels_list():
    channels = []
    ch = {}
    html = urlopen("http://programandroid.365dni.cz/android/v5-tv.php?locale=cs_CZ").read()
    root = ET.fromstring(html)
    for i in root.iter('a'):
        if 'c' in i.attrib:
            if addon.getSetting("category") == "0":
                if i.attrib["c"] == "CZ" or i.attrib["c"] == "SK":
                    ch[i.attrib["id"]] = (i.attrib["id"] + "-" + i.find('n').text).replace(" ", "-").lower()
                    if addon.getSetting("logo_enabled") == "true":
                        channels.append({'display-name': [(i.find('n').text, u'cs')], 'id': (i.attrib["id"] + "-" + i.find('n').text).replace(" ", "-").lower(), 'icon': [{'src': 'http://portal2.sms.cz/kategorie/televize/bmp/loga/velka/' + str(i.find('o').text)}]})
                    else:
                        channels.append({'display-name': [(i.find('n').text, u'cs')], 'id': (i.attrib["id"] + "-" + i.find('n').text).replace(" ", "-").lower()})
            elif addon.getSetting("category") == "2":
                try:
                    cch = open(custom_channels, "r").read().split(",")
                except:
                    xbmcgui.Dialog().notification("365 EPG Grabber","Žádné vladtní kanály", xbmcgui.NOTIFICATION_ERROR, 4000, sound = False)
                    sys.exit(0)
                if i.attrib["id"] in cch:
                    ch[i.attrib["id"]] = (i.attrib["id"] + "-" + i.find('n').text).replace(" ", "-").lower()
                    if addon.getSetting("logo_enabled") == "true":
                        channels.append({'display-name': [(i.find('n').text, u'cs')], 'id': (i.attrib["id"] + "-" + i.find('n').text).replace(" ", "-").lower(),'icon': [{'src': 'http://portal2.sms.cz/kategorie/televize/bmp/loga/velka/' + str(i.find('o').text)}]})
                    else:
                        channels.append({'display-name': [(i.find('n').text, u'cs')], 'id': (i.attrib["id"] + "-" + i.find('n').text).replace(" ", "-").lower()})
            else:
                ch[i.attrib["id"]] = (i.attrib["id"] + "-" + i.find('n').text).replace(" ", "-").lower()
                if addon.getSetting("logo_enabled") == "true":
                    channels.append({'display-name': [(i.find('n').text, u'cs')], 'id': (i.attrib["id"] + "-" + i.find('n').text).replace(" ", "-").lower(),'icon': [{'src': 'http://portal2.sms.cz/kategorie/televize/bmp/loga/velka/' + str(i.find('o').text)}]})
                else:
                    channels.append({'display-name': [(i.find('n').text, u'cs')], 'id': (i.attrib["id"] + "-" + i.find('n').text).replace(" ", "-").lower()})
    chl = ','.join(ch.keys())
    return chl, ch, channels


def main(notice):
    try:
        cchc = open(custom_channels, "r").read().split(",")
    except:
        cchc = []
    chl, ch, channels = get_channels_list()
    programmes = []
    if chl != "":
        if notice == 1:
            xbmcgui.Dialog().notification("365 EPG Generator","Generuje se...", xbmcgui.NOTIFICATION_INFO, 3000, sound = False)
        now = datetime.now()
        if addon.getSetting("day_enabled") == "true":
            de = -1
        else:
            de = 0
        for i in range(de, int(addon.getSetting("num_days"))):
            next_day = now + timedelta(days = i)
            date = next_day.strftime("%Y-%m-%d")
            html = urlopen("http://programandroid.365dni.cz/android/v5-program.php?datum=" + date + "&id_tv=" + chl).read()
            root = ET.fromstring(html)
            root[:] = sorted(root, key=lambda child: (child.tag,child.get('o')))
            for i in root.iter('p'):
                n = i.find('n').text
                try:
                    k = i.find('k').text
                except:
                    k = ''
                programmes.append({'channel': ch[i.attrib["id_tv"]], 'start': i.attrib["o"].replace("-", "").replace(":", "").replace(" ", "") + " +0200", 'stop': i.attrib["d"].replace("-", "").replace(":", "").replace(" ", "") + " +0200", 'title': [(n, u'')], 'desc': [(k, u'')]})
        if addon.getSetting("category") == "0" or addon.getSetting("category") == "1":
            if addon.getSetting("logo_enabled") == "true":
                channels.append({'display-name': [('BBC Earth', u'cs')], 'id': '0-bbc-earth','icon': [{'src': 'https://www.satelitnatv.sk//obrazky/loga_stanic/50/bbc_earth_50.png'}]})
            else:
                channels.append({'display-name': [('BBC Earth', u'cs')], 'id': '0-bbc-earth'})
            programmes2 = bbc()
            for y in programmes2:
                programmes.append(y)
        else:
            if "0" in cchc:
                if addon.getSetting("logo_enabled") == "true":
                    channels.append({'display-name': [('BBC Earth', u'cs')], 'id': '0-bbc-earth','icon': [{'src': 'https://www.satelitnatv.sk//obrazky/loga_stanic/50/bbc_earth_50.png'}]})
                else:
                    channels.append({'display-name': [('BBC Earth', u'cs')], 'id': '0-bbc-earth'})
                programmes2 = bbc()
                for y in programmes2:
                    programmes.append(y)
        w = xmltv.Writer(encoding="utf-8", source_info_url="http://www.funktronics.ca/python-xmltv", source_info_name="Funktronics", generator_info_name="python-xmltv", generator_info_url="http://www.funktronics.ca/python-xmltv")
        for c in channels:
            w.addChannel(c)
        for p in programmes:
            w.addProgramme(p)
        w.write(download_path + addon.getSetting("file_name"), pretty_print=True)
        upload(notice)
    elif "0" in cchc:
        if notice == 1:
            xbmcgui.Dialog().notification("365 EPG Generator","Generuje se...", xbmcgui.NOTIFICATION_INFO, 3000, sound = False)
        if addon.getSetting("logo_enabled") == "true":
            channels.append({'display-name': [('BBC Earth', u'cs')], 'id': '0-bbc-earth','icon': [{'src': 'https://www.satelitnatv.sk//obrazky/loga_stanic/50/bbc_earth_50.png'}]})
        else:
            channels.append({'display-name': [('BBC Earth', u'cs')], 'id': '0-bbc-earth'})
        programmes2 = bbc()
        for y in programmes2:
            programmes.append(y)
        w = xmltv.Writer(encoding="utf-8", source_info_url="http://www.funktronics.ca/python-xmltv", source_info_name="Funktronics", generator_info_name="python-xmltv", generator_info_url="http://www.funktronics.ca/python-xmltv")
        for c in channels:
            w.addChannel(c)
        for p in programmes:
            w.addProgramme(p)
        w.write(download_path + addon.getSetting("file_name"), pretty_print=True)
        upload(notice)
    else:
        xbmcgui.Dialog().notification("365 EPG Grabber","Žádné vladtní kanály", xbmcgui.NOTIFICATION_ERROR, 4000, sound = False)
    sys.modules.clear()


def router():
    paramstring = sys.argv[0]
    if paramstring == "main.py":
        if addon.getSetting("notice") == "true":
            main(1)
        else:
            main(0)
    else:
        main(1)


if __name__ == '__main__':
    router()