#!/usr/bin/env python

from constants import *
from card_render import CardRender

#   Python libraries
pass

#   Outside libraries
import pygame

class OxygenCells(object):

    def __init__(self, oxygen_profile, screen):

        #   Save screen to draw on later
        self.screen = screen

        #   Oxygen profile is the original oxygen cell configuration, in terms
        #   of red and blue alert cells. e.g. 'bbbbrr'

        #   Interpret oxygen_profile string
        decode = {'r': 'Red Cell', 'b': 'Blue Cell'}
        self.oxygen_profile = [decode[letter] for letter in oxygen_profile]
        self.start_count = len(self.oxygen_profile)
        self.count = self.start_count

        #   Get card objects for individual oxygen cells and put them on a
        #   surface for oxygen cells.
        self.oxygen_cards = []
        self.damaged_oxygen_cards = []
        surf_width = self.start_count//2 * CARD_WIDTH + \
            (self.start_count//2 - 1) * OXYGEN_SPACING
        surf_height = 2*CARD_HEIGHT + OXYGEN_SPACING
        self.oxygen_surface = pygame.Surface((surf_width, surf_height)).convert_alpha()

        self.generate_oxygen_cards()

        #   Makes a position for the surface
        x = int(OXYGEN_POS[0] - surf_width/2)
        y = int(OXYGEN_POS[1] - surf_height/2)
        self.pos = (x, y)

    def generate_oxygen_cards(self):
        """ Generates oxygen surfaces and adds them to self.oxygen_cards. """

        #   Create card object for each oxygen cell
        for idx, item in enumerate(self.oxygen_profile):
            xpos = idx%3 * CARD_WIDTH + idx%3 * OXYGEN_SPACING
            ypos = (CARD_HEIGHT + OXYGEN_SPACING) * (idx > 2)

            #   Separate surfaces for damaged and rendered oxygen cells.
            damaged = CardRender("Damaged", self.oxygen_surface, pos=(xpos, ypos))
            render = CardRender(item, self.oxygen_surface, pos=(xpos, ypos))
            self.damaged_oxygen_cards.append(damaged)
            self.oxygen_cards.append(render)


    def get_oxygen_surface(self):
        """ Returns a surface for the oxygen cells object """

        #   Fill the background as black
        self.oxygen_surface.fill(pygame.SRCALPHA)

        #   Draw each cell onto the surface, but make it damaged if it is
        #   damaged.

        for item in self.oxygen_cards[-self.count:]:
            item.draw()
        for item in self.damaged_oxygen_cards[:-self.count]:
            item.draw()
        if self.count == 0:
            for item in self.damaged_oxygen_cards[:]:
                item.draw()

        #   Return the surface
        return self.oxygen_surface

    def draw(self):
        """ Draws the oxygen cells on the screen object. """

        surf = self.get_oxygen_surface()
        surf.set_alpha(255)
        self.screen.blit(surf, self.pos)

    def destroy_oxygen(self, n = 1):
        """ Destroys a number of oxygen cell cards. A negative number will
        restore cells. """

        self.count = max(0, self.count - 1)
