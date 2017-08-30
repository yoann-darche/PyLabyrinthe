# -*- coding: utf-8 -*-

import random
import MonsterEngine

__author__ = 'Yoann'


class Entity():

    """
    Cette classe correspond à la définition des méthodes communes aux Joueurs 
    et aux monstres du Labyrinthe    
    """

    def __init__(self, initpv = 100):
        

        self.Name = "nobody"
        self.x = -1
        self.y = -1
        self.lastDir = None
        self.allowedDir = ('N', 'S', 'E', 'O')
        
        self._initPV = initpv
        self.PV = self._initPV
        
        self.isLightUpdater = True   # Indique si l'entité met à jour les zone éclairé du labyrinthe
        self.isVisible      = True

        self._hasChanged = False

        # Call back
        self.OnCheckMove = None
        self.OnUpdateLabPos = None
        self.OnDie = None
        

                
                
    def restart(self):
        """
        Cette fonction est appelée pour réinitialiser la position de l'entité
        """
        self.PV = self._initPV
        self.lastDir = None
        self.allowedDir = ('N', 'S', 'E', 'O')
        self.moveToInitialPos()
        
    def setInitialPos(self,x,y):
        """
        Définit la position initiale de l'netité
        """
        self._initX = x
        self._initY = y


    def move(self, direction):
        """
        Cette fonction s'occupe de gérer le déplacement du joueur
        :param direction: 'N' | 'S' | 'O' | 'E'
        :return: true / false
        """
        
        
        if direction not in self.allowedDir: return False
        
        self.lastDir = direction

        #print("Movement détecté sur le joueur {0} en position {1},{2} dir={3}".format(self.Name, self.x, self.y, direction))
        #try:
        if direction == 'N' and self.OnCheckMove(self.x, self.y-1, self):
            self.y -= 1
            self.allowedDir = ('N','S','E','O')
            res = self.OnUpdateLabPos(self,self.x,self.y+1)            
        elif direction == 'S' and self.OnCheckMove(self.x, self.y+1, self):
            self.y += 1
            self.allowedDir = ('N','S','E','O')
            res = self.OnUpdateLabPos(self,self.x,self.y-1)
        elif direction == 'E' and self.OnCheckMove(self.x+1, self.y, self):
            self.x += 1
            self.allowedDir = ('N','S','E','O')
            res = self.OnUpdateLabPos(self,self.x-1,self.y)            
        elif direction == 'O' and self.OnCheckMove(self.x-1, self.y, self):
            self.x -= 1
            self.allowedDir = ('N','S','E','O')
            res = self.OnUpdateLabPos(self,self.x+1,self.y)
        else:
            return False
        #except:
        #    print(">>> Execpetion Player::move()")
        #    return False

       
         
        self.changePv(-1)
        self._hasChanged = True

        # La valeur de retour de OnUpdateLabPos peut être None !
        if res == True:
            self.isVisible = True
        elif res == False:
            self.isVisible = False
                    
        
        return True
        
    def moveToInitialPos(self):
        """
        Positionne l'entité sur la case de départ
        """
        self.moveToInternal((self._initX,self._initY))


    def moveTo(self, coord):
        """
        Cette fonction déplace le jour en coordonnées absolues
        /!\ En appel externe !!
        
        :param: coord un couple de deux valuer (x,y)
        :return: True / False
        """

        (self.x,self.y)= coord
        self._hasChanged = True
                    
        return True
        
    def moveToInternal(self, coord):
        """
        Cette fonction déplace le jour en coordonnées absolues
        /!\ En appel interne !!
        
        :param: coord un couple de deux valuer (x,y)
        :return: True / False
        """
        x = self.x
        y = self.y
        (self.x,self.y)= coord
        
        #print("Entity::moveToInternal old({0},{1}) new({2},{3})".format(x,y,self.x,self.y))
        
        try: 
            res = self.OnUpdateLabPos(self,x,y)
            if res == True:
                self.isVisible = True
            elif res == False:
                self.isVisible = False
        except:
            pass

        self._hasChanged = True
            
        return True
        
    
    
    def changePv(self, nb=-1):
        """
        Cette fonction assure la modification des point de vie,
        et vérifie également si il en reste. Dans le cas où nous
        sommes arrivé au bout alors on tente d'appeler la callback OnDie.

        :param nb: nombre de point de vie à supprimer ou ajouter
                     < 0 => Supprime des point de vie
                     > 0 => Ajoute des point de vie
        :return: le nombre de point de vie restant
        """
        self.PV += nb
        if self.PV <= 0:
            self.PV = 0
            try:
                self.OnDie(self)
            except:
                pass
                
            self.moveToInitialPos()
            self.PV = self._initPV

        return self.PV
        
    def setAllowedMove(self, dirs= ('N','S','E','O')):
        
        self.allowedDir = dirs
        

        
