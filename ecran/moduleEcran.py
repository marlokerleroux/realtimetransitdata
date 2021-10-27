#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import threading
import time
from datetime import datetime
import socket
#from dateutil import tz

class Ligne:
    "Object ligne pour l'affichage sur la matrice le LED"
    def __init__(self, texte, x, y, align,color):
        self.color=color
        self.x=x #ligne
        self.y=y #col
        self.align=align
        self.texte=texte

class Ecran:
    "Regroupe les paramètres pour un écran et de ses lignes"
    def __init__(self, name, time, actif):
        self.ligne = []
        self.name=name
        self.time=time
        self.actif=actif
    def addLigne(self, ligne):
        self.ligne.append(ligne)


class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        #self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="")
        self.ligne = []

    def updateScr(self, scr_current):
        self.ligne.clear()
        for ligne_current in scr_current.ligne:
            self.ligne.append(ligne_current)
            # print(ligne_current.texte,ligne_current.x,ligne_current.y)


    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("/opt/projet/fonts/5x8.bdf")
        textColor = graphics.Color(250, 90, 205)

        while True:
            offscreen_canvas.Clear()
            for ligne_current in self.ligne:
                # if lig_current.align == 0:
                len = graphics.DrawText(offscreen_canvas, font, ligne_current.y, ligne_current.x , ligne_current.color, ligne_current.texte)
                # if lig_current.defil == 1:
                #     len = graphics.DrawText(offscreen_canvas, font, ligne_current.y, ligne_current.x+offset , ligne_current.color, ligne_current.texte)
                void drawPixel(uint16_t x, uint16_t y, uint16_t color);

            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

    def clear(self):
        offscreen_canvas.Clear()
        self.ligne.clear()

class Affichage (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.run_text = RunText()

    def updateAff(self, scr_current):
        self.run_text.updateScr(scr_current)

    def run(self):
        if (not self.run_text.process()):
            self.run_text.print_help()


class ModuleEcran (threading.Thread):
    "Module de gestion de l'écran"
    def __init__(self, debug):
        self.debug=debug
        self.mngAffichage = Affichage()
        self.mngAffichage.start()

        color1=graphics.Color(255, 255, 255)
        color2=graphics.Color(255, 255, 0)
        color3=graphics.Color(255, 255, 0)
        #Création de l'écran
        self.scrbus = Ecran("01",1,True)
        self.scrbus .addLigne(Ligne("Ville Arret",7,0,0,color1))#Titre
        self.scrbus .addLigne(Ligne("XX",14,0,0,color2))#ligne
        self.scrbus .addLigne(Ligne("Direction",14,12,0,color2))#Destination
        self.scrbus .addLigne(Ligne("5mn",14,50,0,color2))#Temps
        self.scrbus .addLigne(Ligne("XX",21,0,0,color2))
        self.scrbus .addLigne(Ligne("Direction",21,12,0,color2))
        self.scrbus .addLigne(Ligne("5mn",21,50,0,color2))
        self.scrbus .addLigne(Ligne("XX",29,0,0,color2))
        self.scrbus .addLigne(Ligne("Direction",29,12,0,color2))
        self.scrbus .addLigne(Ligne("5mn",29,50,0,color2))

        #Création de l'écran Bienvenu
        self.scrWelcome = Ecran("IP",10,False)
        self.scrWelcome.addLigne(Ligne("@IP : ",7,0,0,color2))
        self.scrWelcome.addLigne(Ligne(getIp(),14,0,0,color2))
        self.scrWelcome.addLigne(Ligne("v 0.5.2",21,0,0,color2))
        self.scrWelcome.addLigne(Ligne("SVNFTg==",29,0,0,color2))

        #Création de l'écran ERROR
        self.scrError = Ecran("Error",10,False)
        self.scrError.addLigne(Ligne("Error:",7,0,0,color2))
        self.scrError.addLigne(Ligne("Inconnu",14,0,0,color2))

        #Création de l'écran Attente Config
        self.scrWait = Ecran("Error",10,False)
        self.scrWait.addLigne(Ligne("Attente",7,0,0,color2))
        self.scrWait.addLigne(Ligne("IP:",14,0,0,color2))
        self.scrWait.addLigne(Ligne("$ ",21,0,0,color2))
        self.scrWait.addLigne(Ligne("$ ",29,0,0,color2))

        #Affichage sur l'écran
        self.mngAffichage.updateAff(self.scrWelcome)
        time.sleep(15)
        #Thread
        threading.Thread.__init__(self)

    def getIp():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
        return s.getsockname()[0]

    def update(self, info):
        self.dataAPI=info
        if self.debug == 1:
            print("ModuleEcran : Update :",info,"")

    def run(self):
        while 1:
            #Gestion des données TODO
            # for in self.:
            #Gestion Affichage
            for scr_current in self.scr:
                if scr_current.time > 0 and scr_current.actif == True:
                    # if self.debug == 1:
                    #     print("Ecran", scr_current.name)
                    # for ligne_current in scr_current.ligne:
                    #     if self.debug == 1:
                    #         print("    ", scr_current.ligne[0].texte)
                    #         print("")
                    # print("updateModule")
            self.mngAffichage.updateAff(self.scrbus)
            print("refresh")
            time.sleep(0.5)


# Main function
if __name__ == "__main__":
    dataSimu=[
{'ligne': '05', 'terminus': 'Port de Commerce', 'temps': '1635373166.0'},
{'ligne': '05', 'terminus': 'Provence', 'temps': '1635373036.0'},
{'ligne': '01', 'terminus': 'Gare', 'temps': '1635382396.0'},
{'ligne': '01', 'terminus': 'Hôpital Cavale', 'temps': '1635371271.0'}
]

    scr = ModuleEcran(1)
    scr.start()
    scr.conf("################")
    while 1:
        time.sleep(2.0)
        scr.update(dataSimu)
        time.sleep(28.0)
    scr.stop()
