# -*- coding: utf-8 -*-

import random
import LabyTextFx

import SpriteIndex


__author__ = 'Yoann'

"""
    Ce package contient la définition de l'effet porte on/off dans le labyrinthe
    
    Le code en minuscule correspond au/x bouton/s, en majuscule à la/les porte/s
    
"""


class LTFxSensUnique(LabyTextFx.LabyTextFx):


    def __init__(self, dir='N'):
        self.dir = dir # delais avant fermeture
        
        

    def initFx(self, ObjLabyTxt, code):
        
        """
        Initialise les données de fonctionnement de l'effet.
        """
                    
        LabyTextFx.LabyTextFx.initFx(self,ObjLabyTxt, code)
        
        self.FxSet = set()
        
        
        # Scan pour le caractère dans le labyrinthe
        
        # Pour chaque ligne du Labyrinthe
        for ly, ligne in enumerate(self._Map.CarteTxt):

            # Pour chaque colonne du Labyrinthe
            for lx, car in enumerate(ligne):
            
                if car == code:
                    # Ajout du callBack
                    self.FxSet.add((lx,ly))
                    ObjLabyTxt._registerFxCb(self.checkFX, lx, ly)
                    
            self._hasChanged = True
                            
             
        return True
        
    def checkFX(self, ObjPlayer, type, x=None, y=None):
    
        if type=='check':             
        
            if ObjPlayer.x == x:
                if  ObjPlayer.y > y and self.dir == 'N': return True
                if  ObjPlayer.y < y and self.dir == 'S': return True
                return False
            if ObjPlayer.y == y:
                if  ObjPlayer.x > x and self.dir == 'O': return True
                if  ObjPlayer.x < x and self.dir == 'E': return True
                return False
        else:
            
            ObjPlayer.setAllowedMove((self.dir))
            
            return((None,None))
        
        
    def renderFx(self, ObjGfx, dt):
        
        
        if self._hasChanged:
            
            if self.dir == 'N': 
                tileId = SpriteIndex.SPRITE_SENSU_N
            elif self.dir == 'O': 
                tileId = SpriteIndex.SPRITE_SENSU_O
            elif self.dir == 'S': 
                tileId = SpriteIndex.SPRITE_SENSU_S
            elif self.dir == 'E': 
                tileId = SpriteIndex.SPRITE_SENSU_E
                        
            for (x,y) in self.FxSet:                
                ObjGfx.addFxTile(x,y,tileId)
                
                
            self._hasChanged = False
        
        return True        
        
    def gfxLinkFx(self, car=None):

        return True
        
        
        
