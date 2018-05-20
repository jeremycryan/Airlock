#!/usr/bin/env python

from constants import *
from client_helpers import source_path as sp

#   Outside libraries
import pygame

#   Python libraries
from math import sqrt
from time import time

known_images = {}

class CardRender(object):
    """ Class for rendering individual cards. """

    def __init__(self, name, screen, pos = (0, 0), scale = 1.0):

        #   Set screen to blit everything to
        self.screen = screen
        self.scale = scale

        #   Alpha settings
        self.alpha = 255
        self.target_alpha = 255
        self.fade_rate = 155
        self.smoothing = 150    #   255 is crisp and sharp, 0 is disgustingly smooth

        #   There may be some case where these are separate
        self.target_pos = pos
        self.render_pos = pos
        self.destroy_on_destination = False
        self.pile = False
        self.display_type = "full"

        #   Movement parameters
        self.max_speed = 1200    #   Pixels (?) per second
        self.prop_accel = 3   #   Proportion of distance to target per second
        self.threshold = 1  #   Pixels away for "close enough"

        #   Generate image/surface
        self.name = name
        self.card_size = (int(CARD_WIDTH * scale), int(CARD_HEIGHT * scale))
        self.path = "%s.png" % name.lower()
        if known_images.get(self.path, 0):
            self.surface = known_images[self.path]
        else:
            self.surface = self.generate_surface(self.path)
        known_images[self.path] = self.surface

        #   Generate icon surface
        self.generate_icon_surface()

        #   Lighten effect
        self.lighten_amt = 0
        self.lighten_surface = pygame.Surface(self.card_size).convert()
        self.lighten_surface.fill((255, 255, 255))

        self.last_flash = 0
        self.since_flash = 999
        self.flash_period = 0.7
        self.flash_intensity = 600

    def generate_icon_surface(self):
        """ Generates a surface smaller than the original for use as an icon """

        self.icon_surface = pygame.Surface((int(CARD_WIDTH * 0.7),
            int(CARD_WIDTH * 0.7)))
        self.icon_surface.blit(self.surface, (int(-CARD_WIDTH * 0.3),
            int(-CARD_WIDTH * 0.3)))
        self.icon_surface = pygame.transform.scale(self.icon_surface,
            (int(CARD_WIDTH * 0.4), int(CARD_WIDTH * 0.4)))

    def transform(self, new_name):
        """ Changes into a different card graphically. """
        self.name = new_name
        self.path = "%s.png" % new_name.lower()
        self.surface = self.generate_surface(self.path)

        #   Load the image, only if it hasn't been loaded before.
        if known_images.get(self.path, 0):
            self.surface = known_images[self.path]
        else:
            self.surface = self.generate_surface(self.path)

    def set_scale(self, new_scale):
        """ Changes the scale of the card. """

        self.scale = new_scale
        self.card_size = (int(CARD_WIDTH * new_scale),
            int(CARD_HEIGHT * new_scale))
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
            card_image = pygame.image.load(sp(image_path)).convert()
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
        color = (0, 0, 0), min_size = 15, max_width = 999, max_height = 999,
        lock = False):
        """ Generates a pygame font object such that it fits within the
        maximum dimensions.

        min_size is the minimum font size allowed
        margin is the number of pixels free of the sides and top the final
            text must be
        if lock is true, only size min_size will be tested."""

        size = min_size
        self.card_font = pygame.font.SysFont(font, size)
        string = self.card_font.render(text, 1, color)

        if lock:
            return string

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

        #   Only move if the card is farther than the acceptable amount away.
        if dist > self.threshold:

            #   Calculate direction and speed
            if abs(dist) > 0:
                direc = (dx/dist, dy/dist)
            else:
                direc = (1, 0)
            speed = min(self.max_speed, dist*self.prop_accel)
            new_dx = direc[0] * speed
            new_dy = direc[1] * speed

            #   Update alpha value
            if self.target_alpha < self.alpha:
                self.alpha -= dt*self.fade_rate
            elif self.target_alpha > self.alpha:
                self.alpha += dt*self.fade_rate

            #   Change render position
            self.move_render(new_dx * dt, new_dy * dt)

    def set_alpha(self, alpha, hard = False):
        """ Sets the target alpha value for fades. Hard makes the transition
        instantaneous. """

        self.target_alpha = alpha

        if hard:
            self.alpha = alpha

    def flash(self):
        """ Flashes the card a lighter color briefly. """

        self.last_flash = time()

    def draw_flash(self):
        """ Draws the flash effect on the card. """

        #   Updates time-since-flash attribute
        self.since_flash = time() - self.last_flash

        if self.since_flash < self.flash_period:
            self.lighten_amt = min(self.since_flash,
                self.flash_period - self.since_flash) * self.flash_intensity
            print(self.since_flash, self.flash_period, self.lighten_amt)

    def draw(self):
        """ Draws the card on the screen based on its render position. """

        if self.display_type == "icon":
            new_surf = self.icon_surface.copy()
        else:
            new_surf = self.surface.copy()

        self.draw_flash()

        #   Camera smoothing
        self.screen.set_alpha(self.smoothing)

        #   Apply lighten effect
        self.lighten_surface.set_alpha(self.lighten_amt)
        new_surf.blit(self.lighten_surface.convert(), (0, 0))

        new_surf.set_alpha(self.alpha)

        self.screen.blit(new_surf, self.render_pos)

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

    def send_pos(self, card = None):
        """ Position other cards should be thrown from. """
        return self.render_pos

    def receive_pos(self, card = None):
        """ Position other cards should be thrown to """
        return self.target_pos