class Player(Entity):

    """
    Cette classe correspond à la définition des Joueurs
    
    Elle implemente les fonctions spéciciques aux joueurs
    """
    
    
class Monster(Entity):
    
    """
    Cette classe correspond à la définition des Monstres    
    Elle implemente les fonctions spéciciques aux Monstres
    """
    
    def __init__(self, speed = 1, initpv = 100):
        """
        Constructeur du Monstre
        :param speed : vitesse de déplacement du monstre en ms
        :param initpv: nombre de point de vie du monstre
        """
        
        # Appel de l'init de la classe parente (Entity)
        Entity.__init__(self, initpv)
        
        # Par défaut les monstre ne découvre pas le labyrinthe
        self.isLightUpdater = False
        self.isVisible      = False
        
        self.OnAvlDir = None # Recherche les direction possible
        
        self.speed = speed
        self.lastDt = 0
        
        # Affect l'algorithme de déplacement du monstre
        self.engine = MonsterEngine.MME_Standard
        
        self._mgr = None            # Pointeur sur la Classe de gestion des monstres
        
        
    
    def doMove(self, dt):
        """
        Cette fonction assure le déplacement du monster
        """
        
        self.lastDt += dt
        
        # si le Delta time est supérieur à la vitesse alors on bouge
        if(self.lastDt > self.speed):
            self.lastDt = 0
            
            self.engine(self,dt)
            
    def kill(self):
        """
        Fonction assurant la suppression du monstres (logique)
        """
        
        self._mgr.removeMonster(self)
                        

# ==============================================================================
# == Gestion de la liste des entités                                           ==
# ==============================================================================

