# -*- coding: utf-8 -*-

import random
import LabyTextFx


__author__ = 'Yoann'

"""
    Ce package contient la définition de l'effet porte on/off dans le labyrinthe
    
    Le code en minuscule correspond au/x bouton/s, en majuscule à la/les porte/s
    
"""


class LTFxPorteEt(LabyTextFx.LabyTextFx):


    def __init__(self, closeTime=0):
        self.closeTime = closeTime # delais avant fermeture
        
        

    def initFx(self, ObjLabyTxt, code):
        
        """
        Initialise les données de fonctionnement de l'effet.
        Un lettre capital designe la porte
        Un lettre non capital désigne le déclancheur
        param: closeTime correspond à un delais avant fermeture automatique
        """
        
        self.DoorSet = dict()  # Stocke les coordonnées des portes
                              # Trio (x,y,sens) ou sens = V ou H pour 
                              # différentier les porte Horizontal et Vertical
        self.TrigSet = dict()  # Stocke les coordonnées des boutons
                              # Trio (x,y,actif) ou actif = appuyé ou pas
        
        self.PorteOuverte = False # Indique si la porte est ouverte ou fermée
        
        
        self.lastTime  = 0         # compteur délais
    
        LabyTextFx.LabyTextFx.initFx(self,ObjLabyTxt, code)
        
        CODE = code.upper()
        code = code.lower()
        
        # Scan pour le caractère dans le labyrinthe
        
        # Pour chaque ligne du Labyrinthe
        for ly, ligne in enumerate(self._Map.CarteTxt):

            # Pour chaque colonne du Labyrinthe
            for lx, car in enumerate(ligne):
            
                if car == code:
                    self.TrigSet[(lx,ly)] = False
                    # Ajout du callBack
                    ObjLabyTxt._registerFxCb(self.checkFX, lx, ly)
                elif car == CODE:
                    chk = self._Map._getLinkCode(lx,ly)
                    print("LTFxPorteEt:initFx::",lx,ly,chk)
                    if chk & 0x05 == 0x05:
                        self.DoorSet[(lx,ly)]='V'
                    else:
                        self.DoorSet[(lx,ly)]='H'
                    # Ajout du callBack
                    ObjLabyTxt._registerFxCb(self.checkFX, lx, ly)
                
                    
        self._hasChanged = True
                            
             
        return True
        
    def checkFX(self, ObjPlayer, type, x=None, y=None):
    
        if type=='check': 
            if (x, y) in self.TrigSet: return True
            if (x, y) in self.DoorSet: return self.PorteOuverte
            print("LTFxPorteEt::checkFX(check) -- No found (",x,y,")")
            return False
            
        
        # test le cas où le joueur active un trigger
        
        x = ObjPlayer.x
        y = ObjPlayer.y
        print("LTFxPorteEt::checkFX(apply) :: Porte= ",self.PorteOuverte)
        print("Pos:",x,y," Set:",self.TrigSet)
        
        if (x,y) in self.TrigSet:
            v = self.TrigSet[(x,y)]
            
            if self.closeTime > 0:
                if v : 
                    # Cas où le trigger est déjà activé ==> reset du time
                    self.lastTime  = 0
                    print("LTFxPorteEt::checkFX(apply) :: Trigger déjà activé !")
                    return (None,None)
                else:
                    # Cas où il y a activation
                    self.TrigSet[(x,y)] = True
                    self._hasChanged = True
                    self.lastTime  = 0
            else:
                # Mode bascule
                self.TrigSet[(x,y)] = not v
                self._hasChanged = True
                
            # Cacul l'état de la porte
            if False in self.TrigSet.values():
                if self.PorteOuverte:
                    self.PorteOuverte = False
                    self._hasChanged = True
            else:
                if not self.PorteOuverte:
                    self.PorteOuverte = True
                    self._hasChanged = True
            
            print("LTFxPorteEt::checkFX(apply) :: Porte= ",self.PorteOuverte)
                
        return((None,None))
        
        
    def renderFx(self, ObjGfx, dt):
        
        self.lastTime  = self.lastTime + dt
        #print("LTFxPorte::renderFx :: dt=",self.lastTime," maxtime=",self.closeTime)
        
        if self.PorteOuverte and self.closeTime > 0 and self.closeTime < self.lastTime: 
            self._hasChanged = True
            self.PorteOuverte = False   
            for (x,y) in self.TrigSet:
                self.TrigSet[(x,y)] = False
            self.lastTime = 0
        
        if self._hasChanged:
            
            print("LTFxPorteEt::renderFx .... ")
            
            if(self.PorteOuverte): 
                trigId_True = 14
                trigId_False = 14
                doorH = 3
                doorV = 7
            else: 
                trigId_True = 13
                trigId_False = 12
                doorH = 2
                doorV = 6
            
            
            for (x,y) in self.TrigSet: 
                if self.TrigSet[(x,y)]:
                    ObjGfx.addFxTile(x,y,trigId_True)
                else:
                    ObjGfx.addFxTile(x,y,trigId_False)
                
            for (x,y) in self.DoorSet:   
                if self.DoorSet[(x,y)] == 'H':
                    ObjGfx.addFxTile(x,y,doorH)
                else:
                    ObjGfx.addFxTile(x,y,doorV)
                
            self._hasChanged = False
        
        return True        
        
    def gfxLinkFx(self, car=None):
        
        if car.islower(): return False
        
        return True
        
        
        
