import time
import threading
from datetime import datetime
from dateutil import tz


class Ligne:
    "Object ligne pour l'affichage sur la matrice le LED"
    name="ligneDef"
    vitesse=1
    defil=-1
    x=5
    y=2
    h=2
    l=4
    color="FFFFFF"
    texte="500"

class Ecran:
    "Regroupe les paramètres pour un écran et de ses lignes"
    def __init__(self, name, time, actif):
        self.ligne = []
        self.name=name
        self.time=time
        self.actif=actif
    def addLigne(self, ligne):
        self.ligne.append(ligne)


class ModuleEcran (threading.Thread):
    "Module de gestion de l'écran"
    def __init__(self, debug):
        self.debug=debug
        self.scr = []
        if debug == 1:
            print("ModuleEcran : Start [mode:Debug]")
            print(self.__doc__)
        #Création des écrans
        E0 = Ecran("01",5,True)
        E0L1 = Ligne()
        E0.addLigne(E0L1)
        self.scr.append(E0)
        E1 = Ecran("02",1,True)
        E1L1 = Ligne()
        E1.addLigne(E1L1)
        self.scr.append(E1)
        #Thread
        if debug == 1:
            print("ModuleEcran : Thread init [mode:Debug]")
        threading.Thread.__init__(self)
        if debug == 1:
            print("ModuleEcran : Ready")


    def update(self, info):
        if self.debug == 1:
            print("ModuleEcran : Update :",info,"")
        self.scr[0].ligne[0].texte=str(info)
        self.scr[1].ligne[0].texte="LOL"
        # self.scr[1].actif=False


    def run(self):
        while 1:
            for scr_current in self.scr:
                if scr_current.time > 0 and scr_current.actif == True:
                    if self.debug == 1:
                        print("Ecran", scr_current.name)
                    for ligne_current in scr_current.ligne:
                        if self.debug == 1:
                            print("    ", scr_current.ligne[0].texte)
                            print("")
                    update(scr_current.ligne)
                    time.sleep(scr_current.time)


scr = ModuleEcran(1)
scr.start()
idx = 0
while 1:
    idx=idx+1
    scr.update(idx)
    time.sleep(8.0)
scr.stop()
