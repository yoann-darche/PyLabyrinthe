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
            "T @    |q          |        | A        T",
            "+----+ | --_----+  | +---+  |  ------+ |",
            "|    |    >p>   |  | |   |           | |",
            "| +  +--P-+ +-+ |  + + + +-R-+^----+ | |",
            "| |           | |      | |@ p|  r  < | |",
            "| +----+ +--+ + +---+  | P   +^----+ | |",
            "|      < |          | ++ |1 1>  q T| | |",
            "+--+   + +--------+1+ |  +-Q-+-----+-+ |",
            "|s     | |        +++ | ++         |   |",
            "+--+   | ++  A    |   |  | +-+ +--_+ +0|",
            "|  |   |  |   +---+ + |A++ |s    >   +-+",
            "|  |   ++ |       | +-+-+  +-+---+ +-+T|",
            "|  +-+  + +-----+ | |   | ++   Su+   | |",
            "T       |       | | < | | |  +---+---+^|",
            "|    +--+-+     | | +-+ |   ++      s| |",
            "|    |       @  + + | | +++ +  +-----+ |",
            "| +--+ +------+     | |   |         u| |",
            "|   @|        +-----+ + + +------+U+-+ |",
            "|    |        |T  q |   |              |",
            "+----+--------------+---+--------------+"]
    
        self.Theme = "Blue"
        self.IsShadowEnabled = False
        elf.SponeCode = '@'
        