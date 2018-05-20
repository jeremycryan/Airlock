#!/usr/bin/env python

from card_array import CardArray
from constants import *

class PermanentsRender(CardArray):
    """ Renders permanents (e.g. Energy, Hull Breach) as little circles. """

    def __init__(self, pos, player):

        #   Initialize the superclass
        CardArray.__init__(self, pos, hand=False)

        self.player_x = player.pos[0]
        self.player_y = player.pos[1]

    def receive_pos(self, card):
        """ Returns the position cards should be thrown to. Additionally
        modifies the positions of other cards to make room. """

        #   Change cards to icons on receive
        card.display_type = "icon"

        self.cards.append(card)
        self.correct_positions()

        return card.target_pos

    def send_pos(self, card):
        """ Returns the position cards should be thrown from. """

        #   Change cards to full display on exit
        card.display_type = "full"

        self.cards.remove(card)
        self.correct_positions()
        if self.hand:
            card.set_scale(1.0)
        return card.render_pos

    def get_correct_position(self, card):
        """ Determines what the x and y position of a card should be, based
        on its position in the array. """

        idx = self.cards.index(card)
        xpos = int(self.pos[0] - self.width()/5 + idx*(CARD_WIDTH*0.4 + \
            self.get_array_spacing()))
        ypos = int(self.pos[1] - self.height()/2)
        return (xpos + self.player_x, ypos + self.player_y)
