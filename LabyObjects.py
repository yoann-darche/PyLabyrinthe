__author__ = 'Yoann'

"""
Ce module regroupe tous le code concernant la gestion d'un labyrinthe

   Class Laby : Classe principale gérant la logique du labyrinthe
   Class MonsterList : Gère les montres et leur évolution
   Class GameSession : Gère la logique de création d'une partie
   
"""

import random

import Entity
import LabyTextFx

class Laby():
    """
    Cette objet est une méta classe (une classe modèle)
    qui regroupe toutes les définitions des fonctions logiques
    nécessaires à l'utilisation de la carte du Labyrinthe
    """
    


    def __init__(self):
        """
        Constructeur de Classe: Cette fonction lance l'initialisation de l'objet.
        
        :param fileName: Nom du fichier à charger
        :return: instance de Classe
        """


        self.NomLaby = ''        # Nom du Labyrinthe
        self.FileName = ''       # Nom du fichier
        self.Theme = "Gray"      # Theme graphique du labyrinthe
        self.LX = -1             # Largeur du Labyrinthe
        self.LY = -1             # Hauteur du Labyrinthe
        
        self.Carte = None        # byte array du labyrinthe
        self.CarteEntity = []    # Recense la position des joueurs (et monstres)
        self.CarteFX = []        # Recense les effets dynamiques
        
        self.IsShadowEnabled = False # Desactivation de la fonction calcul d'ombre
        self.IsShadowUpdated = False # Indique si une évolution sur les ombres à eu lieu
        
        self.PlayerSponePlace = set()  # Ensemble des positions d'apparition
        self.MonsterSponePlace = set()  # Ensemble des positions d'apparition
                
        self.PlayerList = []     # Liste des joueurs        
        self.FXList = {}         # Liste des effets LabyTextFx
        self.MsgList = []        # Liste des messages à afficher
        
        
        self.OnFinish = None     # CallBack utilisé pour indiquer la fin de partie
        
        self.isFinished  = False # Inidcateur que la partie est fini ou pas
        
    
        # Propriétés d'état de la classe
        self.__isValid = False
                        
        

    def loadFromFile(self, Source):
        """
        Function assurant le chargement d'une carte de Labyrinthe depuis un fichier
        :param Source: chemin complet pour atteindre le fichier
        :return: true/false
        """
        return False

    def setDefault(self):
        """
        Cette fonction créer un labyrinthe de test par défaut
        :return None:
        """
        return None
        
        
    def setLXLY(self,mLX,mLY):
        """
        Cette fonction définit la taille logique du labyrinthe
        et initailise la carte logique des joueurs/monstres
        """
        self.LX = mLX
        self.LY = mLY
        self.CarteFX = [[None] * self.LX for _ in range(self.LY)]
        self.CarteEntity = [[None] * self.LX for _ in range(self.LY)]
        self.Carte = bytearray(self.LX *self.LY)
                
    # **************************************************************************
    # ** Réinitialisation de la MAP                                           **
    # **************************************************************************
    
    def reInit(self):
        """
        Cette fonction assure la remise à zéro de tous les paramètres 
        
        /!\ Seul la liste des joueur est conservée       
        """
        
        self.NomLaby = ''        # Nom du Labyrinthe
        self.Theme = "Gray"      # Theme graphique du labyrinthe
        self.LX = -1             # Largeur du Labyrinthe
        self.LY = -1             # Hauteur du Labyrinthe
        
        self.Carte = None        # byte array du labyrinthe
        self.CarteEntity = []    # Recense la position des joueurs (et monstres)
        self.CarteFX = []        # Recense les effets dynamiques
        
        self.PlayerSponePlace = set()  # Ensemble des positions d'apparition
        self.MonsterSponePlace = set()  # Ensemble des positions d'apparition
                        
        self.FXList = {}         # Liste des effets LabyTextFx
        
        self.isFinished  = False
        
        self.MsgList.clear()
        
        
        
        
    # **************************************************************************
    # ** Gestion des joueurs                                                  **
    # **************************************************************************

        
    def diePlayer(self,PlayerObj):
        
        self.pushMessage(PlayerObj.Name + " est très fatigué(e)... retour à la case départ")

        
    # **************************************************************************
    # ** Gestion des Déplacements                                             **
    # ************************************************************************** 
    
    def getAvlDir(self,x,y):
        """
            Retourne les directions possibles à partir d'une position            
        """ 
        
        # Vérifie que nous sommes bien dans les limites
        if not(self.__isValid) and not(x < self.LX and x >= 0 and y < self.LY and y >= 0) :
            return []
    
        # Vérifie qu'il n'y a pas de mur
        if (self.Carte[y*self.LX + x] & 0x0F) != 0 :
            return []
            
        Res = []
        
        if x > 0:
            if (self.Carte[y*self.LX + x-1] & 0x0F) == 0 :
                Res = Res + [ 'O' ]
                
        if y > 0:
            if (self.Carte[(y-1)*self.LX + x] & 0x0F) == 0 :
                Res = Res + [ 'N' ]
                
        if x < self.LX-1:
            if (self.Carte[y*self.LX + x+1] & 0x0F) == 0 :
                Res = Res + [ 'E' ]
                
        if y < self.LY-1:
            if (self.Carte[(y+1)*self.LX + x] & 0x0F) == 0 :
                Res = Res + [ 'S' ]
                
        return(Res)
    

    def checkPos(self,x,y,PlayerObj=None):
        """
        Fonction qui vérifie que la position x, y est libre pour un déplacement
        :param x:
        :param y:
        :return: true/false
        """
        
        # Vérifie que nous sommes bien dans les limites
        if not(self.__isValid) and not(x < self.LX and x >= 0 and y < self.LY and y >= 0) :
            return False
        
        #print("checkPos(",x,",",y,") [", self.Carte[y*self.LX + x] & 0x0F,"]" )    
            
        # Vérifie qu'il n'y a pas un autre joueur/monstre
        if self.CarteEntity[y][x] is not None :
            return False
            
        #print("checkPos:Pas de joueur",x,y, self.Carte[y*self.LX + x] )
            
        # Vérifie qu'il n'y a pas de mur
        if (self.Carte[y*self.LX + x] & 0x0F) != 0 :
            return False
                        
        #print("checkPos:Pas vide",x,y, self.Carte[y*self.LX + x] )
            
        # Est un effet
        if (PlayerObj is not None):
            
            #print("OK for FX Test")
            
            if self.CarteFX[y][x] is not None:
                return self.CarteFX[y][x](PlayerObj,'check',x,y)              
                    
        # Dans le cas par défaut on retourne True
        return True

        
    def updatePlayerPos(self,ObjPlayer,prev_x,prev_y):
        """
        Cette fonction est utiliser pour mettre à jour la carte avec la position 
        du joueur.
        :param ObjPalyer: Joueur; prev_x,prev_y ancienne position
        :returns: None si ce n'est pas possible, sinon True ou False pour dire visible ou pas
        """

        #print("LabyObj::updatePlayerPos")
        
        if prev_x >= self.LX or prev_y >= self.LY:
            return None

        if self.CarteFX[ObjPlayer.y][ObjPlayer.x] is not None:
            (nx,ny) = self.CarteFX[ObjPlayer.y][ObjPlayer.x](ObjPlayer,'apply') 
            if nx is not None:
                
                self.CarteEntity[prev_y][prev_x] = None
                
                if nx >= 0:            
                
                    print("LabyObject::updatePlayerPos :: OK for FX Apply nouvelle pos : ",nx,ny)
                    ObjPlayer.moveTo((nx,ny))               
                    self.CarteEntity[ObjPlayer.y][ObjPlayer.x] = ObjPlayer

            else:
                self.CarteEntity[prev_y][prev_x] = None
                self.CarteEntity[ObjPlayer.y][ObjPlayer.x] = ObjPlayer
                
        else:
            self.CarteEntity[prev_y][prev_x] = None
            self.CarteEntity[ObjPlayer.y][ObjPlayer.x] = ObjPlayer
                

         
        # Calcul de la lumière
        if self.IsShadowEnabled:
            if ObjPlayer.isLightUpdater:
                self.updateLight(ObjPlayer.x,ObjPlayer.y) 
                
            # Calcul de la visibilitée
            if self.Carte[ObjPlayer.y * self.LX + ObjPlayer.x] & 0xF0 == 0:
                return False
            
        return True
        
    def getSponePos(self, ObjEntity, rayon=0):
        """
            Selectionne un point d'apparition            
        """
        
        if(isinstance(ObjEntity,Entity.Monster)) :
            T = self.MonsterSponePlace
        else:
            T = self.PlayerSponePlace
        
        (x,y) = random.choice(list(T))
        
        # Vérifie qu'il n'y a pas quelqu'un déjà
        
        while ((self.checkPos(x,y) == False) and (len(T)>0)):
            
            xmin = x - rayon
            if xmin < 0 : xmin=0
            xmax = x + rayon
            if xmax > self.LX : xmax = self.LX-1
            ymin = y - rayon
            if ymin < 0 : ymin=0
            ymax = y + rayon
            if ymax > self.LY : ymax = self.LY-1
            
            for mx in range(xmin,xmax):
                for my in range(ymin,ymax):
                    if self.checkPos(mx,my) :                    
                        ObjEntity.setInitialPos(mx,my)
                        ObjEntity.x = mx
                        ObjEntity.y = my
                        return True
                    

            T = T - {(x, y)}
            if len(T) > 0 :
                (x,y) = random.choice(list(T))
            else:
                break
            
        if self.checkPos(x,y) :
            ObjEntity.setInitialPos(x,y)
            return True

        # Limite de recherche avec un rayon de 5
        if rayon > 3:            
            print("Laby::getSponePos : limite maximum de recherche de la position de départ atteinte pour l'entité",
                   ObjEntity.Name) 
            return False
        else:
            self.getSponePos(ObjEntity,rayon+1)
            
    
    # **************************************************************************
    # * Gestion du Shadow                                                      *
    # **************************************************************************
       
    def updateLight(self, x,y):
        
        """
        Cette fonction assure le calcul de l'éclairage du labyrinthe
        A chaque fois qu'un joueur se déplace, alors la case où se 
        trouve le joueur est éclairée ansi qu'une partie des cases
        à proximitées
        """
        
        if x < self.LX-1:
            max_x=x+1
        else:
            max_x = x
            
        if x > 0:
            min_x = x-1
        else:
            min_x = 0
            
        if y > 0:
            min_y = y-1
        else:
            min_y = 0
            
        if y < self.LY-1:
            max_y = y+1
        else:
            max_y = y
            
       # print("min/max x y == LX,LY == x y",min_x, max_x, min_y, max_y, "==", self.LX, self.LY, " == ", x,y)
            
        for px in range(min_x,max_x+1):
            for py in range(min_y,max_y+1):
                
                
                if (px == 0 and py == 0) or \
                   (px == 0 and py == self.LY-1) or  \
                   (px == self.LX-1 and py == self.LY-1) or \
                   (px == self.LX-1 and py == 0):
                       code = 0xF0
                elif py == 0:
                    if px == x: code = 0xF0
                    elif px < x: code = 0xD0
                    else: code = 0xE0
                elif px == 0:
                    if py == y: code = 0xF0
                    elif py < y: code = 0xB0                        
                    elif py > y: code = 0xE0                                        
                elif px == self.LX-1:
                    if py == y: code = 0xF0
                    elif py < y: code = 0x70                        
                    elif py > y: code = 0xD0                     
                elif py == self.LY-1:
                    if px == x: code = 0xF0
                    elif px < x: code = 0x70
                    else: code = 0xB0
                elif px == x:
                    if py == y: code = 0xF0
                    elif py < y: code = 0x30
                    elif py > y: code = 0xC0                    
                elif px < x:
                    if py == y: code = 0x50
                    elif py < y: code = 0x10
                    elif py > y: code = 0x40
                else:
                    if py == y: code = 0xA0
                    elif py < y: code = 0x20
                    else: code = 0x80                    
                    
        #        print("px,py = code",px, py, " = ", hex(code))
                pos = py * self.LX + px
            
                self.Carte[pos] = self.Carte[pos] | code
                
        self.IsShadowUpdated  = True
    
    def blackOut(self):
        
        for p in range(0,len(self.Carte)):
            self.Carte[p] = self.Carte[p] & 0x0F
            
        self.resetPermananteLigth(True)
            
    def showAll(self):
        
        for p in range(0,len(self.Carte)):
            self.Carte[p] = self.Carte[p] | 0xF0
            
    def resetPermananteLigth(self, PermOnly = False):
        """
        Fonction utilisée pour réactivé les lumières par défaut.
        si PermOnly = True, seules les lumières dite permanantes seront reprises,
        sinon toute les lumières auto seront réactivées
        """
        
        return
    
    # **************************************************************************
    # ** Gestion des effets dynamiques                                        **
    # **************************************************************************
    
    def _registerFx(self, FX, code):
        """
        Enregistre l'effet dans la liste des effets actifs
        """
        
        # Vérification que l'objet descent bien de LabyTextFx
        if not(isinstance(FX,LabyTextFx.LabyTextFx)):
            return False
            
         # Vérification que le joueur n'est pas déjà enregistrer
        if code in self.FXList.keys():
            return False
            
        # Ajout du joueur dans la liste
        self.FXList[code] = FX
        
        return FX.initFx(self,code)
    
    def _registerFxCb(self, Fonc, x, y):
        """
        Enregistre la call back en position X,Y de l'effet
        """
        
        # Vérification qu'il n'y a pas déjà une call back

        if self.CarteFX[y][x] is None:
            self.CarteFX[y][x] = Fonc
            return True
            
        return False
       
    # **************************************************************************
    # ** Gestion des messages                                                 **
    # **************************************************************************
    
    def pushMessage(self, Message, Temps=5):
        """
        Fonction assurant la collecte des message, le paramètre temps indique
        le temps d'affichage du message en secondes
        """
        
        self.MsgList.insert(0,(Message,Temps))
        
    def popMessage(self):
        
        if(len(self.MsgList) > 0) :
            return self.MsgList.pop()
        else:
            return (None,None)

    def countMessage(self):
        
        return(len(self.MsgList))
        

    @property
    def isValide(self):
        """
        Function qui informe si le Labyrinthe est utilisable
        :return True/False:
        """
        return __isValid

    def getSize(self):
        """
        Fonction qui retourne la taille du Labyrinthe
        :return: (lx,ly)
        """
        return (self.LX,self.LY)
        
    # **************************************************************************
    # ** Evénements externes                                                  **
    # **************************************************************************
    
    def onAllMonsterDead(self):
        """
        Fonction appelé pour indiquer que tout les monstres sont morts
        """
        
        self.isFinished = True
        


        
        
        
                
            
            