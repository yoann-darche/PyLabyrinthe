# -*- coding: utf-8 -*-

import random

__author__ = 'Yoann'

"""
    Unité qui regroupe les différent moteur calculant le déplacement
    d'un monstre.
    
    prototype def <MonMonsterEngine> ( self, dt)
"""


def MME_Standard(self, dt):
    """
    Déplacement basé sur une direction disponnible au hazard, si pas bon
    prendre la direction par défaut
    """
        
    directions = self.OnAvlDir(self.x,self.y)
    
    hasMoved = False
    
#  if self.lastDir in directions:
#      directions.remove(self.lastDir)
#      hasMoved = self.move(self.lastDir)
    
    if directions == []:
        return None
        
    while(hasMoved == False):
        a = random.choice(directions)
        hasMoved = self.move(a)
        
        if hasMoved == False:
            directions.remove(a)
            
            if self.lastDir in directions:
                directions.remove(self.lastDir)
                hasMoved = self.move(self.lastDir)
            elif len(directions) == 0:
                self.moveToInitialPos()
                hasMoved = True


def MME_Foward(self, dt):
    """
    Déplacement basé sur une direction disponnible au hazard, si pas bon
    prendre la direction par défaut
    """
        
    directions = self.OnAvlDir(self.x,self.y)
    
    hasMoved = False
    
    if self.lastDir in directions:
        directions.remove(self.lastDir)
        hasMoved = self.move(self.lastDir)
    
    if directions == []:
        return None
        
    while(hasMoved == False):
        a = random.choice(directions)
        hasMoved = self.move(a)
        
        if hasMoved == False:
            directions.remove(a)
            
            if self.lastDir in directions:
                directions.remove(self.lastDir)
                hasMoved = self.move(self.lastDir)
            elif len(directions) == 0:
                self.moveToInitialPos()
                hasMoved = True

                
def MME_Basic(self,dt):
    """
    Déplacement basé sur une direction disponnible au hazard
    """
        
    directions = self.OnAvlDir(self.x,self.y)
    hasMoved = False
    
    if directions == []:
        return None
        
    while(hasMoved == False):
        a = random.choice(directions)
        hasMoved = self.move(a)
        
        if hasMoved == False:
            directions.remove(a)
            
        if len(directions) == 0:
            self.moveToInitialPos()
            hasMoved = True                
        
        