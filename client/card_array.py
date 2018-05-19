#!/usr/bin/env python

from constants import *

# Python libraries
import random

class CardArray(object):
    """ Class for rendering arrays of cards: e.g. a hand or stage.

    This will almost always be a horizontal row of cards with uniform spacing """

    def __init__(self, pos, hand = False):

        #   Set initial position
        self.pos = pos
        self.cards = []
        self.hand = hand
        self.pile = False

        #   Maximum width of array object
        self.max_width = (CARD_WIDTH + ARRAY_SPACING) * 5

    def width(self):
        """ Returns the width of the array. """

        return min(len(self.cards) * CARD_WIDTH + (len(self.cards) - 1) * \
            ARRAY_SPACING, self.max_width)

    def height(self):
        """ Returns the height of the array. """

        #   For a horizontal row of cards, the height should be the same
        #   as that of a single card
        return CARD_HEIGHT

    def receive_pos(self, card):
        """ Returns the position cards should be thrown to. Additionally
        modifies the positions of other cards to make room. """

        self.cards.append(card)
        self.correct_positions()
        if self.hand:
            card.set_scale(HAND_SCALE)
        return card.target_pos

    def send_pos(self, card):
        """ Returns the position cards should be thrown from. """

        self.cards.remove(card)
        self.correct_positions()
        if self.hand:
            card.set_scale(1.0)
        return card.render_pos

    def find_with_name(self, name):
        """ Finds a card in the list with the given name. """

        #   If looking for a card with the same name, substitute them.
        for item in self.cards:
            if item.name == name:
                return item
        return False

    def correct_positions(self):
        """ Corrects the positions of all cards in array. """

        for card in self.cards:
            self.send_to_pos(card)

    def shuffle(self):
        """ Shuffles the hand around randomly!"""

        random.shuffle(self.cards)
        self.correct_positions()

    def send_to_pos(self, card):
        """ Sends a card to the correct position """

        card.move_to(self.get_correct_position(card))

    def get_correct_position(self, card):
        """ Determines what the x and y position of a card should be, based
        on its position in the array. """

        idx = self.cards.index(card)
        xpos = int(self.pos[0] - self.width()/2 + idx*(CARD_WIDTH + \
            self.get_array_spacing()))
        ypos = int(self.pos[1] - self.height()/2)
        return (xpos, ypos)

    def get_array_spacing(self):
        """ Gets the spacing between cards of the array, based on array size """

        prag_spacing = self.max_width
        if len(self.cards) > 1:
            prag_spacing = (self.max_width - len(self.cards) * CARD_WIDTH)\
                /(len(self.cards) - 1)
        return min(prag_spacing, ARRAY_SPACING)

    def remove_card(self, n=1, obj = None):
        """ This method does mostly nothing. """
        return min(n, len(self.cards))

    def add_card(self, n=1, obj = None):
        """ This method does mostly nothing. """
        return n
