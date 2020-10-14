import wx
import re
import time
import requests
import threading
from bs4 import BeautifulSoup
from win10toast import ToastNotifier

toaster = ToastNotifier()

items_dict = {
    'TemperingAlloy':   'https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?ItemID=5687&SortBy=LastSeen&Order=desc',
    'CornFlower':   'https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?ItemID=511&SortBy=LastSeen&Order=desc',
    'PotentNirncrux':  'https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?ItemID=3790&SortBy=LastSeen&Order=desc',
    'FleshflyLarva':   'https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?ItemID=&ItemNamePattern=larva&SortBy=LastSeen&Order=desc',
    'Mastic':   'https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?ItemID=&ItemNamePattern=mastic&SortBy=LastSeen&Order=desc',
    'RawAncestorSilk':  'https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?ItemID=&ItemNamePattern=Raw+Ancestor+Silk&SortBy=LastSeen&Order=desc',
    'Rosin':   'https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?ItemID=2677&SortBy=LastSeen&Order=desc',
    'Kuta':   'https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?ItemID=1114&SortBy=LastSeen&Order=desc',
    'PlatinumDust':   'https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?ItemID=18023&ItemNamePattern=Platinum+Dust&SortBy=LastSeen&Order=desc'
}


def check_items():
    global items_dict
    for item in items_dict:
        check_item(item)


def notificate(name, price):
    toaster.show_toast("İndirim : " + name, name +
                       "'s price is : " + str(price), icon_path='.\\icon.ico')


def check_item(item):
    global items_dict
    r = requests.get(items_dict[item])
    response = r.text
    soup = BeautifulSoup(response, "lxml")
    items_tr = soup.findAll("tr", {"class": "cursor-pointer"})
    for item_tr in items_tr:
        item_tr = str(item_tr).replace(' ', '').replace('\r', '')
        price_regex = re.search(
            r'<imgclass="small-icon"src="/Content/icons/gold.png"/>\n(.*)\n\n<divclass="text-danger">', item_tr).group(1)
        price_regex = str(price_regex).replace(',', '')
        price_regex = float(price_regex)
        # print(item, '   kontrol ediliyor    :   ', items_dict[item], '  =>  ', price_regex)
        if item == 'TemperingAlloy' and price_regex <= float(3100):
            notificate(item, price_regex)
        elif item == 'CornFlower' and price_regex <= float(450):
            notificate(item, price_regex)
        elif item == 'PotentNirncrux' and price_regex <= float(15.500):
            notificate(item, price_regex)
        elif item == 'FleshflyLarva' and price_regex <= float(21):
            notificate(item, price_regex)
        elif item == 'Mastic' and price_regex <= float(490):
            notificate(item, price_regex)
        elif item == 'RawAncestorSilk' and price_regex <= float(40):
            notificate(item, price_regex)
        elif item == 'Rosin' and price_regex <= float(2000):
            notificate(item, price_regex)
        elif item == 'Kuta' and price_regex <= float(1850):
            notificate(item, price_regex)
        elif item == 'PlatinumDust' and price_regex <= float(66):
            notificate(item, price_regex)
    time.sleep(0.25)


def onBaslatButton(event):
    global durumLabel
    global durum
    durumLabel.SetLabel("Çalışıyor.")
    durum = True


def onDurdurButton(event):
    global durumLabel
    global durum
    durumLabel.SetLabel("Çalıştırmak için Tıklayınız")
    durum = False


durum = False


def onExit(event):
    global frame, app
    app.Destroy()
    exit()


def guiThreadDef():
    global frame, app, durumLabel
    app = wx.App()
    frame = wx.Frame(None, -1, 'Bot')
    frame.SetSize(400, 250)
    frame.Bind(wx.EVT_CLOSE, onExit)
    panel = wx.Panel(frame, wx.ID_ANY)

    baslatButton = wx.Button(panel, id=wx.ID_ANY, label="Başlat")
    baslatButton.Bind(wx.EVT_BUTTON, onBaslatButton)
    baslatButton.SetPosition((20, 150))

    durdurButton = wx.Button(panel, id=wx.ID_ANY, label="Durdur")
    durdurButton.Bind(wx.EVT_BUTTON, onDurdurButton)
    durdurButton.SetPosition((290, 150))

    durumLabel = wx.StaticText(
        panel, -1, "align center", (100, 50), (160, -1), wx.ALIGN_CENTER)
    durumLabel.SetBackgroundColour("pink")
    durumLabel.SetLabel("Çalıştırmak için Tıklayınız")

    frame.Show()
    frame.Centre()
    app.MainLoop()


def botThreadDef():
    global durum
    while True:
        if durum != False:
            check_items()
            time.sleep(65)
        time.sleep(5)


botThread = threading.Thread(target=botThreadDef)
botThread.setDaemon(True)
botThread.start()
guiThreadDef()
