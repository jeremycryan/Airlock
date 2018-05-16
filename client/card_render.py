#!/usr/bin/env python

from constants import *
from client_helpers import source_path as sp

#   Outside libraries
import pygame

#   Python libraries
from math import sqrt

class CardRender(object):
    """ Class for rendering individual cards. """

    def __init__(self, name, screen, pos = (0, 0), scale = 1.0):

        #   Set screen to blit everything to
        self.screen = screen
        self.scale = scale

        #   There may be some case where these are separate
        self.target_pos = pos
        self.render_pos = pos
        self.destroy_on_destination = False

        #   Movement parameters
        self.max_speed = 1500    #   Pixels (?) per second
        self.prop_accel = 3   #   Proportion of distance to target per second

        #   Generate image/surface
        self.name = name
        self.card_size = (int(CARD_WIDTH * scale), int(CARD_HEIGHT * scale))
        self.path = "%s.png" % name.lower()
        self.surface = self.generate_surface(self.path)

    def set_scale(self, new_scale):
        """ Changes the scale of the card. """

        self.scale = new_scale
        self.card_size = (int(CARD_WIDTH * new_scale), int(CARD_HEIGHT * new_scale))
        path = "%s.png" % self.name.lower()
        self.surface = self.generate_surface(path)

    def blank(self):
        """ Replaces object with a blank card in the same position. """

        return CardRender("Blank", self.screen, self.target_pos)

    def width(self):
        """ Width of the card. """
        return self.surface.get_width()

    def height(self):
        """ Height of the card. """
        return self.surface.get_height()

    def size(self):
        """ Returns a tuple of the card's width and height. """
        return (self.width(), self.height())

    def generate_surface(self, image_path):
        """ Generates the surface to represent the card on the screen """

        card_surface = pygame.Surface(self.card_size)

        #   Load image from path

        try:
            card_image = pygame.image.load(sp(image_path))
            card_image = pygame.transform.scale(card_image, self.card_size)
            return card_image

        #   If path not found, make a blank one instead
        except pygame.error:

            card_surface.fill((255, 255, 255))
            #   Generate text for the card name, but ignore if name starts with
            #   an underscore (use this for card backs)
            if self.name[0] != "_":
                string = self.generate_good_font(self.card_size, self.name, CARDFONT)
                card_surface.blit(string, (CARD_WIDTH/2 - string.get_width()/2,
                    CARD_HEIGHT/2 - string.get_height()/2))
            return card_surface

    def generate_good_font(self, max_dims, text, font, margin = 5,
        color = (0, 0, 0), min_size = 15, max_width = 999, max_height = 999):
        """ Generates a pygame font object such that it fits within the
        maximum dimensions. """

        size = min_size
        self.card_font = pygame.font.SysFont(font, size)
        string = self.card_font.render(text, 1, color)

        #   While the thing is small enough, make it bigger
        while string.get_width() < max_dims[0] - margin and \
            string.get_height() < max_dims[1] - margin and \
            string.get_width() < max_width and \
            string.get_height() < max_height:

            #   Generate a new surface and increase the size
            self.card_font = pygame.font.SysFont(font, size)
            string = self.card_font.render(text, 1, color)
            size += 1

        #   Make it slightly smaller than it was
        self.card_font = pygame.font.SysFont(font, size-2)
        string = self.card_font.render(text, 1, color)

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
        dist = self.to_go()

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

    def destroy_me(self):
        """ Determines whether this card wants to be destroyed. """

        if self.destroy_on_destination and self.to_go() < 1:
            return True

        return False

    def to_go(self):
        """ Distance between render position and actual position. """

        dx = self.render_pos[0] - self.target_pos[0]
        dy = self.render_pos[1] - self.target_pos[1]
        dist = (dx**2 + dy**2)**0.5
        return dist

    def send_pos(self):
        """ Position other cards should be thrown from. """
        return self.render_pos

    def receive_pos(self):
        """ Position other cards should be thrown to """
        return self.target_pos
