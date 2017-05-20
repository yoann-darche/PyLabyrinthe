# -*- coding: utf-8 -*-

import LabyObjects

__author__ = 'Yoann'

"""
    Ce package contient la définition de la claasse LabyText, une classe dérivée de LabyObject
    implémentant le code exécutable pour la gestion d'un Labyrinthe en mode texte.
"""

import LabyTextFxTunnel
import LabyTextFxPorte
import LabyTextFxPorteEt
import LabyTextFxSensUnique

class LabyText(LabyObjects.Laby):


    CarteTxt = []          # Propriété contenant la carte du labyrinthe encours

    def initMap(self):
    
        self.CarteTxt = [
            "+-------+----------++-------+----------+",
            "T       |          ||       |          T",
            "+----+  |  -----+  |+----+  |  -----+  |",
            "|    |          |  ||    |          |  |",
            "| +  +-----+    |  ||    |          |  |",
            "| |        |    |        |          |  |",
            "| +----+   +    +   |    |          |  |",
            "|      |            |    |          |  |",
            "+--+   +------------+   ++          |  |",
            "|      |            |TTT|           |  |",
            "+--+   |  +          TTT|           |  |",
            "|  |   +  |   +-----+TTT|           |  |",
            "|  |      |         +---++          |  |",
            "|  +------+-----+   |   |           |  |",
            "T               |   |   |           |  |",
            "|    +----+     +   |   |           |  |",
            "|    |       1      |               |  |",
            "|  +-+   +----------+    |          |  |",
            "|    |              |    |          | 0|",
            "+----+--------------+----+-------------+"]
    
    
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
            if ((c in ('|', '-', '+')) or \
                ( (self.CarteFX[y][x-1] is not None) and self.FXList[c.upper()].gfxLinkFx(c) )):
                code = code | 0x04
            
        if x < self.LX-1:
            c = self.CarteTxt[y][x+1] 
            if ((c in ('|', '-', '+')) or \
                ((self.CarteFX[y][x+1] is not None) and self.FXList[c.upper()].gfxLinkFx(c))):
                code = code | 0x01
            
        if y > 0: 
            c = self.CarteTxt[y-1][x]
            if ((c in ('|', '-', '+')) or \
                ((self.CarteFX[y-1][x] is not None) and self.FXList[c.upper()].gfxLinkFx(c))):
                code = code | 0x02
            
        if y < self.LY-1:
            c = self.CarteTxt[y+1][x]
            if ((c in ('|', '-', '+')) or \
                ((self.CarteFX[y+1][x] is not None) and self.FXList[c.upper()].gfxLinkFx(c))):
                code = code | 0x08
                
        return(code)
            
        
    
    def setDefault(self):
       
        # Initialisation des tableaux
        self.setLXLY(len(self.CarteTxt[0]), len(self.CarteTxt) )
        
        # Ajout des effets

        self._registerFx(LabyTextFxTunnel.LTFxTunnel(),'T')
                
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
        
        # Pour chaque ligne du Labyrinthe
        for ly, ligne in enumerate(self.CarteTxt):

            # Pour chaque colonne du Labyrinthe
            for lx, car in enumerate(ligne):
                
                if car == ' ':
                    self.Carte[ly*self.LX + lx] = 0
                elif car not in ('|', '-', '+'):
                    self.Carte[ly*self.LX + lx] = 0
                else:
                    # Vérifie les cases à proximité
                    self.Carte[ly * self.LX + lx] = self._getLinkCode(lx,ly)
                    
                #     if lx > 0: 
                #         c = ligne[lx-1]
                #         if ((c in ('|', '-', '+')) or \
                #            ( (self.CarteFX[ly][lx-1] is not None) and self.FXList[c.upper()].gfxLinkFx(c) )):
                #             code = code | 0x04
                #         
                #     if lx < self.LX-1:
                #         c = ligne[lx+1] 
                #         if ((c in ('|', '-', '+')) or \
                #            ((self.CarteFX[ly][lx+1] is not None) and self.FXList[c.upper()].gfxLinkFx(c))):
                #             code = code | 0x01
                #         
                #     if ly > 0: 
                #         c = self.CarteTxt[ly-1][lx]
                #         if ((c in ('|', '-', '+')) or \
                #            ((self.CarteFX[ly-1][lx] is not None) and self.FXList[c.upper()].gfxLinkFx(c))):
                #             code = code | 0x02
                #         
                #     if ly < self.LY-1:
                #         c = self.CarteTxt[ly+1][lx]
                #         if ((c in ('|', '-', '+')) or \
                #            ((self.CarteFX[ly+1][lx] is not None) and self.FXList[c.upper()].gfxLinkFx(c))):
                #             code = code | 0x08
                    
                #self.Carte[ly * self.LX + lx] = self._getLinkCode(lx,ly)
        
        
        self.__isValid = True

        return None

        

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


