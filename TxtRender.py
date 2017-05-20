from Player import Player
from LabyText import LabyText

__author__ = 'Yoann'


# *****************************************************************************
# ** Classe dérivant du Player pour introduire les spécificité de l'affichage**
# ** en mode text.                                                           **
# *****************************************************************************

class TxtPlayer(Player):

    """
       Cette classe dérive de la classe Player afin de définir
       les methode et propriété pour l'affichage d'un joueur
       en mode texte
    """

    Icon = ''  # Contient le caractère d'affichage

    def __init__(self, initPv=100, disp='@'):
        Player.__init__(self,initPv)
        self.Icon = disp[0]

    def __str__(self):
        """ Methode appelée lorsque que l'on utilise la fonction print() """
        return "{2} [{0} PV:{1}]".format(self.Name, self.PV, self.Icon)


class TxtRender():

    """
    Cette classe s'occupe de l'affichage
    """

    __Map =  None  # Contient une référence sur le labyrinthe
    __Players = []

    def DoRender(self):
        """
            Effectue l'affichage du Labyrinthe
        """

        # Créer l'ensemble des lignes occupées par un Joueur
        py = [i.y for i in self.__Players]

        # Routine d'affichage de toutes les lignes du labyrinthe
        if self.__Map is not None:
            for n,l in enumerate(self.__Map.Carte):
                if n in py:
                    for p in self.__Players:
                        if p.y == n:
                            l = l[:p.x]+p.Icon+l[p.x+1:]
                    print(l)
                else:
                    print(l)

        # Routine d'affichage des score
        for i in self.__Players:
            print(i)


    def SetLaby(self, Laby):
        self.__Map = Laby

    def AddUser(self, player):
        if type(player) != TxtPlayer:
            raise Exception("Le paramètre Joueur n'est pss du bon type !")
        else:
            self.__Players.append(player)


###
#   Test de la Classe
###

# Note: Cette partie du code ne sera exécutée que si il est appelée en exécution,
# mais pas si le fichier est importé. Ceci est pratique pour écrire des tests de Classe
if __name__ == "__main__":

    TestLaby = LabyText()

    Renderer = TxtRender()

    J1 = TxtPlayer(45,'@')
    J2 = TxtPlayer(50,'&')

    J1.OnCheckMove = TestLaby.checkPos
    J1.x = 3
    J1.y = 3

    J2.OnCheckMove = TestLaby.checkPos
    J2.x = 10
    J2.y = 10

    Renderer.SetLaby(TestLaby)
    Renderer.AddUser(J1)
    Renderer.AddUser(J2)

    Renderer.DoRender()

    