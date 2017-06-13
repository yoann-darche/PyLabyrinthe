# -*- coding: utf-8 -*-

import random
import MonsterEngine

__author__ = 'Yoann'


class Entity():

    """
    Cette classe correspond à la définition des méthodes communes aux Joueurs 
    et monstre du Labyrinthe    
    """

    def __init__(self, initpv = 100):


        self._mgr = None            # Pointeur sur la Classe de gestion des monstres

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
        
    def kill(self):
        """
        Fonction assurant la suppression du monstres (logique)
        """
        
        self._mgr.removeMonster(self)
        
        
        



        
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
        
        
    
    def doMove(self, dt):
        """
        Cette fonction assure le déplacement du monster
        """
        
        self.lastDt += dt
        
        # si le Delta time est supérieur à la vitesse alors on bouge
        if(self.lastDt > self.speed):
            self.lastDt = 0
            
            self.engine(self,dt)
                        

