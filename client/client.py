#!/usr/bin/env python

from constants import *
from card_render import CardRender
from oxygen_cells import OxygenCells

#   Python libraries
import time
import random

#   Outside libraries
import pygame

class Client(object):

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
        self.screen_commit = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])

        self.cards = []

    def generate_oxygen(self, oxygen_profile, screen):
        """ Generates an oxygen cell object. """
        self.oxygen = OxygenCells(oxygen_profile, screen)

    def main(self):
        """ Runs the main loop for the client """
        self.demo_card()

    def draw_cards(self):
        """ Draws all cards onto the screen. """

        for card in self.cards:
            card.draw()

    def update_card_movement(self, dt):
        """ Updates the position of all cards. """

        for card in self.cards:
            card.update_movement(dt)

    def clear_screen(self):
        """ Clears the screen to all black. """
        self.screen.fill((0, 0, 0))

    def demo_card(self):
        """ Makes a card that jumps around the screen a bit. """

        a = CardRender("Engine Failure", self.screen)
        self.generate_oxygen('bbbbrr', self.screen)

        up = time.time()
        since_last = 0

        while True:
            nup = time.time()
            dt = nup - up
            up = nup
            since_last += dt

            self.screen.fill((0, 0, 0))
            self.oxygen.draw()
            a.update_movement(dt)
            a.draw()
            self.draw_cards()

            pygame.display.flip()

            new = time.time()
            if since_last > 5:
                print("FPS: %s" % int(1/dt))
                if self.oxygen.count > 0:
                    self.oxygen.destroy_oxygen()
                since_last = 0
                a.move_to((random.randrange(0, WINDOW_WIDTH),
                    random.randrange(0, WINDOW_HEIGHT)))


if __name__ == '__main__':
    client = Client()
    client.main()
