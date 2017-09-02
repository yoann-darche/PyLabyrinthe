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
        self._ctxGfx = GfxCtx.CtxGfx("Labyrinthe d'Info@Leze V0.80a")
        self._ctxGfx.onNext = self._onNextMap
        self._ctxGfx.onReload = self._onReload
        
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
        
        self.mapList = [
            "./maps/Special.json",
            "./maps/litle.json", 
            "./maps/Intro_001.json",             
            "./maps/Learning.json", 
            "./maps/Default.json", 
            "./maps/FindTheWay.json",            
            "./maps/Phasor.json"]
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
        time = self._ctxGfx.doEndMapTitle()
        print("Time::", time)
        self._onNextMap()
        
        
    def _onNextMap(self):
        
        print("GameSession::_onNextMap")
        
        nextMap = self.mapList.pop()
        
        self.loadLaby(nextMap)
        self._ctxGfx.resizeLabyCanvas(self._labyObject.LX, self._labyObject.LY)
        self._entityMgr.reinitPlayer()
        self._entityMgr.reinitMonster()
        self._gfxRender.reInit()
        
    def _onReload(self):
        
        mapName = self._labyObject.FileName
        print("GameSession::_onReload")
        
        self.loadLaby(mapName)
        self._ctxGfx.resizeLabyCanvas(self._labyObject.LX, self._labyObject.LY)
        self._entityMgr.reinitPlayer()
        self._entityMgr.reinitMonster()
        self._gfxRender.reInit()        
        
        


# Vérification que nous sommes dans le programme principal
if __name__ == "__main__":

    SG = GameSession()
    
    SG.loadMapList()
    SG.loadFirstMap()
    SG.loadPlayer()
    SG.loadMonster()
    
    
    SG.mainLoop()


