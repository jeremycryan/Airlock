#!/usr/bin/env python

class Card(object):
    """   An airlock card object """

    def __init__(self, game, name = 'energy'):
        self.game = game
        self.name = name
        self.hidden = True

    def __repr__(self):
        return self.name

    def visible_name(self):
        return "Unknown" if self.hidden else self.name
