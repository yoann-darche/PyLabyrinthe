# -*- coding: utf-8 -*-

import LabyTextFx
import Entity


__author__ = 'Yoann'

"""
    Ce package contient la définition de l'effet BlackOut
    
"""


class LTFxBlackOut(LabyTextFx.LabyTextFx):
    

    def initFx(self, ObjLabyTxt, code):        
        
        LabyTextFx.LabyTextFx.initFx(self,ObjLabyTxt, code)
        
        self.BlackOutSet = set() # Set des aspirateur
        
        # Scan pour le caractère dans le labyrinthe
        
        # Pour chaque ligne du Labyrinthe
        for ly, ligne in enumerate(self._Map.CarteTxt):

            # Pour chaque colonne du Labyrinthe
            for lx, car in enumerate(ligne):
            
                if car == code:
                    
                    # Ajout du callBack
                    ObjLabyTxt._registerFxCb(self.checkFX, lx, ly)
                    self.BlackOutSet.add((lx,ly))
                    
        self._hasChanged = False
                            
        return True
        
    def checkFX(self, ObjEntity, type, x=None, y=None):
    
        if type=='check': return True
        
        # Vérification de l'ordre et du type de l'entité
        if ((type!='apply') or isinstance(ObjEntity,Entity.Monster)) : 
            return (x,y)
        
        self._Map.blackOut()
        self._Map.pushMessage("Eh Eh! J'ai éteind la lumière",3)
        self._Map.pushMessage("Bonne chance !",3)
                
        return (x,y)
        
        
    def renderFx(self, ObjGfx, dt):
                
        return True        
        
        
        
