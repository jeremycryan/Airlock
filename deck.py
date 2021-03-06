#!/usr/bin/env python

#   Python libraries
import random

#   Outside libraries
from card import Card


class Deck(object):
    """   A deck of airlock cards """

    def __init__(self, game, name = "temp", is_main_deck = False):
        self.game = game
        self.cards = []
        self.name = name
        if is_main_deck:
            self.populate()

    def __repr__(self):
        return self.name

    def populate(self):
        """ Adds the default deck. """

        for card in self.game.cards:
            self.create(card)
        self.shuffle()

    def create(self, name, num=1):
        """ Adds 'num' cards of name 'name' to the deck. """

        card = self.game.load_card(name)
        if not card:
            print("Card class not found: " + name)
            return
        for i in range(0, num):
            self.cards.append(card(self.game))

    def add(self, cards):
        """ Adds a list of cards to the deck. """

        if not hasattr(cards, "__iter__"):
            self.cards.append(cards)
        else:
            for card in cards:
                self.cards.append(card)

    def shuffle(self):
        """ Shuffles the deck. """

        random.shuffle(self.cards)
        self.game.publish(self.game.players, "shuffle", self)

    def draw(self, num=1, replace=False):
        """ Takes the top card(s) from the deck, as a list """

        if num < 1:
            return []
        if num > len(self.cards):
            num = len(self.cards)
        cards = self.cards[-num:]
        if not replace:
            self.cards = self.cards[:-num]
        return cards

    def select(self, index=-1, replace=False):
        """ Takes a specified card from the deck, as a list """

        if index >= len(self.cards) or index < -len(self.cards):
            return []
        card = self.cards[index]
        if replace:
            del self.cards[index]
        return [card]

    def remove(self, card):
        """ Takes a given card from the deck, as a list """
        if card in self.cards:
            self.cards.remove(card)
        else:
            if card:
                print("Card could not be discarded: " + str(card))
            return []
        return [card]

    def remove_all(self):
        """ Takes all cards from the deck, as a list """
        
        cards = self.cards
        self.cards = []
        return cards

    def to_list(self):
        """ Returns the cards in the deck, as a list """

        return self.cards[:]

    def size(self):
        """ Returns the number of cards in the deck """
        
        return len(self.cards)

    def count(self, name):
        """ Counts the occurences of specified card in the deck """

        return sum(card.name == name for card in self.cards)

    def find(self, name, num = 1, replace = False):
        """ Returns cards by name, num = -1 returns all instances """
        found = []
        for card in self.cards:
            if card.name == name:
                if num > len(found) or num < 0:
                    if not replace:
                        self.cards.remove(card)
                    found += [card]
        return found
