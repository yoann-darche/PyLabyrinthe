# -*- coding: utf-8 -*-

import tkinter as Tk
from PIL import Image, ImageDraw, ImageTk, ImageEnhance
import os

import time

from Entity import Player, Monster


__author__ = 'Yoann'


    
# *****************************************************************************
# ** Classe dérivant du Player pour introduire les spécificité de l'affichage**
# ** en mode graphique.                                                      **
# *****************************************************************************

class GfxPlayer(Player):

    """
       Cette classe dérive de la classe Player afin de définir
       les methode et propriété pour l'affichage d'un joueur
       en mode graphique
    """

    def __init__(self, ctxGfx, initPv=100, spriteFile='sprite/Hero/hero.png'):
        """
        Fonction d'initialisation du Player mode Graphique
        :param gfxCtx: Context TK
        :param initPv: Point de vie Initial
        :param spriteFile: Fichier image représantant le joueur
        :return: NA
        """

        # Référence sur context graphique
        self._ctxGfx = ctxGfx

        Player.__init__(self,initPv)

        # Contient le sprite du joueur
        # self.Sprite = Tk.PhotoImage(file=spriteFile, master=self._ctxGfx.fenetre)
        self.Sprite = Image.open(spriteFile)
        self._img = None

        # Déclanche l'affichage
        self._hasChanged = True

    def __str__(self):
        """ Methode appelée lorsque que l'on utilise la fonction print() """
        return "P[{0} PV:{1}]".format(self.Name, self.PV)

    def bindKey(self, listKey):
        """
        :param listKey: Liste nommé des touche : { "N":"<Up>", "S":"<Down>", "O":"<Left>", "E":"<Right>" }
        :return: True/False
        """

        if self._ctxGfx is None:
            print("GfxPlayer:bindKey : Erreur pas de context graphique")
            return False

        # Ici, nous parcourrons le dictionaire pour associer les touches de dépalcement
        for k, i in listKey.items():
            self._ctxGfx.fenetre.bind(i, lambda event, o=self, ky=k: o.move(ky))

        return True

    def render(self, t):
        """
        Fonction assurant l'affichage du player
        :param t:
        :return:
        """

        if not self._hasChanged:
            return None

        if self._img is None:            
            self.tkSprite = ImageTk.PhotoImage(image=self.Sprite, master=self._ctxGfx.can)
            self._img = self._ctxGfx.can.create_image(self.x*self._ctxGfx.ry, self.y*self._ctxGfx.ry, anchor=Tk.NW,
                                                      image=self.tkSprite, tag='sprite')
        else:
            self._ctxGfx.can.coords(self._img, self.x*self._ctxGfx.ry, self.y*self._ctxGfx.ry)
            self._ctxGfx.can.tag_raise(self._img) 

        self._hasChanged = False

        return None

# *****************************************************************************
# ** Classe dérivant du Monster pour introduire les spécificités de          **
# ** l'affichage en mode graphique.                                          **
# *****************************************************************************

