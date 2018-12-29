#!/usr/bin/env python

from constants import *

#   outside libraries
import pygame

class ButtonArray(object):
    """ Makes an array of buttons with different names. """

    def __init__(self, screen, pos = (0, 0), max_dims = (100, 100)):

        self.options = []
        self.texted_options = []

        #   Set variables for width and height
        self.width = max_dims[0]
        self.height = max_dims[1]

        #   Set position
        self.pos = pos

        #   Surface to blit buttons onto
        self.back_surf = pygame.Surface(max_dims).convert()
        self.back_surf.set_alpha(120)
        self.front_surf = pygame.Surface(max_dims).convert_alpha()
        self.screen = screen

    def get_clicked(self, mouse_pos):
        """ Returns the option selected based on the position of the mouse. """

        #   Don't do anything if there are not options to draw
        if not len(self.options):
            return None

        spacing = 10
        num = len(self.options)
        total_space = spacing * (num - 1)
        height_each = int((self.height - total_space)/num)

        for idx, option in enumerate(self.options):

            #   Draw the button onto one surface
            x = self.pos[0]
            y = self.pos[1] + (spacing + height_each) * idx

            if x < mouse_pos[0] and mouse_pos[0] < x + self.width:
                if y < mouse_pos[1] and mouse_pos[1] < y + height_each:
                    return option

        return None

    def draw_rectangles(self):
        """ Draws the background rectangles for the buttons on the screen. """

        #   Don't do anything if there are not options to draw
        if not len(self.options):
            return None

        #   Parameters for drawing buttons
        spacing = 10
        num = len(self.options)
        total_space = spacing * (num - 1)
        height_each = int((self.height - total_space)/num)
        color = (255, 255, 255)

        for idx, option in enumerate(self.options):

            #   Draw the button onto one surface
            x = 0
            y = (spacing + height_each) * idx
            button_rect = (x, y, self.width, height_each)
            pygame.draw.rect(self.back_surf, color, button_rect)

            #   Draw the text onto another surface
            size = 30
            button_font = pygame.font.Font(BUTTONFONT, size)
            text_render = button_font.render(option, 1, (0, 0, 0))
            text_x = int(x + self.width/2 - text_render.get_width()/2)
            text_y = int(y + height_each/2 - text_render.get_height()/2)
            self.front_surf.blit(text_render, (text_x, text_y))

    def clear(self):
        """ Clears the array. """

        self.options = []

    def draw(self):
        """ Draws the buttons on the screen. """

        #   Draw background rectangles
        self.back_surf.fill(pygame.SRCALPHA)
        self.front_surf.fill(pygame.SRCALPHA)
        self.draw_rectangles()

        self.screen.blit(self.back_surf, self.pos)
        self.screen.blit(self.front_surf, self.pos)
