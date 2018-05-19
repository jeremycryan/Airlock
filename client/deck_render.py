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
        CardRender.__init__(self, args[0], args[1], pos = kwargs["pos"])

        self.num, self.num_shadow = self.generate_numbers()
        self.pile = True

        #   Generates surface for deck name
        self.name_surface = self.generate_name_surface()

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
        #   BUG shouldn't have to set alpha here, but for some reason the deck
        #   alpha changes when it sends cards to player hands.
        card_img.set_alpha(255)
        self.screen.blit(card_img, self.render_pos)

        ns_h = self.name_surface.get_height()
        ns_w = self.name_surface.get_width()
        self.screen.blit(self.name_surface,
            (int(self.render_pos[0] - ns_w/2 + CARD_WIDTH/2),
            int(self.render_pos[1] - ns_h/2 - 20)))

    def generate_name_surface(self):
        """ Generates a surface for the deck's name. """

        font = DECKFONT
        return self.generate_good_font(CARDSIZE, self.name, font,
            color = (120, 90, 120), min_size = 30, lock = True)

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

        self.deck_size += n
        self.num, self.num_shadow = self.generate_numbers()
