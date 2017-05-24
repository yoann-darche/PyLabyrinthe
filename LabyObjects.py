__author__ = 'Yoann'

import Entity
import LabyTextFx

class Laby():
    """
    Cette objet est une méta classe (une classe modèle)
    qui regroupe toutes les définitions des fonctions logiques
    nécessaires à l'utilisation de la carte du Labyrinthe
    """
    


    def __init__(self,fileName=None):
        """
        Constructeur de Classe: Cette fonction lance l'initialisation de l'objet.
        Si un nom de fichier est préciser alors il sera chargé, sinon la fonction
        de construction par défaut sera appélée.

        :param fileName: Nom du fichier à charger
        :return: instance de Classe
        """


        self.NomLaby = ''        # Nom du Labyrinthe
        self.Theme = "Gray"      # Theme graphique du labyrinthe
        self.LX = -1             # Largeur du Labyrinthe
        self.LY = -1             # Hauteur du Labyrinthe
        
        self.Carte = None        # byte array du labyrinthe
        self.CarteEntity = []    # Recense la position des joueurs (et monstres)
        self.CarteFX = []        # Recense les effets dynamiques
        
        self.PlayerList = []     # Liste des joueurs
        self.MonsterList = []    # Liste des monstres
        self.FXList = {}         # Liste des effets LabyTextFx
        
    
        # Propriétés d'état de la classe
        self.__isValid = False

        
        self.IsShadowEnabled = False
        
        if fileName == None:
            self.initMap()
            self.setDefault()
        else:
            try:
                __isValid = self.loadFromFile(fileName)
            except:
                __isValid = False
                
        

    def loadFromFile(self, Source):
        """
        Function assurant le chargement d'une carte de Labyrinthe depuis un fichier
        :param Source: chemin complet pour atteindre le fichier
        :return: true/false
        """
        return False

    def setDefault(self):
        """
        Cette fonction créer un labyrinthe de test par défaur
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
    # ** Gestion des joueurs                                                  **
    # **************************************************************************

    def addPlayer(self, PlayerObj):
        """
        Cette fonction ajoute un joueur dans le labyrinthe
        :param PlayerObj objet représentant un joueur descendant de Entity.py
        :return True/False
        """
        # Vérification que l'objet est bien un descendant de Player
        if not(isinstance(PlayerObj,Entity.Player)):
            return False
            
        # Vérification que le joueur n'est pas déjà enregistrer
        if PlayerObj in self.PlayerList:
            return False
            
        # Ajout du joueur dans la liste
        self.PlayerList.append(PlayerObj)
        
        
        # Lien avec la fonction de contrôle de déplacement
        PlayerObj.OnCheckMove = self.checkPos
        PlayerObj.OnUpdateLabPos = self.updatePlayerPos
        
        # ajout de sa position dans la carte
        if PlayerObj.x < self.LX and PlayerObj.x >= 0 and PlayerObj.y < self.LY and PlayerObj.y >= 0 :
            self.CarteEntity[PlauerObj.y][PlayerObj.x] = PlayerObj
        
        
        return True

    def removePlayer(self, PlauerObj):
        """
        Cette fonction supprime un joueur du labyrinthe
        :param PlayerObj objet représentant un joueur descendant de Entity.py
        :return True/False
        """ 
        
        # Vérification que le joueur n'est pas déjà enregistrer
        if PlayerObj in self.PlayerList:
            # Efface la position dans la carte
            self.CarteEntity[PlauerObj.y][PlayerObj.x] = None
            # retire de la liste
            self.PlayerList.remove(PlayerObj)
            return True
            
        return False


    # **************************************************************************
    # ** Gestion des Monstres                                                 **
    # **************************************************************************   

    def addMonster(self, MonsterObj):
        """
        Cette fonction ajoute un monstre dans le labyrinthe
        :param MonsterObj objet représentant un monstre descendant de Entity.py
        :return True/False
        """
        # Vérification que l'objet est bien un descendant de Monster
        if not(isinstance(MonsterObj,Entity.Monster)):
            return False
            
        # Vérification que le monstre n'est pas déjà enregistré
        if MonsterObj in self.MonsterList:
            return False
            
        # Ajout du monstre dans la liste
        self.MonsterList.append(MonsterObj)
        
        
        # Lien avec la fonction de contrôle de déplacement
        MonsterObj.OnCheckMove = self.checkPos
        MonsterObj.OnUpdateLabPos = self.updatePlayerPos
        MonsterObj.OnAvlDir = self.getAvlDir
        
        # ajout de sa position dans la carte
        if MonsterObj.x < self.LX and MonsterObj.x >= 0 and MonsterObj.y < self.LY and MonsterObj.y >= 0 :
            self.CarteEntity[MonsterObj.y][MonsterObj.x] = MonsterObj
        
        
        return True

    def removeMonster(self, MonsterObj):
        """
        Cette fonction supprime un monstre du labyrinthe
        :param MonsterObj objet représentant un monster descendant de Entity.py
        :return True/False
        """ 
        
        # Vérification que le monstre est bien enregistré
        if MonsterObj in self.MonsterList:
            # Efface la position dans la carte
            self.CarteEntity[MonsterObj.y][MonsterObj.x] = None
            # retire de la liste
            self.MonsterList.remove(MonsterObj)
            return True
            
        return False
        
    # **************************************************************************
    # ** Gestion des mouvements des monstres                                  **
    # ************************************************************************** 
    
    def updateMonster(self,dt):
        # Pour chaque monstre
        for p in self.MonsterList:
            p.doMove(dt)
        
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
        """

        if prev_x >= self.LX or prev_y >= self.LY:
            return False

        if self.CarteFX[ObjPlayer.y][ObjPlayer.x] is not None:
            (nx,ny) = self.CarteFX[ObjPlayer.y][ObjPlayer.x](ObjPlayer,'apply') 
            if nx is not None:
                
                self.CarteEntity[prev_y][prev_x] = None
                
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
        self.updateLight(ObjPlayer.x,ObjPlayer.y) 
            
        return True
        
        
        
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



