#!/usr/bin/env python
from deck import Deck
from card import Card
from player import Player

class Game(object):
    """ Airlock game object """

    def __init__(self):
        self.create_oxygen()
        self.create_decks(True)
        self.players = []
        self.active_player = None


    def main(self):
        """ Plays the game """

        print(self.deck)


    def add_player(self, name):
        """ Adds a player of name 'name' to the game. """

        self.players.append(Player(self, name))


    def create_decks(self, expansion = True):
        """ Creates the deck objects. """

        self.deck = Deck(self, expansion, True)
        self.discard = Deck(self)
        self.command_pile = Deck(self)


    def create_oxygen(self):
        """ Creates the oxygen cells. """

        self.oxygen = 6
        self.cell_types = ['r','r','b','b','b','b']
        self.force_red = False
        self.oxygen_protected = False

    def damage_oxygen(self):
        """ Damages an oxygen cell. """

        #   TODO consider end game situation
        self.oxygen -= 1


    def is_red_alert(self):
        """ Returns True if the current oxygen cell is a red alert cell """

        return self.oxygen[-1] == 'red' or self.force_red


if __name__ == '__main__':
    game = Game()
    game.add_player('Paul')
    game.add_player('Daniel')
    game.add_player('Jeremy')
    game.main()
