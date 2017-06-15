# -*- coding: utf-8 -*-

import GfxRender as Gfx
import LabyObjects as LabyObj
import LabyText as Laby
import MonsterEngine

__author__ = 'Yoann'

"""
    Programme principal
"""


# Vérification que nous sommes dans le programme principal
if __name__ == "__main__":

    print("Lancement du jeu de labyrinthe V0.70")

    # Création du Labyrinthe
    print("1/ Création du Labyrinthe ....")
    #MonLaby = Laby.LabyText()
    MonLaby = Laby.LabyText()
    MonLaby.loadJSON('./maps/FindTheWay.json')
    #MonLaby.setDefault()
    
    # Création de la liste des monstres
    MonsterMgr = LabyObj.MonsterList(MonLaby)
    
    # Création du context Graphique
    print("2/ Création de l'environnement Graphique")
    LabyGfx = Gfx.GfxRender(MonLaby,MonsterMgr)

    # Ajout du premier joueur
    J1 = LabyGfx.AddUser('John', pv=500)
    # Affectation des touches
    J1.bindKey({"N": "<Up>", "S": "<Down>", "O": "<Left>", "E": "<Right>"})
    # Positionnement du joueur
    J1.moveToInitialPos()

    # Ajout du second joueur
    J2 = LabyGfx.AddUser('Melba', spriteFile='sprite/Hero/hero3.png', pv=500)
    # Affectation des touches
    J2.bindKey({"N": "z", "S": "s", "O": "q", "E": "d"})    
    J2.moveToInitialPos()
    
    

    
    # Ajout d'un monstre
    M = LabyGfx.AddMonster('AHRRR', speed=0.5, pv=500)
    M.engine = MonsterEngine.MME_Basic
    #M.setInitialPos(38,1)
    M.moveToInitialPos()
    
    # Ajout d'un monstre
    M = LabyGfx.AddMonster('AHRRR2', speed=0.3, spriteFile="sprite/Hero/monster02.png", pv=500)
    M.engine = MonsterEngine.MME_Standard
    #M.setInitialPos(15,17)
    M.moveToInitialPos()
    
    # Ajout d'un monstre
    M = LabyGfx.AddMonster('AHRRR3', speed=0.2, spriteFile="sprite/Hero/flammiche.png", pv=1000)
    M.engine = MonsterEngine.MME_Foward
    #M.setInitialPos(15,15)
    M.moveToInitialPos()
    
    M = None
    

    # Première génération de l'affichage du Labyrinthe
    LabyGfx.render(0)

    # Lancement de la boucle principal (boucle graphique)
    LabyGfx.mainLoop()
    
    # Nettoyage
    #LabyGfx = None
    #MonLaby = None
    

