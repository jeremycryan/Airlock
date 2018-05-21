#!/usr/bin/env python

from card_render import CardRender
from deck_render import DeckRender
from hand_render import HandRender
from permanents_render import PermanentsRender
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
        pos = 1,
        is_main_player = False):

        #   Name of the player
        self.name = name
        self.main_player = is_main_player
        self.name_surf = self.generate_name_surface()

        #   Reversed setting - should be true if summary is on right side
        self.reversed = reversed

        #   Surface to blit summary onto
        self.screen = screen
        self.player_number = pos
        self.pos = PLAYER_POSITIONS[pos]

        #   Create surface
        self.surf = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT), pygame.SRCALPHA)
        self.surf = self.surf.convert_alpha()

        #   Make a hand as a face-down deck
        hand_name = "%s Hand" % self.name
        self.hand = HandRender(hand_name, self.surf, pos = PLAYER_HAND_POS,
            deck_size = 0, owner = name, player_num = pos)

        #   Create mission and character cards
        self.mission = mission
        self.mission_card = CardRender(mission, self.surf,
            pos = (MISS_X, MISS_Y))
        self.character = character
        self.character_card = CardRender(character, self.surf,
            pos = (CHAR_X, CHAR_Y))

        #   Little row of permanent icons
        self.permanents = PermanentsRender(PERMANENTS_POS, self)


    def reveal_character(self, character):
        """ Reveals the player's character, or changes its state. """

        self.character_card = CardRender(character, self.surf,
            pos = (CHAR_X, CHAR_Y))


    def generate_name_surface(self):
        """ Generates a surface for the player's name. """

        color = (255, 255, 255)
        font = pygame.font.SysFont(PLAYERFONT, 40)
        string = font.render(self.name, 1, color)
        return string


    def reveal_mission(self, mission):
        """ Reveal's the player's mission, or changes its state. """

        self.mission_card = CardRender(mission, self.surf,
            pos = (MISS_X, MISS_Y))


    def draw_cards(self):
        """ Draws the character card on the player surface. """

        self.character_card.draw()
        self.mission_card.draw()

    def draw_name(self):
        """ Draws the player's name on the surface """

        self.surf.blit(self.name_surf,
            (PLAYER_NAME_POS[0] + self.surf.get_width()/2 - \
            self.name_surf.get_width()/2, PLAYER_NAME_POS[1]))


    def draw_hand(self):
        """ Draws the player's hand """

        self.hand.draw()

    def draw(self):
        """ Draws the player summary onto the screen """

        self.draw_cards()
        if not self.main_player: #   Main player has hand rendered elsewhere
            self.draw_hand()
        self.draw_name()
        self.screen.blit(self.surf, self.pos)