class EntityList:
    
    def __init__(self, LabyObject):
        
        self._map = LabyObject
        self.ActiveMonsterList = []      # Liste des monstres actifs
        self.InActiveMonsterList = []    # Liste des monstres mort ou inactif
        self.ActivePlayerList = []       # Liste des monstres actifs
        
        self.OnFinish = None             # Call back quand il n'y a plus de monstres actifs
        
        self.hasUpdate = False
    
    def addMonster(self, MonsterObj):
        """
        Cette fonction ajoute un monstre dans le labyrinthe
        :param MonsterObj objet représentant un monstre descendant de Entity.py
        :return True/False
        """
        # Vérification que l'objet est bien un descendant de Monster
        if not(isinstance(MonsterObj,Monster)):
            return False
            
        # Vérification que le monstre n'est pas déjà enregistré
        if (MonsterObj in self.ActiveMonsterList) or (MonsterObj in self.InActiveMonsterList):
            return False
            
        # Recherche une position
        if self._map.getSponePos(MonsterObj) == False:
            print("EntityList::addMonster : Erreur lors de la recherche d'une position")
            return False

            
        # Ajout du monstre dans la liste
        self.ActiveMonsterList.append(MonsterObj)
        
        
        # Lien avec la fonction de contrôle de déplacement
        MonsterObj.OnCheckMove = self._map.checkPos
        MonsterObj.OnUpdateLabPos = self._map.updatePlayerPos
        MonsterObj.OnAvlDir = self._map.getAvlDir
        MonsterObj._mgr =  self
        
        # ajout de sa position dans la carte
        if MonsterObj.x < self._map.LX and MonsterObj.x >= 0 and MonsterObj.y < self._map.LY and MonsterObj.y >= 0 :
            self._map.CarteEntity[MonsterObj.y][MonsterObj.x] = MonsterObj
        
        self.hasUpdate = True
        
        return True
                

    def removeMonster(self, MonsterObj):
        """
        Cette fonction supprime un monstre du labyrinthe
        :param MonsterObj objet représentant un monster descendant de Entity.py
        :return True/False
        """ 
        
        # Vérification que le monstre est bien enregistré
        if MonsterObj in self.ActiveMonsterList:
            # Efface la position dans la carte
            self._map.CarteEntity[MonsterObj.y][MonsterObj.x] = None
            # Transfert le monstre de la liste Active vers la liste inactive
            self.ActiveMonsterList.remove(MonsterObj)
            self.InActiveMonsterList.append(MonsterObj)            
            
            self.hasUpdate = True
            
            # Si il n'y a plus de monstre alors on appelle la call back
            if len(self.ActiveMonsterList) < 1:
                try:
                    self.OnFinish()
                except:
                    pass
            
            return True
            
        return False
        
    def updateMonster(self,dt):
        """
        Gestion des mouvements des monstres
        """
        # Pour chaque monstre
        for p in self.ActiveMonsterList:
            p.doMove(dt)
            
    def deleteMonster(self, MonsterObj):
        """
        Cette fonction supprime le monstre des 2 listes
        """
        
        if MonsterObj in self.ActiveMonsterList:
            # Efface la position dans la carte
            self._map.CarteEntity[MonsterObj.y][MonsterObj.x] = None
            self.ActiveMonsterList.remove(MonsterObj)
            self.hasUpdate = True
            
        if MonsterObj in self.InActiveMonsterList:
            self.ActiveMonsterList.remove(MonsterObj)
            self.hasUpdate = True
            
    def reinitMonster(self):
        """
            Cette fonction reactive tous les monstres
        """
                
        for p in self.ActiveMonsterList:
            
            if self._map.getSponePos(p) == False:
                print("EntityList::reinitMonster : Erreur lors de la recherche d'une position")                
            p.restart()
            
        for p in self.InActiveMonsterList:


            print("Trainetement du monstre : ",p)

            # Repositionne le monstre sur la carte
            if self._map.getSponePos(p) == False:
                print("EntityList::reinitMonster : Erreur lors de la recherche d'une position")
            else:
                print("EntityList::reinitMonster: transfert du monstre ",p)
                self.InActiveMonsterList.remove(p)
                self.ActiveMonsterList.append(p)
                
            p.restart()
            
        self.hasUpdate = True
        
        
    def addPlayer(self, PlayerObj):
        """
        Cette fonction ajoute un joueur dans la liste
        """
        
        # Vérification que l'objet est bien un descendant de Player
        if not(isinstance(PlayerObj,Player)):
            return False
            
        # Vérification que le joueur n'est pas déjà enregistré
        if (PlayerObj in self.ActivePlayerList) :
            return False
            
        # Recherche une position
        if self._map.getSponePos(PlayerObj) == False:
            print("EntityList::addPlayer : Erreur lors de la recherche d'une position")
            return False
            
        # Ajout du monstre dans la liste
        self.ActivePlayerList.append(PlayerObj)
        
        # Lien avec les fonctions de contrôle de déplacement, et évènements
        PlayerObj.OnCheckMove = self._map.checkPos
        PlayerObj.OnUpdateLabPos = self._map.updatePlayerPos
        PlayerObj.OnDie = self._map.diePlayer

        #PlayerObj.OnAvlDir = self._map.getAvlDir
        #PlayerObj._mgr =  self
        
        # ajout de sa position dans la carte
        if PlayerObj.x < self._map.LX and PlayerObj.x >= 0 and PlayerObj.y < self._map.LY and PlayerObj.y >= 0 :
            self._map.CarteEntity[PlayerObj.y][PlayerObj.x] = PlayerObj
            
        self.hasUpdate = True
        
        return True
        
    def deletePlayer(self, PlayerObj):
        """
        Cette fonction supprime un joueur du labyrinthe
        :param PlayerObj objet représentant un joueur descendant de Entity.py
        :return True/False
        """ 
        
        # Vérification que le joueur n'est pas déjà enregistrer
        if PlayerObj in self.ActivePlayerList:
            # Efface la position dans la carte
            self._map.CarteEntity[PlayerObj.y][PlayerObj.x] = None
            # retire de la liste
            self.ActivePlayerList.remove(PlayerObj)
            return True
            
        return False
        
        
    def reinitPlayer(self):
        """
            Cette fonction reactive tous les joueur
        """
                
        for p in self.ActivePlayerList:
            
            if self._map.getSponePos(p) == False:
                print("EntityList::reinitPlayer : Erreur lors de la recherche d'une position")                
            p.restart()
            
            
        self.hasUpdate = True