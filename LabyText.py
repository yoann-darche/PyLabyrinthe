# -*- coding: utf-8 -*-

import json
import os

import LabyObjects

__author__ = 'Yoann'

"""
    Ce package contient la définition de la claasse LabyText, une classe dérivée de LabyObject
    implémentant le code exécutable pour la gestion d'un Labyrinthe en mode texte.
"""

import LabyTextFxTunnel
import LabyTextFxAspirateur
import LabyTextFxPorte
import LabyTextFxPorteEt
import LabyTextFxSensUnique
import LabyTextFxBlackOut
import LabyTextFxLightOn

class LabyText(LabyObjects.Laby):
    

    def initMap(self):
    
        # Propriété contenant la carte du labyrinthe encours
        self.CarteTxt = [
            "+-------+----------++-------+----------+",
            "T       |          ||       |          T",
            "+----+  |  -----+  |+----+  |  -----+  |",
            "|@   |          |  ||    |          |  |",
            "| +  +-----+    |  ||    |          |  |",
            "| |        |    |        |          |  |",
            "| +----+   +    +   |    |          |  |",
            "|      |            |    |          |  |",
            "+--+   +------------+   ++          |  |",
            "|      |            |TTT|        #  |  |",
            "+--+   |  +          TTT|       #   |  |",
            "|  |   +  |   +-----+TTT|           |  |",
            "|  |      |         +---++          |  |",
            "|  +------+-----+   |   |           |  |",
            "T               |   |   |           |  |",
            "|    +----+     +   |   |           |  |",
            "|    |       1      |               |  |",
            "|  +-+   +----------+    |          |  |",
            "|    |              |    |          | 0|",
            "+----+--------------+----+-------------+"]
            
        self.PlayerSponeCode = '@'
        self.MonsterSponeCode = '#'
    
    
    def _getLinkCode(self,x,y):
        """
        Cette fonction calcul le code de lien pour dessiner les mur en fonction
        des données de la carte (y compris les effets
        
        retourne None en cas d'echec ou le code sur 4 bit
        
        0x01 : >, 0x02: ^, 0x04: <, 0x08: _
        
        """
        
        code = 0
                
        # Vérifie les cases à proximité
        if x > 0: 
            c = self.CarteTxt[y][x-1]
            if ((c in ('|', '-', '+', 'Z')) or \
                ( (self.CarteFX[y][x-1] is not None) and self.FXList[c.upper()].gfxLinkFx(c) )):
                code = code | 0x04
            
        if x < self.LX-1:
            c = self.CarteTxt[y][x+1] 
            if ((c in ('|', '-', '+', 'Z')) or \
                ((self.CarteFX[y][x+1] is not None) and self.FXList[c.upper()].gfxLinkFx(c))):
                code = code | 0x01
            
        if y > 0: 
            c = self.CarteTxt[y-1][x]
            if ((c in ('|', '-', '+', 'Z')) or \
                ((self.CarteFX[y-1][x] is not None) and self.FXList[c.upper()].gfxLinkFx(c))):
                code = code | 0x02
            
        if y < self.LY-1:
            c = self.CarteTxt[y+1][x]
            if ((c in ('|', '-', '+', 'Z')) or \
                ((self.CarteFX[y+1][x] is not None) and self.FXList[c.upper()].gfxLinkFx(c))):
                code = code | 0x08
                
        return(code)
            
        
    
    def setDefault(self):
       
        # Initialisation des tableaux
        self.setLXLY(len(self.CarteTxt[0]), len(self.CarteTxt) )
        
        # Ajout des effets

        self._registerFx(LabyTextFxTunnel.LTFxTunnel(),'T')
        self._registerFx(LabyTextFxAspirateur.LTFxAspirateur(),'A')
                
        self._registerFx(LabyTextFxPorte.LTFxPorte(),'P')
        self._registerFx(LabyTextFxPorte.LTFxPorte(8),'Q')
        self._registerFx(LabyTextFxPorte.LTFxPorte(4),'R')
        self._registerFx(LabyTextFxPorteEt.LTFxPorteEt(0),'S')
        self._registerFx(LabyTextFxPorteEt.LTFxPorteEt(7),'U')
        
        
        self._registerFx(LabyTextFxSensUnique.LTFxSensUnique('N'),'^')
        self._registerFx(LabyTextFxSensUnique.LTFxSensUnique('S'),'_')
        self._registerFx(LabyTextFxSensUnique.LTFxSensUnique('O'),'<')
        self._registerFx(LabyTextFxSensUnique.LTFxSensUnique('E'),'>')
        
        
        
        self.NomLaby = "Labyrinthe par défaut"
        
        # Convertion du labyrinthe Text en format interne
        self._decodeTxtLaby()

        return None
        
        
    def loadJSON(self,fileName):
        """
        Cette fonction assure la lecture d'un fichier au format JSON
        """
        
        # Réinitialise le labyrinthe
        self.reInit()
        
        f = open(fileName, "r", encoding="utf8")
        
        data = json.load(f)
        
        self.CarteTxt         = data['Carte']
        try:
            self.CarteLight       = data['Light']
        except:
            self.CarteLight = None
            
        self.NomLaby          = data['NomLaby']
        self.FileName         = fileName
        self.Theme            = data['Theme']
        self.IsShadowEnabled  = data['IsShadowEnabled']
        self.MonsterSponeCode = data['MonsterSponeCode']
        self.PlayerSponeCode  = data['PlayerSponeCode']
        
        # Initialisation des tableaux
        self.setLXLY(len(self.CarteTxt[0]), len(self.CarteTxt) )
        
        # Charge les effets
        self._loadFXObject(data['FXList'])
        
        # Convertion du labyrinthe Text en format interne
        self._decodeTxtLaby()
        self._decodeTxtLight()
        

    def resetPermananteLigth(self, PermOnly = False):
        
        return self._decodeTxtLight(PermOnly)

    def _decodeTxtLaby(self):
        """
        Cette fonction assure le décodage du laby en format texte
        et initialise le format interne de LabyObjet
        """
        
        # Pour chaque ligne du Labyrinthe
        for ly, ligne in enumerate(self.CarteTxt):

            # Pour chaque colonne du Labyrinthe
            for lx, car in enumerate(ligne):
                
                if car == ' ':
                    self.Carte[ly*self.LX + lx] = 0
                elif car == self.PlayerSponeCode:
                    self.PlayerSponePlace.add((lx,ly))
                elif car == self.MonsterSponeCode:
                    self.MonsterSponePlace.add((lx,ly))
                elif car not in ('|', '-', '+', 'Z'):
                    self.Carte[ly*self.LX + lx] = 0
                else:
                    # Vérifie les cases à proximité
                    self.Carte[ly * self.LX + lx] = self._getLinkCode(lx,ly)
        
        self.__isValid = True
        
    def _loadFXObject(self, fxList):
        """
        Cette fonction à pour objectif de charger les effets
        à partir d'une liste
        """
        
        for afx in fxList:
            
            # get option if available
            if 'FXOptions' in afx.keys():
                options = afx['FXOptions']
            else:
                options = None
                
            mapCode = afx['MapCode']
            fxObject= afx['FXHandler']
            
            if fxObject == "LabyTextFxAspirateur.LTFxAspirateur":
                self._registerFx(LabyTextFxAspirateur.LTFxAspirateur(),mapCode)
                
            elif fxObject == "LabyTextFxTunnel.LTFxTunnel":
                self._registerFx(LabyTextFxTunnel.LTFxTunnel(),mapCode)
                
            elif fxObject == "LabyTextFxSensUnique.LTFxSensUnique":
                if options is None:
                    self._registerFx(LabyTextFxSensUnique.LTFxSensUnique(),mapCode)
                else:
                    self._registerFx(LabyTextFxSensUnique.LTFxSensUnique(**options),mapCode)
                
            elif fxObject == "LabyTextFxPorte.LTFxPorte":
                if options is None:
                    self._registerFx(LabyTextFxPorte.LTFxPorte(),mapCode)
                else:
                    self._registerFx(LabyTextFxPorte.LTFxPorte(**options),mapCode)
                
            elif fxObject == "LabyTextFxPorteEt.LTFxPorteEt":
                if options is None:
                    self._registerFx(LabyTextFxPorteEt.LTFxPorteEt(),mapCode)
                else:
                    self._registerFx(LabyTextFxPorteEt.LTFxPorteEt(**options),mapCode)
                    
            elif fxObject == "LabyTextFxBlackOut.LTFxBlackOut":
                if options is None:
                    self._registerFx(LabyTextFxBlackOut.LTFxBlackOut(),mapCode)
                else:
                    self._registerFx(LabyTextFxBlackOut.LTFxBlackOut(**options),mapCode)
                
            elif fxObject == "LabyTextFxLightOn.LTFxLightOn":
                if options is None:
                    self._registerFx(LabyTextFxLightOn.LTFxLightOn(),mapCode)
                else:
                    self._registerFx(LabyTextFxLightOn.LTFxLightOn(**options),mapCode)
        
    def _decodeTxtLight(self, PermOnly=False):
        """
        Cette fonction assure le décodage du laby en format texte
        et initialise le format interne de LabyObjet
        """
        
        if self.CarteLight is None:
            return
        
        # Pour chaque ligne du Labyrinthe
        for ly, ligne in enumerate(self.CarteLight):

            # Pour chaque colonne du Labyrinthe
            for lx, car in enumerate(ligne):
                
                if car == 'L':
                    self.updateLight(lx,ly)
                elif not(PermOnly) and car == 'T':
                    self.updateLight(lx,ly)
       

###
#   Test de la Classe
###

# Note: Cette partie du code ne sera exécutée que si il est appelée en exécution,
# mais pas si le fichier est importé. Ceci est pratique pour écrire des tests de Classe
if __name__ == "__main__":

    TestLaby = LabyText()

    (mx,my) = TestLaby.getSize()

    print("Création du labyrinthe <<{0}>>".format(TestLaby.NomLaby))

    print("La taille du Laby est {0}, {1}".format(mx,my))

    print("La carte est :")

    for i in TestLaby.Carte:
        print(i)

    # Couple de test
    testPos = [(0, 0), (45, 1), (1, 45), (-5, -5), (1, 1)]

    for i in testPos:
        x, y = i
        print("Test de la position x={0:3d}, y={1:3d}, => {2}".format(x, y, TestLaby.checkPos(x, y)))


