# -*- coding: utf-8 -*-

import random
import LabyTextFx


__author__ = 'Yoann'

"""
    Ce package contient la définition de l'effet porte on/off dans le labyrinthe
    
    Le code en minuscule correspond au/x bouton/s, en majuscule à la/les porte/s
    
"""


class LTFxPorte(LabyTextFx.LabyTextFx):


    def __init__(self, closeTime=0):
        self.closeTime = closeTime # delais avant fermeture
        
        

    def initFx(self, ObjLabyTxt, code):
        
        """
        Initialise les données de fonctionnement de l'effet.
        Un lettre capital designe la porte
        Un lettre non capital désigne le déclancheur
        param: closeTime correspond à un delais avant fermeture automatique
        """
        
        self.DoorSet = set()  # Stocke les coordonnées des portes
                              # Trio (x,y,sens) ou sens = V ou H pour 
                              # différentier les porte Horizontal et Vertical
        self.TrigSet = set()  # Stocke les coordonnées des boutons
        
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
                    self.TrigSet.add((lx,ly))
                    # Ajout du callBack
                    ObjLabyTxt._registerFxCb(self.checkFX, lx, ly)
                elif car == CODE:
                    chk = self._Map._getLinkCode(lx,ly)
                    print("LTFxPorte:initFx::",lx,ly,chk)
                    if chk & 0x05 == 0x05:
                        self.DoorSet.add((lx,ly,'V'))
                    else:
                        self.DoorSet.add((lx,ly,'H'))
                    # Ajout du callBack
                    ObjLabyTxt._registerFxCb(self.checkFX, lx, ly)
                
                    
            self._hasChanged = True
                            
             
        return True
        
    def checkFX(self, ObjPlayer, type, x=None, y=None):
    
        if type=='check': 
            if (x, y) in self.TrigSet: return True
            if ((x, y, 'H') in self.DoorSet) or ((x, y, 'V') in self.DoorSet): return self.PorteOuverte
            print("LTFxPorte::checkFX(check) -- No found (",x,y,")")
            return False
            
        
        # test du cas où il n'y a qu'une position
        if (ObjPlayer.x, ObjPlayer.y) in self.TrigSet:
            
            if self.closeTime > 0:
                self.lastTime  = 0
                if not self.PorteOuverte: 
                    self.PorteOuverte = True
                    self._hasChanged = True
            else:
                self.PorteOuverte = not self.PorteOuverte
                self._hasChanged = True
            
            print("LTFxPorte::checkFX(apply) :: Porte= ",self.PorteOuverte)
                
        return((None,None))
        
        
    def renderFx(self, ObjGfx, dt):
        
        self.lastTime  = self.lastTime + dt
        #print("LTFxPorte::renderFx :: dt=",self.lastTime," maxtime=",self.closeTime)
        
        if self.closeTime > 0 and self.closeTime < self.lastTime: 
            self._hasChanged = self.PorteOuverte
            self.PorteOuverte = False            
            self.lastTime = 0
        
        if self._hasChanged:
            
            if(self.PorteOuverte): 
                trigId = 5
                doorH = 3
                doorV = 7
            else: 
                trigId = 4
                doorH = 2
                doorV = 6
            
            
            for (x,y) in self.TrigSet:                
                ObjGfx.addFxTile(x,y,trigId)
                
            for (x,y, S) in self.DoorSet:   
                print("LTFxPorte::renderFx",x,y,S)
                if S == 'H':
                    ObjGfx.addFxTile(x,y,doorH)
                else:
                    ObjGfx.addFxTile(x,y,doorV)
                
            self._hasChanged = False
        
        return True        
        
    def gfxLinkFx(self, car=None):
        
        if car.islower(): return False
        
        return True
        
        
        
