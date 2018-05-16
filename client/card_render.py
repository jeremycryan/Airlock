#!/usr/bin/env python

from constants import *
from client_helpers import source_path as sp

#   Outside libraries
import pygame

#   Python libraries
from math import sqrt

class CardRender(object):

    def __init__(self, name, screen, pos = (0, 0)):

        #   Set screen to blit everything to
        self.screen = screen

        #   There may be some case where these are separate
        self.target_pos = pos
        self.render_pos = pos

        #   Movement parameters
        self.max_speed = 1500    #   Pixels (?) per second
        self.prop_accel = 2   #   Proportion of distance to target per second

        #   Generate image/surface
        self.name = name
        self.card_size = CARDSIZE
        self.surface = self.generate_surface("%s.png" % name.lower())

    def blank(self):
        """ Replaces object with a blank card in the same position. """

        return CardRender("Blank", self.screen, self.target_pos)

    def generate_surface(self, image_path):
        """ Generates the surface to represent the card on the screen """

        card_surface = pygame.Surface(self.card_size)

        #   Load image from path
        try:
            card_image = pygame.image.load(sp(image_path)).blit(card_surface)
            card_image = pygame.transform.scale(card_image, self.card_size)
            return card_image

        #   If path not found, make a blank one instead
        except:
            card_surface.fill((255, 255, 255))
            #   Generate text for the card name
            string = self.generate_good_font(CARDSIZE, self.name, "None")
            card_surface.blit(string, (CARDSIZE[0]/2 - string.get_width()/2,
                CARDSIZE[1]/2 - string.get_height()/2))
            return card_surface

    def generate_good_font(self, max_dims, text, font):
        """ Generates a pygame font object such that it fits within the
        maximum dimensions. """

        size = 1
        self.card_font = pygame.font.SysFont(font, size)
        string = self.card_font.render(self.name, 1, (0, 0, 0))
        margin = 5

        #   While the thing is small enough, make it bigger
        while string.get_width() < max_dims[0] - margin and \
            string.get_height() < max_dims[1] - margin:

            #   Generate a new surface and increase the size
            self.card_font = pygame.font.SysFont(font, size)
            string = self.card_font.render(self.name, 1, (0, 0, 0))
            size += 1

        #   Make it slightly smaller than it was
        self.card_font = pygame.font.SysFont(font, size-2)
        string = self.card_font.render(self.name, 1, (0, 0, 0))

        return string


    def move(self, dx, dy):
        """ Moves the card's target position """
        pos = self.target_pos
        self.target_pos = (pos[0] + dx, pos[1] + dy)

    def move_to(self, pos):
        """ Moves the card to the position of choice """
        self.target_pos = pos

    def move_render(self, dx, dy):
        """ Moves the position of where the card is rendered """
        pos = self.render_pos
        self.render_pos = (pos[0] + dx, pos[1] + dy)

    def move_render_to(self, pos):
        """ Moves the card render to the position of choice """
        self.render_pos = pos

    def update_movement(self, dt):
        """ Moves the card closer to its target position """

        #   Find difference in render and target positions
        dx = self.target_pos[0] - self.render_pos[0]
        dy = self.target_pos[1] - self.render_pos[1]
        dist = sqrt(dx**2 + dy**2)

        #   Calculate direction and speed
        if abs(dist) > 0:
            direc = (dx/dist, dy/dist)
        else:
            direc = (1, 0)
        speed = min(self.max_speed, dist*self.prop_accel)
        new_dx = direc[0] * speed
        new_dy = direc[1] * speed

        #   Change render position
        self.move_render(new_dx * dt, new_dy * dt)

    def draw(self):
        """ Draws the card on the screen based on its render position. """

        self.screen.blit(self.surface, self.render_pos)
