
# -*- coding: utf-8 -*-
#import tkinter as Tk
#from tkinter.messagebox import askyesno
#import tkinter.ttk as ttk
#from PIL import Image, ImageDraw, ImageTk, ImageEnhance

# Std import
import sys, time

# Specific import
import pygame
from pygame.locals import *

FPS = 60

# *****************************************************************************
# ** Classe du context Graphique, cette classe assure la création de la      **
# ** fenêtre graphique, et la gestion de ces propriétés et dimension.        **
# *****************************************************************************

class CtxGfx():


    def __init__(self, title='Le labyrinthe oufff & Connceté! - V0.x'):

        # taille de la fenête
        self.WIDTH = 1200
        self.HEIGHT = 800

        # taille des cases du labyrinthe x/y en pixel
        self.rx = 32
        self.ry = 32
        # Nb case
        self.nx = 20
        self.ny = 20
        
        # Callback
        self.onNext = None
        self.onReload = None        
    
        # Objets graphiques        
        self.can = None
        

        # Message par défaut
        self._defaultMsg = title
        self._callbackID = None
        self.msgTimeToLive = 0
        
        # EndMapTitle
        self.msgEndTitle = 0
        self.TitleRect =  None
        self.TitleMsg = None  
        self.SessionTime = 0      


        # initialisation de pyGame
        pygame.init()
        

        self.FPSCLOCK = pygame.time.Clock()
        
        self.fenetre = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption(title)
        
        #self.fenetre = self._fenetre.convert_alpha()
        self.fenetre.fill((0,128,0))
                
        # Tableau des monstres
        #self.tkMonsterBoard = None
        #self.tkMonsterBoardId = None


    def quitter(self, event=None):
        """
        Fonction appelé pour finir le programme, une confirmation est demandée avant.
        (AFR)
        """
        
        #reponse = askyesno("Quitter le programme ?",
        #"Voulez-vous réellement terminer ? \n cliquer <<oui>> pour finir")
        
        #if reponse:
        #    self.fenetre.destroy()
        
        pygame.quit()
        sys.exit()
        

    def construitInterface(self):
        """
        Cette fonction se charge de la construction de l'interface
        :return:
        """

        h = self.ny*self.ry
        
        # Création de la barre des infos
        self.cInfo = pygame.Surface((self.WIDTH,80))
        #self.cInfo = Tk.Canvas(self.fenetre, width=w, height=80, bd=0, bg='black', relief="flat")        
        #self.cInfo.pack()
        
        # Création du context graphique pour l'affichage du labyrinthe
        self.can = pygame.Surface((self.WIDTH,self.HEIGHT))
        
        #self.can = Tk.Canvas(self.fenetre, width=w, height=h, bd=0, bg='black')        
        #self.can.pack()

        
        
        x = (self.WIDTH - 240) // 2
        # Création de la liste des monstres
        self.monster_cadre = pygame.draw.rect(self.cInfo,(79, 0, 0), [self.WIDTH - 2*x, 41, self.WIDTH-240, 80])
       
        
        # Création de la boite de message
        self.msg_cadre = pygame.draw.rect(self.cInfo,(79, 0, 0), [self.WIDTH - 2*x, 41, self.WIDTH-240, 80])
        
        
        self.fontInfo = pygame.font.Font('freesansbold.ttf', 20)
        self.cInfoMsg = self.fontInfo.render(self._defaultMsg, True, (255,255,255), (0,0,0))
        self.fontTime = pygame.font.Font('freesansbold.ttf', 30)
        self.cTimeMsg = self.fontTime.render('0000.0', True, (0,255,255))
        
       # self.cInfoMsg = self.cInfo.create_text(w // 2, 60, width=w-240, fill='white', 
       #                      text=self._defaultMsg, justify=Tk.LEFT, font=('Courrier', 20,))
                             
       # self.cTimeMsg =  self.cInfo.create_text(w-70,40, width=240, fill='#00FFFF', text='0000.0', justify=Tk.RIGHT, font=('Courrier',30))
      

        
    def resizeLabyCanvas(self,nx,ny):
        """
        Cette fonction est appelé pour mettre à jour la taille de l'espace du Labyrinthe
        """
        self.nx = nx
        self.ny = ny
        
        self.margeX = (self.WIDTH - self.nx*self.rx) // 2
        if self.margeX < 0: self.margeX = 0
        
        self.margeY = (self.HEIGHT - self.ny*self.ry) // 2
        if self.margeY < 0: self.margeY = 0
        
        self.canRect = pygame.Rect(self.margeX, self.margeY, self.nx*self.rx, self.ny*self.ry)

        
        self.SessionTime = time.time()
       

    # #########################################################################
    # #                      Boucle principale                               ##
    # #########################################################################
       
    def mainLoop(self,gfxRender):
        
        """
        Boucle principale graphique
        """
        
        while True:
            
            # Gestion des évènement
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                
                # Gestion des touches relachées (commandes)
                if event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        self.quitter()
                    elif event.key == K_n:
                        self.doNext(event)
                    elif event.key == K_r:
                        self.doReload(event)
                     
                # Gestion des touches enfoncées (evt clavier)
                if event.type == KEYDOWN:
                    self._mgrKeyDown(event)
                    
            # Appel de la mise à jour du graphisme Labyrinthe
            gfxRender.onUpdate()
    
            # Appel de la boucle graphique de pyGame
            pygame.display.update()
            self.FPSCLOCK.tick(FPS)



    # **************************************************************************
    # ** Fonctions de gestion des evénèments claviers                         **
    # **************************************************************************
    
    def _mgrKeyDown(self,envent):
        
        pass
        
    




    # **************************************************************************
    # **  Fonctions de gestion de l'affichage des messages.                   **
    # **************************************************************************
        
    def setDefaultMsg(self, msg):
        
        self._defaultMsg = msg
        
        
    def showMessage(self, message, time=5):
        """
        Cette fonction assure l'affichage du message pendant time ms
        """                
        
        # Affiche le cadre des message        
       # self.cInfo.itemconfig(self.cInfoMsg, text=message)     
        print("MSG: ",message)   
        self.msgTimeToLive = time
        

        
    def clearMessage(self):
        
        """
        Fonction appelée après n ms pour effacer le message
        """
        
        # Affiche le cadre des message        
        # self.cInfo.itemconfig(self.cInfoMsg, text=self._defaultMsg)
        self.msgTimeToLive = -1
    
    def doUpdate(self,dt, LabyObj):
        """
        Fonction assurant la mise à jour de l'interface
        """        
        
        # Gestion du EndTitle
        if self.msgEndTitle > 0:
            self.msgEndTitle -= dt
            if self.msgEndTitle <= 0:
                self.doCleanEndMapTitle()
                self.msgEndTitle = 0
        
        
        # Gestion des messages
        if self.msgTimeToLive > 0:
            self.msgTimeToLive -= dt
            if self.msgTimeToLive <= 0:
                if LabyObj.countMessage() == 0:
                    self.clearMessage()
            elif (self.msgTimeToLive > 2) and (LabyObj.countMessage() > 0):
                self.msgTimeToLive = 2
        else:
            (m,t) = LabyObj.popMessage()
            if m is not None:
                self.showMessage(m,t)
                
        # Affichage du Temps
        u = "{0:0>4.1f}".format(time.time()-self.SessionTime)
        #print(">", u)
        #self.cInfo.itemconfig(self.cTimeMsg, text=u) 
                
                
    # **************************************************************************
    # **  Fonctions de gestion de l'affichage des montres.                    **
    # **************************************************************************
    
    def doMonsterStatus(self, MonsterList):
        """
        Fonction assurant l'affichage de l'état des monstres
        """
        
        return None
        
        # Si pas de changement exit direct
        if not(MonsterList.hasUpdate): return None
        
        print("CtxGfx::doMonsterStatus >> Doing")
        MonsterList.hasUpdate = False
        
        w = self.nx*self.rx
        
        nb_total = len(MonsterList.ActiveMonsterList) + len(MonsterList.InActiveMonsterList)
        
        w_monster = nb_total * (self.rx + 2)
        
        x_offset = (self.nx*self.rx - w_monster) // 2
        
        # Création du tableau des monstres
        
        monsterBoard = Image.new('RGBA',(w_monster, 40), (0,0,255,0)) 
                
        k = 0
        for m in MonsterList.ActiveMonsterList:            
            monsterBoard.paste(m.Sprite,(k*(self.rx + 2), 4))
            k = k+1
    
        for m in MonsterList.InActiveMonsterList:
            tmpSprite = ImageEnhance.Color(m.Sprite)
            monsterBoard.paste(tmpSprite.enhance(0.0),(k*(self.rx + 2), 4))
            k = k+1
          
        self.cInfo.delete(self.tkMonsterBoard) 
        self.cInfo.delete(self.tkMonsterBoardId) 
        self.tkMonsterBoard = ImageTk.PhotoImage(image=monsterBoard,  master=self.cInfo)
        self.tkMonsterBoardId = self.cInfo.create_image(x_offset, 0, anchor=Tk.NW, image=self.tkMonsterBoard, state= Tk.NORMAL)
        
        
        
    def doEndMapTitle(self):
        """
        Fonction qui affiche la fin de la Map
        """
            
        print("CtxGfx::doEndMapTitle: Début")
        
        if self.TitleRect is None:
            
            self.msgEndTitle = 5
        
            self.TitleRect = self.can.create_rectangle(self.rx*2, 250, (self.rx*self.nx)-(self.rx*2), 350, 
                          fill='#004F00', width=2, outline='#FFFFFF')

            self.TitleMsg  = self.can.create_text( (self.nx*self.rx) // 2, 300, fill='white', 
                             text='Yeah, tous les monstres ont été maîtrisés',
                             font=('Courrier', 20))
                             
        return(time.time() - self.SessionTime)
                             
        

    def doCleanEndMapTitle(self):
                
        self.can.delete(self.TitleRect)
        self.can.delete(self.TitleMsg)
        self.TitleRect =  None
        self.TitleMsg = None
        
        
        
    # #########################################################################
    # #                      Ecran d'acceuil                                 ##
    # #########################################################################
    
    def startScreen(self):
        
        imgBackground = pygame.image.load('./res/startScreen/background.png')
        rectBackground = imgBackground.get_rect()
        
        rectBackground.centery = self.HEIGHT // 2
        rectBackground.centerx = self.WIDTH // 2
        
        
        self.fenetre.fill(0)
        
        self.fenetre.blit(imgBackground, rectBackground)
        
        # Boucle principal pour l'écran d'acceuil.
        while True: 
            for event in pygame.event.get():
                                
                
                if event.type == QUIT:
                    self.quitter()
                elif event.type == KEYDOWN:
                    # une touche a été appuyée
                    if event.key == K_ESCAPE:
                        self.quitter()
                    return 
                elif event.type == MOUSEBUTTONDOWN :
                    return
                    

            # Affiche l'écran
            pygame.display.update()
            self.FPSCLOCK.tick()
        
        
    # **************************************************************************
    # ** Callnacks diverses
    # **************************************************************************
    
    def doNext(self, event):
        
        try:
            self.onNext()
        except:
            pass
            
    def doReload(self, event):
        
        try:
            self.onReload()
        except:
            pass
        
        
        
    