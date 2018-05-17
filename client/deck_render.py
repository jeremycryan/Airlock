#!/usr/bin/env python

from card_render import CardRender
from constants import *

class DeckRender(CardRender):
    """ Class for rendering piles of cards. """

    def __init__(self, *args, **kwargs):

        #   Set deck size
        if "deck_size" in kwargs:
            self.deck_size = kwargs["deck_size"]
        else:
            self.deck_size = 0

        #   Call init for superclass
        print(args, kwargs)
        CardRender.__init__(self, args[0], args[1], pos = kwargs["pos"])

    def draw(self):
        """ Draws the card on the screen based on its render position. """

        #   Don't draw anything if there are no cards in the deck.
        if self.deck_size == 0:
            return

        #   Generate font objects
        string = self.generate_good_font(self.card_size,
            str(self.deck_size),
            DECKFONT,
            max_height = int(self.height()/3),
            min_size = 40)

        second_string = self.generate_good_font(self.card_size,
            str(self.deck_size),
            DECKFONT,
            max_height = int(self.height()/3),
            color = (255, 255, 255),
            min_size = 40)

        #   Draw deck size on the deck
        card_img = self.surface.copy()
        xpos = int(card_img.get_width()/2 - string.get_width()/2)
        ypos = int(card_img.get_height()/2 - string.get_height()/2)
        card_img.blit(string, (xpos + DECK_XOFF, ypos + DECK_YOFF))
        card_img.blit(second_string, (xpos + DECK_XOFF + DECK_STAGGER,
            ypos + DECK_YOFF + DECK_STAGGER))

        #   Blit to screen
        self.screen.blit(card_img, self.render_pos)

    def remove_card(self, n=1):
        """ Removes a number of cards from the deck. """

        self.deck_size -= n
        successfully_drawn = n

        #   Don't let the deck go below zero, that doesn't make sense
        if self.deck_size < 0:
            successfully_drawn = n - abs(self.deck_size)
            self.deck_size = 0

        return successfully_drawn
