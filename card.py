#!/usr/bin/env python

class Card(object):
    """   An airlock card object """

    def __init__(self, game, name = 'energy'):
        self.game = game
        self.name = name

    def __repr__(self):
        return self.name
