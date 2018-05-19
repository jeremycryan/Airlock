#!/usr/bin/env python

from deck_render import DeckRender
from constants import *

class HandRender(DeckRender):
    """ A deck class specifically for rendering player hands. """

    def __init__(self, *args, **kwargs):

        #   Set owner of the deck, if it's a hand
        if "owner" in kwargs:
            self.owner = kwargs["owner"]
        else:
            self.owner = None
        if "player_num" in kwargs:
            self.player_num = kwargs["player_num"]
        else:
            self.player_num = 1

        DeckRender.__init__(self, args[0], args[1],
            pos = kwargs["pos"], deck_size = kwargs["deck_size"])

        self.transform("Deck")
        self.set_scale(PLAYER_HAND_SCALE)
        self.darken_surface(100)

    def darken_surface(self, amt):
        """ Darkens the surface to be drawn """

        surf_copy = self.surface.copy().convert()
        surf_copy.set_alpha(100)
        self.surface.fill((0, 0, 0))
        self.surface.blit(surf_copy, (0, 0))


    def draw(self):
        """ Draws the card on the screen based on its render position. """

        #   Don't draw anything if there are no cards in the deck.
        if self.deck_size == 0:
            return

        #   Draw deck size on the deck
        card_img = self.surface.copy()
        xpos = int(card_img.get_width()/2 - self.num.get_width()/2)
        ypos = int(card_img.get_height()/2 - self.num.get_height()/2)
        card_img.blit(self.num, (xpos + DECK_XOFF,
            ypos + PLAYER_HAND_YOFF))
        card_img.blit(self.num_shadow, (xpos + DECK_XOFF + DECK_STAGGER,
            ypos + PLAYER_HAND_YOFF + DECK_STAGGER))

        #   Blit to screen
        self.screen.blit(card_img, self.render_pos)

    def send_pos(self, card = None):
        """ Position other cards should be thrown from. """

        xpos = int(PLAYER_POSITIONS[self.player_num][0] - CARD_WIDTH*self.scale/4)
        ypos = int(PLAYER_POSITIONS[self.player_num][1] - CARD_HEIGHT*self.scale/4)

        return (xpos, ypos)

    def receive_pos(self, card = None):
        """ Position other cards should be thrown to. """

        if card:
            if not hasattr(card, "deck_size"):
                card.set_alpha(0)
        #self.add_card(n=1, obj=card)

        return self.send_pos(card = card)
