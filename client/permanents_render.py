#!/usr/bin/env python

from card_array import CardArray

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
        card.display_mode = "icon"

        self.cards.append(card)
        self.correct_positions()

        return (card.target_pos[0] + self.player_x,
            card.target_pos[1] + self.player_y)

    def send_pos(self, card):
        """ Returns the position cards should be thrown from. """

        #   Change cards to full display on exit
        card.display_mode = "full"

        self.cards.remove(card)
        self.correct_positions()
        if self.hand:
            card.set_scale(1.0)
        return card.render_pos
