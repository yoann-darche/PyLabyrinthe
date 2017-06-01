# -*- coding: utf-8 -*-

import random
import LabyTextFx
import Entity


__author__ = 'Yoann'

"""
    Ce package contient la définition de l'aspirateur à Monstre
    
"""


class LTFxAspirateur(LabyTextFx.LabyTextFx):
    

    def initFx(self, ObjLabyTxt, code):        
        
        LabyTextFx.LabyTextFx.initFx(self,ObjLabyTxt, code)
        
        self.AspirSet = set() # Set des aspirateur
        
        # Scan pour le caractère dans le labyrinthe
        
        # Pour chaque ligne du Labyrinthe
        for ly, ligne in enumerate(self._Map.CarteTxt):

            # Pour chaque colonne du Labyrinthe
            for lx, car in enumerate(ligne):
            
                if car == code:
                    
                    # Ajout du callBack
                    ObjLabyTxt._registerFxCb(self.checkFX, lx, ly)
                    self.AspirSet.add((lx,ly))
                    
        self._hasChanged = True
                            
        return True
        
    def checkFX(self, ObjEntity, type, x=None, y=None):
    
        if type=='check': return True
        
        # Vérification de l'ordre et du type de l'entité
        if ((type!='apply') or (not isinstance(ObjEntity,Entity.Monster))) : 
            return (x,y)
        
        ObjEntity.kill()
        self._Map.removeMonster(ObjEntity)
        self._Map.pushMessage("Yes ! un monstre de moins....",3)
        self._Map.pushMessage("Bye Bye " + ObjEntity.Name,3)
                
        return (-1,-1)
        
        
    def renderFx(self, ObjGfx, dt):
        
        if self._hasChanged:
            for (x,y) in self.AspirSet:
                ObjGfx.addFxTile(x,y,15)
                
            self._hasChanged = False
        
        return True        
        
        
        
