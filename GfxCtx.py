
# -*- coding: utf-8 -*-
import tkinter as Tk
from tkinter.messagebox import askyesno
import tkinter.ttk as ttk
from PIL import Image, ImageDraw, ImageTk, ImageEnhance


# *****************************************************************************
# ** Classe du context Graphique, cette classe assure la création de la      **
# ** fenêtre graphique, et la gestion de ces propriétés et dimension.        **
# *****************************************************************************

class CtxGfx():


    def __init__(self, title='Le labyrinthe oufff & Connceté! - V0.x'):


        # taille des cases du labyrinthe x/y en pixel
        self.rx = 32
        self.ry = 32
        # Nb case
        self.nx = 20
        self.ny = 20
        
        # Objets graphiques        
        self.can = None
        

        # Message par défaut
        self._defaultMsg = title
        self._callbackID = None
        self.msgTimeToLive = 0

        self.fenetre = Tk.Tk()
        self.fenetre.config(bg="black")
        self.fenetre.title(title)
        
        # Mise au premier plan
        #self.fenetre.attributes('-fullscreen',1)
        #self.fenetre.overrideredirect(1)

        
        # capture de l'evt de la fenetre
        self.fenetre.protocol("WM_DELETE_WINDOW", self.quitter)
        self.fenetre.bind("<Escape>",self.quitter)
        
        # Tableau des monstres
        self.tkMonsterBoard = None
        self.tkMonsterBoardId = None

    def construitInterface(self):
        """
        Cette fonction se charge de la construction de l'interface
        :return:
        """
        # w = self.nx*self.rx
        w = 1200
        h = self.ny*self.ry
        
        # Création de la barre des infos
        self.cInfo = Tk.Canvas(self.fenetre, width=w, height=80, bd=0, bg='black', relief="flat")        
        self.cInfo.pack()
        
        # Création du context graphique pour l'affichage du labyrinthe
        self.can = Tk.Canvas(self.fenetre, width=w, height=h, bd=0, bg='black')        
        self.can.pack()

        
        
        x = (w - 240) // 2
        # Création de la liste des monstres
        self.monster_cadre = self.cInfo.create_rectangle(w - 2*x, 0, w-240, 40, fill='#4F0000', width=1, outline='#FFFFFF')
        
        # Création de la boite de message
        self.msg_cadre = self.cInfo.create_rectangle(w - 2*x, 41, w-240, 80, fill='#00007F', width=1, outline='#FFFFFF')
        
        self.cInfoMsg = self.cInfo.create_text(w // 2, 60, width=w-240, fill='white', 
                             text=self._defaultMsg, justify=Tk.LEFT, font=('Courrier', 20,))
      

        
    def resizeLabyCanvas(self,nx,ny):
        """
        Cette fonction est appelé pour mettre à jour la taille de l'espace du Labyrinthe
        """
        self.nx = nx
        self.ny = ny
        self.can.config(width=self.nx*self.rx, height=self.ny*self.ry)        
       
       
    def quitter(self, event=None):
        """
        Fonction appelé pour finir le programme, une confirmation est demandée avant
        """
        
        reponse = askyesno("Quitter le programme ?",
        "Voulez-vous réellement terminer ? \n cliquer <<oui>> pour finir")
        
        if reponse:
            self.fenetre.destroy()


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
        self.cInfo.itemconfig(self.cInfoMsg, text=message)     
        print("MSG: ",message)   
        self.msgTimeToLive = time
        

        
    def clearMessage(self):
        
        """
        Fonction appelée après n ms pour effacer le message
        """
        
        # Affiche le cadre des message        
        self.cInfo.itemconfig(self.cInfoMsg, text=self._defaultMsg)
        self.msgTimeToLive = -1
    
    def doUpdate(self,dt, LabyObj):
        """
        Fonction assurant la mise à jour de l'interface
        """        
        
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
                
                
    # **************************************************************************
    # **  Fonctions de gestion de l'affichage des montres.                    **
    # **************************************************************************
    
    def doMonsterStatus(self, MonsterList):
        """
        Fonction assurant l'affichage de l'état des monstres
        """
        
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
        
        self.TitleRect = self.can.create_rectangle(self.rx*2, 250, (self.rx*self.nx)-(self.rx*2), 350, 
                          fill='#004F00', width=2, outline='#FFFFFF')

        print("CtxGfx::doEndMapTitle: Yo")

        self.TitleMsg  = self.can.create_text( (self.nx*self.rx) // 2, 300, fill='white', 
                             text='Yeah, tous les monstres ont été maîtrisés',
                             font=('Courrier', 20))
                             
        print("CtxGfx::doEndMapTitle: Fin")
                             
        

    def doCleanMsg(self):
        
        self.clearMessage()
        self.can.delete(self.TitleRect)
        self.can.delete(self.TitleMsg)
        self.TitleRect =  None
        self.TitleMsg = None
        
        
        
    