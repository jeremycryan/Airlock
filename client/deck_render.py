#!/usr/bin/env python

from card_render import CardRender
from constants import *
import time

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

        self.num, self.num_shadow = self.generate_numbers()

    def generate_numbers(self):
        """ Generates the surfaces for deck count. """

        string = self.generate_good_font(self.card_size,
            str(self.deck_size),
            DECKFONT,
            max_height = int(self.height()/3),
            min_size = 55)

        second_string = self.generate_good_font(self.card_size,
            str(self.deck_size),
            DECKFONT,
            max_height = int(self.height()/3),
            color = (255, 255, 255),
            min_size = 55)

        return(string, second_string)

    def draw(self):
        """ Draws the card on the screen based on its render position. """

        #   Don't draw anything if there are no cards in the deck.
        if self.deck_size == 0:
            return


        #   Draw deck size on the deck
        card_img = self.surface.copy()
        xpos = int(card_img.get_width()/2 - self.num.get_width()/2)
        ypos = int(card_img.get_height()/2 - self.num.get_height()/2)
        card_img.blit(self.num, (xpos + DECK_XOFF, ypos + DECK_YOFF))
        card_img.blit(self.num_shadow, (xpos + DECK_XOFF + DECK_STAGGER,
            ypos + DECK_YOFF + DECK_STAGGER))

        #   Blit to screen
        self.screen.blit(card_img, self.render_pos)

    def remove_card(self, n=1, obj = None):
        """ Removes a number of cards from the deck. """

        self.deck_size -= n
        successfully_drawn = n

        #   Don't let the deck go below zero, that doesn't make sense
        if self.deck_size < 0:
            successfully_drawn = n - abs(self.deck_size)
            self.deck_size = 0

        #   Regenerate card number surfaces
        self.num, self.num_shadow = self.generate_numbers()

        return successfully_drawn

    def add_card(self, n=1, obj = None):
        """ Adds a card to the pile. """

        print("ADD %s" % n)
        self.deck_size += n
        self.num, self.num_shadow = self.generate_numbers()
