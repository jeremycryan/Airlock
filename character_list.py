#!/usr/bin/env python

from card import Card, Character
from deck import Deck

class Doctor(Character):
    def __init__(self, game):
        Card.__init__(self, game, "Doctor")
        self.abilities = {"Sedate":1, "Refresh":1}

    def sedate(self):
        player = self.game.get_player(self)
        target = player.prompt(self.game.live_players[:])
        self.game.publish(self.game.players, "ability", "Sedate", target)
        target.skipped = True
