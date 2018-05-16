#!/usr/bin/env python

class CardArray(object):
    """ Class for rendering arrays of cards: e.g. a hand or stage. """

    def __init__(self, pos):

        #   Set initial position
        self.pos = pos
        self.cards = []

        
