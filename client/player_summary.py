#!/usr/bin/env python

from card_render import CardRender
from constants import *

#   Outside libraries
import pygame

class PlayerSummary(object):
    """ Class for little gui elements that include all the stuff you need to
    know about a given person """

    def __init__(self, name, screen,
        character = "Character",
        mission = "Mission",
        reversed = False,
        pos = 1):

        #   Name of the player
        self.name = name

        #   Reversed setting - should be true if summary is on right side
        self.reversed = reversed

        #   Surface to blit summary onto
        self.screen = screen
        self.pos = PLAYER_POSITIONS[pos]

        #   Create surface
        self.surf = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))

        #   Create mission and character cards
        self.mission_card = CardRender(mission, self.surf,
            pos = (MISS_X, MISS_Y))
        self.character_card = CardRender(character, self.surf,
            pos = (CHAR_X, CHAR_Y))


    def reveal_character(self, character):
        """ Reveals the player's character, or changes its state. """

        self.character_card = CardRender(character, self.screen)


    def reveal_mission(self, mission):
        """ Reveal's the player's mission, or changes its state. """

        self.mission_card = CardRender(mission, self.screen)


    def draw_cards(self):
        """ Draws the character card on the player surface. """

        self.character_card.draw()
        self.mission_card.draw()

    def draw(self):
        """ Draws the player summary onto the screen """

        self.draw_cards()
        self.screen.blit(self.surf, self.pos)
