#!/usr/bin/env python

from card import Card, Character
from deck import Deck

class Doctor(Character):
    def __init__(self, game):
        Card.__init__(self, game, "Doctor")
        self.abilities = {"Sedate":1, "Refresh":1}

    def sedate(self):
        pass
