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
        self.scr = []
        self.mngAffichage = Affichage()
        self.mngAffichage.start()
        if debug == 1:
            print("ModuleEcran : Start [mode:Debug]")
            print(self.__doc__)
        color1=graphics.Color(255, 255, 255)
        color2=graphics.Color(255, 255, 0)
        color3=graphics.Color(255, 255, 0)
        #Création de l'écran
        E0 = Ecran("01",1,True)
        E0.addLigne(Ligne("Ville Arret",7,0,0,color1))#Titre
        E0.addLigne(Ligne("XX",14,0,0,color2))#ligne
        E0.addLigne(Ligne("Direction",14,14,0,color2))#Destination
        E0.addLigne(Ligne("5mn",14,50,0,color2))#Temps
        E0.addLigne(Ligne("XX",21,0,0,color2))
        E0.addLigne(Ligne("Direction",21,14,0,color2))
        E0.addLigne(Ligne("5mn",21,50,0,color2))
        E0.addLigne(Ligne("XX",29,0,0,color2))
        E0.addLigne(Ligne("Direction",29,14,0,color2))
        E0.addLigne(Ligne("5mn",29,50,0,color2))
        self.scr.append(E0)
        #Création de l'écran @ip pendant 10sec
        E1 = Ecran("IP",10,False)
        E1.addLigne(Ligne(getIp(),0,0,0,color2))
        self.scr.append(E1)
        #Affichage sur l'écran
        self.mngAffichage.updateAff(E1)
        time.sleep(15)
        #Thread
        threading.Thread.__init__(self)

    def getIp():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
        return s.getsockname()[0]

    def update(self, info):
        if self.debug == 1:
            print("ModuleEcran : Update :",info,"")
        self.scr[0].ligne[1].texte=str(info)
        # self.scr[1].ligne[0].texte="LOL"
        # self.scr[1].actif=False

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
                    self.mngAffichage.updateAff(scr_current)
                    time.sleep(scr_current.time)

# Main function
if __name__ == "__main__":
    scr = ModuleEcran(1)
    scr.start()
    idx = 0
    print (getIp())
    while 1:
        idx=idx+1
        # bus=api.req(arartbus)
        scr.update(idx)
        time.sleep(8.0)
    scr.stop()