class GfxMonster(Monster):

    """
       Cette classe dérive de la classe Player afin de définir
       les methode et propriété pour l'affichage d'un joueur
       en mode graphique
    """

    def __init__(self, ctxGfx, speed=1000, initPv=100, spriteFile='sprite/Hero/monster.png'):
        """
        Fonction d'initialisation du Player mode Graphique
        :param gfxCtx: Context TK
        :param initPv: Point de vie Initial
        :param spriteFile: Fichier image représantant le joueur
        :return: NA
        """

        # Référence sur context graphique
        self._ctxGfx = ctxGfx

        Monster.__init__(self,speed,initPv)

        # Contient le sprite du joueur
        self.Sprite = Image.open(spriteFile)
        self._img = None

        # Déclanche l'affichage
        self._hasChanged = True
        

    def __str__(self):
        """ Methode appelée lorsque que l'on utilise la fonction print() """
        return "M[{0} PV:{1}]".format(self.Name, self.PV)


    def render(self, t):
        """
        Fonction assurant l'affichage du player
        :param t:
        :return:
        """

        if not self._hasChanged:
            return None

        if self._img is None:
            self.tkSprite = ImageTk.PhotoImage(image=self.Sprite, master=self._ctxGfx.can)
            if self.isVisible:               
                self._img = self._ctxGfx.can.create_image(self.x*self._ctxGfx.ry, self.y*self._ctxGfx.ry, anchor=Tk.NW,
                                                      image=self.tkSprite, tag='sprite')
            else:
                self._img = self._ctxGfx.can.create_image(self.x*self._ctxGfx.ry, self.y*self._ctxGfx.ry, anchor=Tk.NW,
                                                      image=self.tkSprite, tag='sprite', state=Tk.HIDDEN)
                            
        else:
            if self.isVisible:
                self._ctxGfx.can.itemconfig(self._img, state=Tk.NORMAL) 
            else:
                self._ctxGfx.can.itemconfig(self._img, state=Tk.HIDDEN) 
            
            self._ctxGfx.can.coords(self._img, self.x*self._ctxGfx.ry, self.y*self._ctxGfx.ry)
            self._ctxGfx.can.tag_raise(self._img) 
            

        self._hasChanged = False

        return None
        
    def kill(self):
        
        #print("GfxMonster::kill:tagList:",self._ctxGfx.can.find_all())
        if self._img is not None:
            self._ctxGfx.can.delete(self._img)
            self._img = None
        
        #self._ctxGfx.can.delete(self.Sprite)
        #self.Sprite = None
        
        # Appel de la fonction héritée
        Monster.kill(self)
        
        #print("GfxMonster::kill:tagList AFTER:",self._ctxGfx.can.find_all())

