# -*- coding: utf-8 -*-

import random
import LabyTextFx
import SpriteIndex


__author__ = 'Yoann'

"""
    Ce package contient la définition de l'effet tunnel dans le labyrinthe
    
"""


class LTFxTunnel(LabyTextFx.LabyTextFx):
    

    def initFx(self, ObjLabyTxt, code):   
    
        self.k = True
        
        LabyTextFx.LabyTextFx.initFx(self,ObjLabyTxt, code)
        
        # Stocke les coordonnées des points d'entrée et de sortie des tunnels
        self.ExchangeSet = set()  
        
        # Scan pour le caractère dans le labyrinthe
        
        # Pour chaque ligne du Labyrinthe
        for ly, ligne in enumerate(self._Map.CarteTxt):

            # Pour chaque colonne du Labyrinthe
            for lx, car in enumerate(ligne):
            
                if car == code:
                    self.ExchangeSet.add((lx,ly))
                    # Ajout du callBack
                    ObjLabyTxt._registerFxCb(self.checkFX, lx, ly)
                    
            self._hasChanged = True
                    
        print("LTFXTunnel::initFx::ExchangeSet[",code,"] = ", self.ExchangeSet)
             
        return True
        
    def checkFX(self, ObjPlayer, type, x=None, y=None):
    
        if type=='check': return True
        if type!='apply': return False
        
        # test du cas où il n'y a qu'une position
        l = len(self.ExchangeSet)
        if l < 2:
            return True
            
        print("LTFXTunnel::applyFX :: ExchangeSet ", self.ExchangeSet)
        print("LTFXTunnel::applyFX :: ObjPlayer::Pos ", (ObjPlayer.x, ObjPlayer.y))
        # retire de la liste la position actuelle
        TmpLst = list(self.ExchangeSet - {(ObjPlayer.x, ObjPlayer.y)})
        print("LTFXTunnel::applyFX :: TmpList ", TmpLst, "//", self.ExchangeSet)
                
        return(random.choice(TmpLst))
        
        
    def renderFx(self, ObjGfx, dt):
        
        if self._hasChanged:
            #if self.k:
                for (x,y) in self.ExchangeSet:
                    ObjGfx.addFxTile(x,y,SpriteIndex.SPRITE_TELEPORTEUR)
            #else:
            #    for (x,y) in self.ExchangeSet:
            #        ObjGfx.addFxTile(x,y,SpriteIndex.SPRITE_TRESOR)
                    
                self._hasChanged = False
            #print("LTFXTunnel::applyFX::rendered")
            #self.k = not(self.k)
            #print(self.k)
            
        
                return True 
        
        return False        
        
        
        
