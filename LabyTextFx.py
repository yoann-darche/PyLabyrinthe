# -*- coding: utf-8 -*-

__author__ = 'Yoann'

"""
    Ce package contient la définition de la classe Modèle pour le codage des
    effets/evènements qui arrivent aux joueurs dans le labyrinthe.
    Par exemple les portes, les trappes, les tunnels etc..
"""

class LabyTextFx():



    def initFx(self,ObjLabyTxt, code):
        """
        Cette fonction à pour objectif d'initialiser l'effet en analysant la
        carte du labyrinthe, lancer en début de partie
        
        :param: ObjLabyTxt référence sur l'objet LabyText
        :param: code caractère utilisé dans le labyrinthe (ou list de code)
        
        """
        self._hasChanged = False # Indique si une mise à jour Gfx est nécessaire
        self._Map = ObjLabyTxt
        
        return None
    
    
    def checkFX(self, ObjPlayer, type, x=None, y=None):
        """
        Cette fonction à pour objectif de vérifier que l'effet s'applique bien
        au joueur dans se context
        
        si type = 'check' : Vérification uniquement, retourne true/false
        si type = 'apply' : Applique l'effet, retourne (none,none) si pas de 
           modification de la position du player, sinon sa nouvelle position (x,y)
                
        """
        
        if type == "check": return True
        
        return (None,None)
        
        
    def updateFX(deltaTime):
        """
        Fonction qui assure le mise à jour de l'effet temporellement
        """
        
        return True
    
    def renderFx(self, ObjGfx, dt):
        """
        Fonction qui assure la mise à jour de la map dynamique
        param: dt correspond delta time
        """
        
        return True
        
    def gfxLinkFx(self, car=None):
        """
        Fonction qui retourne Vrai quand lien graphique
        """
        
        return False
         

