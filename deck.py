#!/usr/bin/env python

#   Python libraries
import random

#   Outside libraries
import card_list
from card import Card


class Deck(object):
    """   A deck of airlock cards """

    def __init__(self, game, expansion = True, is_main_deck = False):
        self.game = game
        self.cards = []

        if is_main_deck:
            self.populate(expansion)

    def __repr__(self):
        return "Deck object containing %s cards." % len(self.cards)

    def populate(self, expansion = True):
        """ Adds the default deck. """

        #   Populates the deck
        self.add_card('Energy', 13)
        self.add_card('Impact', 7)
        self.add_card('Rupture', 5)
        self.add_card('Aftershock', 3)
        self.add_card('Salvage', 2)
        self.add_card('Safeguard', 2)
        self.add_card('HullBreach', 3)
        self.add_card('Recycle', 3)
        self.add_card('Airlock', 1)
        self.add_card('Martyr', 1)
        self.add_card('Override', 3)
        self.add_card('Overrule', 3)
        self.add_card('Discharge', 3)
        self.add_card('Wormhole', 2)

        #   Add expansion cards if expansion is enabled
        if expansion:
            self.add_card('EngineFailure', 2)
            self.add_card('Nullify', 3)
            self.add_card('Inflict', 2)
            self.add_card('Repair', 2)
            self.add_card('Contaminate', 2)
            self.add_card('Execute', 1)
            self.add_card('Shift', 3)

    def add_card(self, name, num=1):
        """ Adds 'num' cards of name 'name' to the deck. """

        card = getattr(card_list, name, False)
        if not card:
            print("Card class not found: " + name)
            return
        for i in range(0, num):
            self.cards.append(card(self.game))

    def add(self, cards):
        """ Adds a list of cards to the hand. """

        if not hasattr(cards, __iter__):
            self.cards.append(cards)
        else:
            for card in cards:
                self.cards.append(card)

    def shuffle(self):
        """ Shuffles the deck. """

        random.shuffle(self.cards)

    def draw(self, num=1, replace=False):
        """ Takes the top card(s) from the deck, as a list """

        if num > len(self.cards):
            num = len(self.cards)
        cards = self.cards[-num:]
        if replace:
            self.cards = self.cards[:-num]
        return cards

    def select(self, index=-1, replace=False):
        """ Takes a specified card from the deck """

        if index >= len(self.cards) or index < -len(self.cards):
            return []
        card = self.cards[index]
        if replace:
            del self.cards[index]
        return card

    def remove(self, card):
        """  """
        if card in self.cards:
            self.cards.remove(card)
        else:
            print("Card could not be discarded: " + str(card))

    def to_list(self):
        """ Returns the cards in the deck as a list """

        return self.cards[:]
