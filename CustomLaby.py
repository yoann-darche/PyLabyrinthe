# -*- coding: utf-8 -*-

import LabyText

__author__ = 'Yoann'

"""
    Ce package contient la définition de la claasse LabyText, une classe dérivée de LabyObject
    implémentant le code exécutable pour la gestion d'un Labyrinthe en mode texte.
"""

import LabyTextFxTunnel

class LabyCustom(LabyText.LabyText):


    def initMap(self):
    
        self.CarteTxt = [
            "+------+-----------+--------+----------+",
            "T      |q          |        | A        T",
            "+----+ | --_----+  | +---+  |  ------+ |",
            "|    |    >p>   |  | |   |           | |",
            "| +  +--P--_--+ |  + + + +-R-+^----+ | |",
            "| |           | |      | |1 p|  r  < | |",
            "| +----+ +--+ + +---+  | P   +^----+ | |",
            "|      < |          | ++ |1 1>  q T| | |",
            "+--+   + +--------+1+ |  +-Q-+-----+-+ |",
            "|s     | |        +++ | ++         |   |",
            "+--+   | ++       |   |  | +-+ +--_+ +0|",
            "|  |   |  |   +---+ + |T++ |s    >   +-+",
            "|  |   ++ |       | +-+-+  +-+---+ +-+T|",
            "|  +-+  + +-----+ | |   | ++   Su+   | |",
            "T       |A      | | < | | |  +---+---+^|",
            "|    +--+-+     | | +-+ |   ++      s| |",
            "|    |       1  + + | | +++ +  +-----+ |",
            "| +--+ +------+     | |   |         u| |",
            "|    |        +-----+ + + +------+U+-+ |",
            "|    |        |T  q |   |              |",
            "+----+--------------+---+--------------+"]
    
        self.Theme = "Blue"
        self.IsShadowEnabled = False
        