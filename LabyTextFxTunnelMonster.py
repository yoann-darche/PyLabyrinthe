# -*- coding: utf-8 -*-

import LabyTextFxTunnel
import Entity
import SpriteIndex


__author__ = 'Yoann'

"""
    Ce package contient la définition de l'effet tunnel dans le labyrinthe pour les monstres uniquement
    
"""


class LTFxTunnelMonster(LabyTextFxTunnel.LTFxTunnel):

    def checkFX(self, ObjEntity, type, x=None, y=None):
    
    
    
        print("LTFxTunnelMonster::initFx::checkFX::Start")
        if type=='check': return True
        
        # Vérification de l'ordre et du type de l'entité
        if ((type!='apply') or (not isinstance(ObjEntity,Entity.Monster))) : 
            return (x,y)
            
        
        print("LTFxTunnelMonster::initFx::checkFX::Pass")
        
        return(LabyTextFxTunnel.LTFxTunnel.checkFX(self,ObjEntity,type,x,y))
        
    def renderFx(self, ObjGfx, dt):
        
        if self._hasChanged:
            for (x,y) in self.ExchangeSet:
                ObjGfx.addFxTile(x,y,SpriteIndex.SPRITE_TELEPORTEURMONSTER)
            self._hasChanged = False
        
            return True 