# **************************************************************************
# ** Classe qui s'occupe de la génération graphique du Labyrinthe         **
# **************************************************************************
class GfxRender():

    def __init__(self, laby, entityList, CtxGfx):
        
         
        # Initialisation du callback de mise à jour des IA
        self._OnUpdateCbk = None
        
        # Initialisation des variables locales
        self.lastTheme    = None    # theme du Labyrinthe chargé
        self.photo_wall_list = []   # Liste des images de mur
        self.photo_asset_list= []   # Liste des images d'objet
        self.photo_shadow_list=[]   # Liste des ombres
        self.photo_error = None     # Image Erreur
        self.photo_back  = None     # Image de fond

        self.plateau     = None     # Pillow image pour traitement rapide
        self.mapFx       = None
        self.tkPlateau   = None     # Objet Image tk
        self.tkPlateauId = None     # Id de l'objet tk        

        # Mémorisation de la référence sur l'objet de type Laby
        self._Map = laby
        self._EntityList = entityList
        self._ctxGfx = CtxGfx

        # Initialisation des ressources grafiques
        self._initGfx()
        

        # point référence temps
        self._lastTime  = time.time()
        
        # Call Back
        self.OnMapEnd = None
        
        
    def reInit(self):
        """
        Fonction utilisée lors du rechargement d'un Labyrinthe
        """
        
        # Mise à jour de la taille du Labyrinthe
        self._ctxGfx.nx = self._Map.LX
        self._ctxGfx.ny = self._Map.LY
        
        # Initialisation des ressources grafiques
        self._initGfx()        

        # point référence temps
        self._lastTime  = time.time()
        
        # Association de la call back Graphique
        self._ctxGfx.fenetre.after(1000, self.onUpdate)

    def _initGfx(self):
        """
        Recharge les ressource graphique associé au theme du Labyrinthe
        """
        
        if self.photo_error is None:
            self.photo_error = Image.open("sprite/Std/ErrorTile.png")
            
        if self.photo_back is None:
            self.photo_back  = Image.open("sprite/"+self._Map.Theme +"/background.png")
        
        
        if (self.lastTheme is None) or (self.lastTheme !=  self._Map.Theme):
        
            # Vide les liste actuelle
            self.photo_wall_list.clear()
            self.photo_asset_list.clear()
            self.photo_shadow_list.clear()
                    
            # Extraction des images mur
            photo_set = Image.open("sprite/"+self._Map.Theme +"/walls.png")
            for i in range(0,16) :
                img = photo_set.crop((i*self._ctxGfx.rx, 0, (i+1)*self._ctxGfx.rx, self._ctxGfx.ry))
                img.load()
                self.photo_wall_list.append(img)
                
                
            # Extraction des objets
            photo_set = Image.open("sprite/"+self._Map.Theme +"/assets.png")
            (w,h) = photo_set.size
            for i in range(0,w // self._ctxGfx.rx) :
                img = photo_set.crop((i*self._ctxGfx.rx, 0, (i+1)*self._ctxGfx.rx, self._ctxGfx.ry))
                img.load()
                self.photo_asset_list.append(img)     
                
            # Extraction des ombres        
            photo_set = Image.open("sprite/"+self._Map.Theme +"/shadows.png")
            (w,h) = photo_set.size
            for i in range(0,w // self._ctxGfx.rx) :
                img = photo_set.crop((i*self._ctxGfx.rx, 0, (i+1)*self._ctxGfx.rx, self._ctxGfx.ry))
                img.load()
                self.photo_shadow_list.append(img)    
                
            self.lastTheme = self._Map.Theme
            

    def mainLoop(self):
        
        # Association de la call back Graphique
        self._ctxGfx.fenetre.after(1000, self.onUpdate)
        
        self._ctxGfx.fenetre.mainloop()


    def AddUser(self, playerName, pv=100, spriteFile='sprite/Hero/hero.png'):
        """
            Créer et Ajoute un joueur dans le labyrinthe
        :param player: GfxPlayer
        :return: None
        """

        if self._ctxGfx is None:
            print("GfxRender:AddUser : Pas de context graphique initialisé !")
            return None

        #try:
        # Création du nouveau joueur (et de son contexte graphique)
        p = GfxPlayer(self._ctxGfx, initPv=pv, spriteFile=spriteFile)
        p.Name = playerName
        
        # Ajout dans la liste des joueurs
        self._EntityList.addPlayer(p)            

        return p
        #except e:
        #    return None
            
            
    def AddMonster(self, monsterName, speed=2, pv=5000, spriteFile='sprite/Hero/monster.png'):
        """
            Créer et Ajoute un monstre dans le labyrinthe
        :param 
        :return: None
        """

        if self._ctxGfx is None:
            print("GfxRender::AddMonster : Pas de context graphique initialisé !")
            return None

        try:
            # Création du nouveau joueur (et de son contexte graphique)
            p = GfxMonster(self._ctxGfx, speed, initPv=pv, spriteFile=spriteFile)
            p.Name = monsterName
            
            # Ajout dans la liste des joueurs
            self._EntityList.addMonster(p)
            
            return p
        except e:
            return None




    def renderMap(self):
        """
            Cette fonction s'occupe de la génération de l'image graphique
            Pour le moment elle intègre que la mise à jour du Laby et des Perso
        :return: None
        """
                
         
        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # %% Génération deu Labyrinthe %%
        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        # Dessine le fond
        
        self._ctxGfx.setDefaultMsg(self._Map.NomLaby)
        self._ctxGfx.showMessage('Bienvenu dans')
        

        self.plateau = Image.new('RGBA',(self._ctxGfx.nx * self._ctxGfx.rx, self._ctxGfx.ny * self._ctxGfx.ry), (255,255,255,255))
        
        (bw,bh) = self.photo_back.size

        (nbx, r) = divmod(self._ctxGfx.nx * self._ctxGfx.rx, bw)
        if r > 0: nbx += 1
        
        (nby, r) = divmod(self._ctxGfx.ny * self._ctxGfx.ry,bh)
        if r > 0: nby += 1
        
        for y in range(0,nby):
            for x in range(0,nbx):
                self.plateau.paste(self.photo_back,(x*bw, y*bh))                


        # Génération des murs

        # Pour chaque ligne du Labyrinthe
        for ly in range(0,self._ctxGfx.ny):

            # Pour chaque colonne du Labyrinthe
            for lx in range(0,self._ctxGfx.nx):

                # Est ce un Mur ?
                code = self._Map.Carte[ly * self._Map.LX + lx] & 0x0F
                
                #print("render::code (lx,ly) = (",lx, ",", ly, ")", code)
                if code != 0:
                    self.plateau.paste(self.photo_wall_list[code],(lx*self._ctxGfx.ry, ly*self._ctxGfx.ry))                
                            

    def renderFx(self, dt):
        """
        Fonction qui générent les modifications graphiques au dessus de la map  
        pour l'affichage des effets (porte, trésor, etc...)
        """
        
        if self.mapFx is None:
            self.mapFx = Image.new('RGBA',(self._ctxGfx.nx * self._ctxGfx.rx, self._ctxGfx.ny * self._ctxGfx.ry), (0,0,255,0))
        
        for k in self._Map.FXList:
            self._Map.FXList[k].renderFx(self, dt)
            
    def addFxTile(self,x,y,tileId):
        """
        Cette fonction est appelée par la classe LabyTextFx lors de la mise
        à jour graphique.
        """
        
        if tileId > len(self.photo_asset_list)-1:
            self.mapFx.paste(self.photo_error,(x*self._ctxGfx.ry, y*self._ctxGfx.ry))   
        else:
            self.mapFx.paste(self.photo_asset_list[tileId],(x*self._ctxGfx.ry, y*self._ctxGfx.ry))   
                
        return None

    def renderShadow(self):
        
        self.mapShadow = Image.new('RGBA',(self._ctxGfx.nx * self._ctxGfx.rx, self._ctxGfx.ny * self._ctxGfx.ry), (255,255,255,0))
        
        for x in range(0,self._ctxGfx.nx):
            for y in range(0,self._ctxGfx.ny):
                code = (self._Map.Carte[y * self._Map.LX + x] & 0xF0) >> 4
                code = code & 0x0F
                if code != 0x0F:
                    self.mapShadow.paste(self.photo_shadow_list[code],(x*self._ctxGfx.ry, y*self._ctxGfx.ry))
                
                
        
    def render(self, dt):
        """
        Fonction qui assure le mix des map pour générer l'image final
        """
        
        #self.mapFinal = Image.new('RGBA',(self._ctxGfx.nx * self._ctxGfx.rx, self._ctxGfx.ny * self._ctxGfx.ry), (0,0,0,255))
        
        # Vérifie si le plateau de base a été généré
        if self.plateau is None : self.renderMap()
        
        # calcule la couche dynamique (basé sur l'état des effets)
        self.renderFx(dt)
        
        self.mapFinal = Image.alpha_composite(self.plateau,self.mapFx)
        
        # Calcul l'éclairage
        if self._Map.IsShadowEnabled == True:            
            self.renderShadow()
            self.mapFinal = Image.alpha_composite(self.mapFinal,self.mapShadow)
                      
        
        # dump vers Tk
        #OldTkId = self.tkPlateauId
        
        
        self._ctxGfx.can.delete(self.tkPlateau) 
        self._ctxGfx.can.delete(self.tkPlateauId) 
        self.tkPlateau = ImageTk.PhotoImage(image=self.mapFinal,  master=self._ctxGfx.fenetre)
        self.tkPlateauId = self._ctxGfx.can.create_image(0, 0, anchor=Tk.NW, image=self.tkPlateau, state= Tk.NORMAL)
        self._ctxGfx.can.tag_lower(self.tkPlateauId) 
        
        
        
        
        
        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # %% Affichage des Persos      %%
        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        # Pour chaque perso
        for p in self._EntityList.ActivePlayerList:
            p.render(dt)
            
        # Pour chaque monstre
        for p in self._EntityList.ActiveMonsterList:
            p.render(dt)
        

    def onUpdate(self):
        """
            Fonction appeler régulièrement pour mettre à jour la position des joueurs
        :return:
        """

        # Récupère le point temps
        cur = time.time()
        # Calcule la différence
        dt = cur - self._lastTime


        # Mise à jour de l'interface
        self._ctxGfx.doUpdate(dt, self._Map)

        # Mise à jour des positions des monstres
        self._EntityList.updateMonster(dt)
        
        self._ctxGfx.doMonsterStatus(self._EntityList)
        
        # Appel du callback pour MAj de l'IA...
        try:
            self._OnUpdateCbk(dt)
        except:
            pass
        
        self.render(dt)


        # Mise à jour de la référence temporelle
        self._lastTime  = cur

        # Si la map n'est pas finit on continue, sinon on arrête
        if not self._Map.isFinished :    
            # Association de la call back Graphique
            self._ctxGfx.fenetre.after(50, self.onUpdate)
        else:
            try:
                self.OnMapEnd()
            except:
                pass
        
