#!/usr/bin/env python

from card_objects import Card

class CardName(Card):

    def __init__(self, game):
        name = 'cardname'
        Card.__init__(game, name)

    def play(self):
        pass
