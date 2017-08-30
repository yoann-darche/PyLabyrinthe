# -*- coding: utf-8 -*-

import GfxCtx
import GfxRender as Gfx
import LabyObjects as LabyObj
import LabyText as Laby
import Entity
import MonsterEngine

__author__ = 'Yoann'

"""
    Programme principal
"""



class GameSession():
    
    """
    Cette class matérialise une session de jeu, elle asssure la transition entre les niveaux (cartes)
    """
    
    def __init__(self):
    
        self.playListFile = None
        self._labyObject  = None
        self._gfxRender   = None
        self._entityMgr   = None
        
        # Création de la liste des Map
        self.mapList = []
        
        # Création du context Graphique
        self._ctxGfx = GfxCtx.CtxGfx()
        # Affichage de l'interface
        self._ctxGfx.construitInterface()
        
        # Création de l'objet labyrinthe        
        self._labyObject = Laby.LabyText()
        
        # initialise la liste des monstres
        self._entityMgr = Entity.EntityList(self._labyObject)        
        # Initialise le call back lorsque que tous les monstre sont mort
        self._entityMgr.OnFinish = self._labyObject.onAllMonsterDead
        
        # initialisation du graphisme
        self._gfxRender = Gfx.GfxRender(self._labyObject,self._entityMgr,self._ctxGfx)
        self._gfxRender.OnMapEnd = self._onMapEnd
    

    def loadMapList(self):
        
        self.mapList = ["./maps/BaseTest.json", "./maps/Default.json", "./maps/Gauntlet.json"]
        self.mapList.reverse()
        
    def loadLaby(self,LabyName):
        
        # charge le labyrinthe
        self._labyObject.loadJSON(LabyName)
        
        
    def loadMonster(self):
            
        # Ajout d'un monstre
        M = self._gfxRender.AddMonster('Simple', speed=0.5, pv=500)
        M.engine = MonsterEngine.MME_Basic
        M.moveToInitialPos()
        
        # Ajout d'un monstre
        M = self._gfxRender.AddMonster('More', speed=0.3, spriteFile="sprite/Hero/monster04.png", pv=500)
        M.engine = MonsterEngine.MME_Standard
        M.moveToInitialPos()
        
        # Ajout d'un monstre
        M = self._gfxRender.AddMonster('Flamiche', speed=0.2, spriteFile="sprite/Hero/flammiche.png", pv=1000)
        M.engine = MonsterEngine.MME_Foward
        M.moveToInitialPos()
        
        M = None
        
    def loadPlayer(self):
        
        # Ajout du premier joueur
        J1 = self._gfxRender.AddUser('John', pv=500)
        # Affectation des touches
        J1.bindKey({"N": "<Up>", "S": "<Down>", "O": "<Left>", "E": "<Right>"})
        # Positionnement du joueur
        J1.moveToInitialPos()
    
        # Ajout du second joueur
        J2 = self._gfxRender.AddUser('Melba', spriteFile='sprite/Hero/hero3.png', pv=500)
        # Affectation des touches
        J2.bindKey({"N": "z", "S": "s", "O": "q", "E": "d"})    
        J2.moveToInitialPos()
        
    def loadFirstMap(self):
        
        firstMap = self.mapList.pop()
        self.loadLaby(firstMap)
        self._ctxGfx.resizeLabyCanvas(self._labyObject.LX, self._labyObject.LY)
        self._gfxRender.reInit()
    

    def mainLoop(self):
        
        # Lancement de la boucle principal (boucle graphique)
        self._gfxRender.mainLoop()
        
        
    def _onMapEnd(self):
        
        # Call back utilisé pour détecté la fin d'une partie
        
        print("GameSession::_onMapEnd: On Map End !!!!!!!!!!!")
        self._ctxGfx.doEndMapTitle()
        self._onNextMap()
        
        
    def _onNextMap(self):
        
        print("GameSession::_onNextMap:: Start")
        
        nextMap = self.mapList.pop()
        
        self.loadLaby(nextMap)
        self._ctxGfx.resizeLabyCanvas(self._labyObject.LX, self._labyObject.LY)
        self._monsterMgr.reinitPlayer()
        self._monsterMgr.reinitMonster()
        self._gfxRender.reInit()
        
        


# Vérification que nous sommes dans le programme principal
if __name__ == "__main__":

    SG = GameSession()
    
    SG.loadMapList()
    SG.loadFirstMap()
    SG.loadPlayer()
    SG.loadMonster()
    
    
    SG.mainLoop()


   ##   print("Lancement du jeu de labyrinthe V0.70")

   ##   # Création du Labyrinthe
    # print("1/ Création du Labyrinthe ....")
    # #MonLaby = Laby.LabyText()
    # MonLaby = Laby.LabyText()
    # MonLaby.loadJSON('./maps/Entony2.json')
    # #MonLaby.setDefault()
    # 
    # # Création de la liste des monstres
    # MonsterMgr = LabyObj.MonsterList(MonLaby)
    # 
    # # Création du context Graphique
    # print("2/ Création de l'environnement Graphique")
    # LabyGfx = Gfx.GfxRender(MonLaby,MonsterMgr)

   ##   # Ajout du premier joueur
    # J1 = LabyGfx.AddUser('John', pv=500)
    # # Affectation des touches
    # J1.bindKey({"N": "<Up>", "S": "<Down>", "O": "<Left>", "E": "<Right>"})
    # # Positionnement du joueur
    # J1.moveToInitialPos()

   ##   # Ajout du second joueur
    # J2 = LabyGfx.AddUser('Melba', spriteFile='sprite/Hero/hero3.png', pv=500)
    # # Affectation des touches
    # J2.bindKey({"N": "z", "S": "s", "O": "q", "E": "d"})    
    # J2.moveToInitialPos()
    # 
    # 

   ##   
    # # Ajout d'un monstre
    # M = LabyGfx.AddMonster('AHRRR', speed=0.5, pv=500)
    # M.engine = MonsterEngine.MME_Basic
    # #M.setInitialPos(38,1)
    # M.moveToInitialPos()
    # 
    # # Ajout d'un monstre
    # M = LabyGfx.AddMonster('AHRRR2', speed=0.3, spriteFile="sprite/Hero/monster04.png", pv=500)
    # M.engine = MonsterEngine.MME_Standard
    # #M.setInitialPos(15,17)
    # M.moveToInitialPos()
    # 
    # # Ajout d'un monstre
    # M = LabyGfx.AddMonster('AHRRR3', speed=0.2, spriteFile="sprite/Hero/flammiche.png", pv=1000)
    # M.engine = MonsterEngine.MME_Foward
    # #M.setInitialPos(15,15)
    # M.moveToInitialPos()
    # 
    # M = None
    # 

   ##   # Première génération de l'affichage du Labyrinthe
    # LabyGfx.render(0)


  ###     
    # # Nettoyage
    # #LabyGfx = None
    # #MonLaby = None
    # 

