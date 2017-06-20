# -*- coding: utf-8 -*-

import LabyTextFx
import Entity

import SpriteIndex


__author__ = 'Yoann'

"""
    Ce package contient la définition de l'effet LightOn
    Cela permet d'afficher tout le labyrinthe (en option avec un temps limite)
    
"""


class LTFxLightOn(LabyTextFx.LabyTextFx):
    

    def __init__(self, delay=0):
        self.delay = delay # delais avant fermeture
        
    def initFx(self, ObjLabyTxt, code):        
        
        LabyTextFx.LabyTextFx.initFx(self,ObjLabyTxt, code)
        
        self.LigthOnSet = set() # Set des aspirateur
        
        # Scan pour le caractère dans le labyrinthe
        
        # Pour chaque ligne du Labyrinthe
        for ly, ligne in enumerate(self._Map.CarteTxt):

            # Pour chaque colonne du Labyrinthe
            for lx, car in enumerate(ligne):
            
                if car == code:
                    
                    # Ajout du callBack
                    ObjLabyTxt._registerFxCb(self.checkFX, lx, ly)
                    self.LigthOnSet.add((lx,ly))
                    
        self.cumul = -1
        
        self._hasChanged = True
        print("LTFxLightOn::initFx done, nb trigger =", len(self.LigthOnSet))
                            
        return True
        
    def checkFX(self, ObjEntity, type, x=None, y=None):
    
        if type=='check': return True
        
        # Vérification de l'ordre et du type de l'entité
        if ((type!='apply') or isinstance(ObjEntity,Entity.Monster)) : 
            return (x,y)
        
        print("LTFxLightOn::checkFX : Allume le labyrinthe")
        
        self._Map.showAll()   

        if self.delay > 0: self.cumul = 0     
                
        return (x,y)
        
        
    def renderFx(self, ObjGfx, dt):
                
        if self.delay > 0 and self.cumul >= 0:
            self.cumul += dt
            if self.cumul > self.delay:
                self._Map.blackOut()
                self.cumul = -1
        
        if self_hasChnaged :
            for (x,y) in self.LigthOnSet: 
                ObjGfx.addFxTile(x,y,SpriteIndex.SPRITE_LIGTHON)
        
        return True        
        
        
        
