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
        self.defil=0
        self.defilOffset=0# defilement mode 1
        self.strCurrent=""
        self.strAff=""
        self.texte=texte
        self.font=graphics.Font()
        self.font.LoadFont("/opt/projet/fonts/5x8.bdf")
    def changeFont(self,str):
        self.font.LoadFont(str)

    def setAlign(self,arg):
        self.defil=arg

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

    def defilement(self,strAff):
        nouvelle_chaine=strAff
        # nouvelle_chaine=nouvelle_chaine[-1]+nouvelle_chaine[0:-1]
        nouvelle_chaine=nouvelle_chaine[1:(len(strAff))]+nouvelle_chaine[0]
        return nouvelle_chaine


    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        # font = graphics.Font()
        # font.LoadFont("/opt/projet/fonts/5x8.bdf")

        while True:
            offscreen_canvas.Clear()
            for ligne_current in self.ligne:
                if ligne_current.defil == 0:
                    size = graphics.DrawText(offscreen_canvas, ligne_current.font, ligne_current.y, ligne_current.x , ligne_current.color, ligne_current.texte)
                elif ligne_current.defil == 1:
                    texteScr=ligne_current.texte
                    ligne_current.defilOffset-=2
                    if (len(ligne_current.texte)*5) > (12*6):
                        texteScr+="   "
                    if ligne_current.defilOffset < ((len(texteScr)*5)*-1):
                        ligne_current.defilOffset=0
                    offset=(12*6)+ligne_current.defilOffset
                    if offset > 0:
                        offset=0
                    size = graphics.DrawText(offscreen_canvas, ligne_current.font, ligne_current.y+offset, ligne_current.x , ligne_current.color, texteScr)
                elif ligne_current.defil == 2:
                    if ligne_current.texte != ligne_current.strCurrent:
                        ligne_current.strAff=ligne_current.texte
                        ligne_current.strCurrent=ligne_current.texte
                    ligne_current.strAff=self.defilement(ligne_current.strAff)
                    size = graphics.DrawText(offscreen_canvas, ligne_current.font, ligne_current.y, ligne_current.x , ligne_current.color, ligne_current.strAff[0:7])

                #     len = graphics.DrawText(offscreen_canvas, font, ligne_current.y, ligne_current.x+offset , ligne_current.color, ligne_current.texte)
            time.sleep(0.4)
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
        self.scrbus.addLigne(Ligne("",7,0,0,color1))#Titre
        self.scrbus.ligne[0].setAlign(1)
        self.scrbus.addLigne(Ligne("",14,0,0,color2))#ligne
        self.scrbus.addLigne(Ligne("",14,12,0,color2))#Destination
        self.scrbus.addLigne(Ligne("",14,49,0,color2))#Temps
        self.scrbus.addLigne(Ligne("",22,0,0,color2))
        self.scrbus.addLigne(Ligne("",22,12,0,color2))
        self.scrbus.addLigne(Ligne("",22,49,0,color2))
        self.scrbus.addLigne(Ligne("",30,0,0,color2))
        self.scrbus.addLigne(Ligne("",30,12,0,color2))
        self.scrbus.addLigne(Ligne("",30,49,0,color2))

        #Création de l'écran Bienvenu
        self.scrWelcome = Ecran("IP",10,False)
        self.scrWelcome.addLigne(Ligne("@IP : ",7,0,0,color2))
        self.scrWelcome.addLigne(Ligne(self.getIp(),14,0,0,color2))
        self.scrWelcome.addLigne(Ligne("v 0.5.2",21,0,0,color2))
        self.scrWelcome.addLigne(Ligne("SVNFTg==",29,0,0,color2))
        self.scrWelcome.ligne[1].changeFont("/opt/projet/fonts/4x6.bdf")

        #Création de l'écran ERROR
        self.scrError = Ecran("Error",10,False)
        self.scrError.addLigne(Ligne("Error:",7,0,0,color2))
        self.scrError.addLigne(Ligne("Inconnu",14,0,0,color2))

        #Création de l'écran Attente Config
        self.scrWait = Ecran("Wait",10,False)
        self.scrWait.addLigne(Ligne("Wait Data",7,0,0,color2))
        self.scrWait.addLigne(Ligne("",14,0,0,color2))
        self.scrWait.addLigne(Ligne("",21,0,0,color2))
        self.scrWait.addLigne(Ligne("",29,0,0,color2))

        #Affichage sur l'écran
        self.mngAffichage.updateAff(self.scrWelcome) ################################
        # self.printScr(self.scrWelcome) ################################
        time.sleep(2)
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
                ret = ">1h"
            else:
                if m < 10:
                    ret = "0"+mi+"m"
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
                #self.scrWait.ligne[2].texte=self.getIp()
                # self.printScr(self.scrWait)################################
                self.mngAffichage.updateAff(self.scrWait) ################################
            else:
                pasAff = []
                for pas in self.dataAPI:
                    #print("=>",pas["ligne"], pas["terminus"],pas["temps"])
                    if len(pasAff) < 3 and float(pas["temps"]) > tisp:
                        pasAff.append(pas)
                    elif len(pasAff) >= 3:
                        break

                for idx in range(0,3):
                    if len(pasAff) > idx:
                        self.scrbus.ligne[1+(idx*3)].texte=str(pasAff[idx]["ligne"])[0:2]
                        self.scrbus.ligne[2+(idx*3)].texte=str(pasAff[idx]["terminus"])
                        if len(pasAff[idx]["terminus"]) > 7:
                            self.scrbus.ligne[2+(idx*3)].texte+=" "
                            self.scrbus.ligne[2+(idx*3)].defil=2
                        else:
                            self.scrbus.ligne[2+(idx*3)].defil=0
                        self.scrbus.ligne[3+(idx*3)].texte=self.writeTime(tisp,float(pasAff[idx]["temps"]))[0:3]
                    else:
                        self.scrbus.ligne[1+(idx*3)].texte="  "
                        self.scrbus.ligne[2+(idx*3)].texte="  "
                        self.scrbus.ligne[3+(idx*3)].texte="  "

                if len(pasAff) == 0:
                    self.scrbus.ligne[1].texte="Pas de bus"

                # self.printScr(self.scrbus)################################
                self.mngAffichage.updateAff(self.scrbus)################################
            #print("refresh")
            time.sleep(5)
