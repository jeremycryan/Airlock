#!/usr/bin/env python

#   Python libraries
import random

#   Outside libraries

class Card(object):
    """   An airlock card object """

    def __init__(self, game, name = 'energy'):
        self.game = game
        self.name = name


class Deck(object):
    """   A deck of airlock cards """

    def __init__(self, game, expansion = True):
        self.game = game
        self.cards = []
        self.populate(expansion)

    def populate(self, expansion = True):
        """ Adds the default deck. """

        #   Populates the deck
        self.add_card('energy', 13)
        self.add_card('impact', 7)
        self.add_card('rupture', 5)
        self.add_card('aftershock', 3)
        self.add_card('salvage', 2)
        self.add_card('safeguard', 2)
        self.add_card('hull breach', 3)
        self.add_card('recycle', 3)
        self.add_card('airlock', 1)
        self.add_card('martyr', 1)
        self.add_card('override', 3)
        self.add_card('overrule', 3)
        self.add_card('discharge', 3)
        self.add_card('wormhole', 2)

        #   Add expansion cards if expansion is enabled
        if expansion:
            self.add_card('engine failure', 2)
            self.add_card('nullify', 3)
            self.add_card('inflict', 2)
            self.add_card('repair', 2)
            self.add_card('contaminate', 2)
            self.add_card('execute', 1)
            self.add_card('shift', 3)

    def add_card(self, name, num=1):
        """ Adds 'num' cards of name 'name' to the deck. """

        for i in range(0, num):
            self.cards.append(Card(name))

    def shuffle(self):
        """ Shuffles the deck. """

        random.shuffle(self.cards)
