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
        self.dataAPI = []
        self.lastData = 0
        self.infoCOnfig= ""
        self.mngAffichage = Affichage() ################################
        self.mngAffichage.start() ################################


        color1=graphics.Color(255, 255, 255)
        color2=graphics.Color(255, 255, 0)
        color3=graphics.Color(255, 255, 0)
        #Création de l'écran
        self.scrbus = Ecran("Bus",1,True)
        self.scrbus.addLigne(Ligne("Ville Arret",7,0,0,color1))#Titre
        self.scrbus.addLigne(Ligne("",14,0,0,color2))#ligne
        self.scrbus.addLigne(Ligne("",14,12,0,color2))#Destination
        self.scrbus.addLigne(Ligne("",14,50,0,color2))#Temps
        self.scrbus.addLigne(Ligne("",21,0,0,color2))
        self.scrbus.addLigne(Ligne("",21,12,0,color2))
        self.scrbus.addLigne(Ligne("",21,50,0,color2))
        self.scrbus.addLigne(Ligne("",29,0,0,color2))
        self.scrbus.addLigne(Ligne("",29,12,0,color2))
        self.scrbus.addLigne(Ligne("",29,50,0,color2))

        #Création de l'écran Bienvenu
        self.scrWelcome = Ecran("IP",10,False)
        self.scrWelcome.addLigne(Ligne("@IP : ",7,0,0,color2))
        self.scrWelcome.addLigne(Ligne(self.getIp(),14,0,0,color2))
        self.scrWelcome.addLigne(Ligne("v 0.5.2",21,0,0,color2))
        self.scrWelcome.addLigne(Ligne("SVNFTg==",29,0,0,color2))

        #Création de l'écran ERROR
        self.scrError = Ecran("Error",10,False)
        self.scrError.addLigne(Ligne("Error:",7,0,0,color2))
        self.scrError.addLigne(Ligne("Inconnu",14,0,0,color2))

        #Création de l'écran Attente Config
        self.scrWait = Ecran("Wait",10,False)
        self.scrWait.addLigne(Ligne("Wait Data",7,0,0,color2))
        self.scrWait.addLigne(Ligne("IP:",14,0,0,color2))
        self.scrWait.addLigne(Ligne("null ",21,0,0,color2))
        self.scrWait.addLigne(Ligne("$ ",29,0,0,color2))

        #Affichage sur l'écran
        self.mngAffichage.updateAff(self.scrWelcome) ################################
        # self.printScr(self.scrWelcome) ################################
        time.sleep(0.5)
        #Thread
        threading.Thread.__init__(self)

    def getIp(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
        return s.getsockname()[0]

    def conf(self, info):
        self.infoCOnfig=info
        self.scrbus.ligne[0].texte=str(info)

    def update(self, info):
        self.dataAPI=info
        self.lastData=time.time()
        if self.debug == 1:
            print("ModuleEcran : Update :",info,"")
            print("")

    # def printScr(self,scr):
    # 	if self.debug == 1:
    #         print("Ecran", scr.name, "nbLign:",len(scr.ligne))
    #         for ligne_current in scr.ligne:
    #             print("    ", ligne_current.texte)
    #         print("")

    def writeTime(self,actuel,futur):
        diffTime=float(futur-actuel)
        ret=""
        if diffTime <= 0:
            return "0m"
        else:
            h=diffTime/3600
            m=(diffTime-(int(h)*3600))/60
            hi=str(int(h))
            mi=str(int(m))
            if h >= 1:
                ret = hi+"h"+mi
            else:
                ret = mi+"m"
            return ret

    def run(self):
        while 1:
            #Gestion des données TODO
            # for in self.:
            #Gestion Affichage
            tisp = time.time()

            if self.lastData+3600 < tisp: # si les données sont trop ancien (plus de communication) 1h
                self.scrWait.ligne[2].texte=self.getIp()
                # self.printScr(self.scrWait)################################
                self.mngAffichage.updateAff(self.scrWait) )################################
            else:
                pasAff = []
                for pas in self.dataAPI:
                    print("=>",pas["ligne"], pas["terminus"],pas["temps"])
                    if len(pasAff) < 3 and float(pas["temps"]) > tisp:
                        pasAff.append(pas)
                    elif len(pasAff) >= 3:
                        break

                for idx in range(0,3):
                    if len(pasAff) > idx:
                        # self.scrbus.ligne[1+(idx*3)].texte="test"
                        # self.scrbus.ligne[2+(idx*3)].texte="test"
                        # self.scrbus.ligne[3+(idx*3)].texte="test"
                        self.scrbus.ligne[1+(idx*3)].texte=str(pasAff[idx]["ligne"])
                        self.scrbus.ligne[2+(idx*3)].texte=str(pasAff[idx]["terminus"])
                        self.scrbus.ligne[3+(idx*3)].texte=self.writeTime(tisp,float(pasAff[idx]["temps"]))
                    else:
                        self.scrbus.ligne[1+(idx*3)].texte=""
                        self.scrbus.ligne[2+(idx*3)].texte=""
                        self.scrbus.ligne[3+(idx*3)].texte=""

                if len(pasAff) == 0:
                    self.scrbus.ligne[1].texte="Pas de bus"

                # self.printScr(self.scrbus)################################
                self.mngAffichage.updateAff(self.scrbus) )################################
            print("refresh")
            time.sleep(5)




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
