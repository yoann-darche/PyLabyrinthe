# -*- coding: utf-8 -*-

__author__ = 'Yoann'


class Entity():

    """
    Cette classe correspond à la définition des méthodes communes aux Joueurs 
    et monstre du Labyrinthe    
    """

    def __init__(self, initpv = 100):

        self.Name = "nobody"
        self.x = -1
        self.y = -1
        self.lastDir = None
        self.allowedDir = ('N', 'S', 'E', 'O')

        self.PV = initpv

        self._hasChanged = False

        # Call back
        self.OnCheckMove = None
        self.OnUpdateLabPos = None
        self.OnDie = None


    def move(self, direction):
        """
        Cette fonction s'occupe de gérer le déplacement du joueur
        :param direction: 'N' | 'S' | 'O' | 'E'
        :return: true / false
        """
        
        
        if direction not in self.allowedDir: return False
        
        self.lastDir = direction

       # print("Movement détecté sur le joueur {0} en position {1},{2} dir={3}".format(self.Name, self.x, self.y, direction))
        #try:
        if direction == 'N' and self.OnCheckMove(self.x, self.y-1, self):
            self.y -= 1
            self.allowedDir = ('N','S','E','O')
            self.OnUpdateLabPos(self,self.x,self.y+1)            
        elif direction == 'S' and self.OnCheckMove(self.x, self.y+1, self):
            self.y += 1
            self.allowedDir = ('N','S','E','O')
            self.OnUpdateLabPos(self,self.x,self.y-1)
        elif direction == 'E' and self.OnCheckMove(self.x+1, self.y, self):
            self.x += 1
            self.allowedDir = ('N','S','E','O')
            self.OnUpdateLabPos(self,self.x-1,self.y)            
        elif direction == 'O' and self.OnCheckMove(self.x-1, self.y, self):
            self.x -= 1
            self.allowedDir = ('N','S','E','O')
            self.OnUpdateLabPos(self,self.x+1,self.y)
        else:
            return False
        #except:
        #    print(">>> Execpetion Player::move()")
        #    return False

       
         
        self.changePv(-1)
        self._hasChanged = True
        return True

    def moveTo(self, coord):
        """
        Cette fonction déplace le jour en coordonnées absolues
        
        :param: coord un couple de deux valuer (x,y)
        :return: True / False
        """
        
        (self.x,self.y) = coord
            
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
                self.OnDie()
            except:
                pass

        return self.PV
        
    def setAllowedMove(self, dirs= ('N','S','E','O')):
        
        self.allowedDir = dirs



        
class Player(Entity):

    """
    Cette classe correspond à la définition des Joueurs
    
    Elle implemente les fonction spécicique au joueurs
    """
    
    
class Monster(Entity):
    
    """
    Cette classe correspond à la définition des Monstres
    
    Elle implemente les fonction spécicique au Monstre
    """
    
    def doMove(self):
        x = x
