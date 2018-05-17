#!/usr/bin/env python

from constants import *
from card_render import CardRender
from deck_render import DeckRender
from oxygen_cells import OxygenCells
from player_summary import PlayerSummary

#   Python libraries
import time
import random
from math import sin

#   Outside libraries
import pygame

class Client(object):

    def __init__(self):
        pygame.init()
        self.screen = pygame.Surface([WINDOW_WIDTH, WINDOW_HEIGHT])
        self.ui = pygame.Surface([SIDEBAR_WIDTH, WINDOW_HEIGHT])
        self.screen_offset = (0, 0)

        #   Screen shake settings
        self.anim = True
        self.shake_amp = 0
        self.shake_impulse = 300
        self.shake_muffle = 0.01
        self.shake_rate = 30

        #   Actual screen
        self.screen_commit = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
        pygame.display.set_caption("Project Airlock")

        self.cards = []
        self.decks = []

    def generate_oxygen(self, oxygen_profile, screen):
        """ Generates an oxygen cell object. """
        self.oxygen = OxygenCells(oxygen_profile, screen)

    def main(self):
        """ Runs the main loop for the client """
        self.demo_card()

    def remove_extra_cards(self):
        """ Removes all cards that want to be removed. """

        to_remove = []
        for card in self.cards:
            if card.destroy_me():
                to_remove.append(card)
        for item in to_remove:
            self.cards.remove(item)

    def draw_cards(self):
        """ Draws all cards and decks onto the screen. """

        for item in self.cards + self.decks:
            item.draw()

    def update_card_movement(self, dt):
        """ Updates the position of all cards. """

        for card in self.cards:
            if not self.anim:
                card.move_render_to(card.target_pos)
            else:
                card.update_movement(dt)

        self.remove_extra_cards()

    def clear_screen(self, troubleshoot = False):
        """ Clears the screen to all black. """
        self.screen.fill((0, 0, 0))

        if troubleshoot:
            self.draw_troubleshoot()

    def demo_card(self):
        """ Makes a card that jumps around the screen a bit. """

        a = CardRender("Aftershock", self.screen)
        d = DeckRender("Deck", self.screen, pos = DRAW_PILE_POS, deck_size = 10)
        self.cards.append(a)
        self.decks.append(d)
        self.generate_oxygen('bbbbrr', self.screen)

        p1 = PlayerSummary("Paul", self.screen, pos = 1)
        p2 = PlayerSummary("Jeremy", self.screen, pos = 2)
        p3 = PlayerSummary("Daniel", self.screen, pos = 3)
        p4 = PlayerSummary("Adam", self.screen, pos = 4)
        p5 = PlayerSummary("Nick", self.screen, pos = 5)
        p6 = PlayerSummary("Ray", self.screen, pos = 6)

        up = time.time()
        since_last = 0

        while True:
            nup = time.time()
            dt = nup - up
            up = nup
            since_last += dt

            self.clear_screen(troubleshoot = True)
            for player in [p1, p2, p3, p4, p5, p6]:
                player.draw()
            self.oxygen.draw()
            self.update_card_movement(dt)
            self.draw_cards()

            self.update_screen(dt)

            new = time.time()
            if since_last > 2:
                self.move_card(a, d, name = "Mission", destroy_on_destination = 1)
                print("FPS: %s" % int(1/dt))
                self.destroy_oxygen()
                d.remove_card(2)
                since_last = 0
                a.move_to((random.randrange(0, WINDOW_WIDTH),
                    random.randrange(0, WINDOW_HEIGHT)))

    def destroy_oxygen(self):
        """ Destroys an oxygen cell and applies a camera shake. """

        self.oxygen.destroy_oxygen()

        #   Shake camera if animations are enabled
        if self.anim:
            self.shake_amp = 50


    def update_screen(self, dt):
        """ Draws the screen onto the other screen then does the thing. """

        #   Update camera shake
        self.update_camera_shake(dt)

        #   blit fake screen onto real screen
        self.screen_commit.blit(self.screen, (self.screen_offset))
        self.screen_commit.blit(self.ui, (0, 0))
        pygame.display.flip()

    def update_camera_shake(self, dt):
        """ Updates the camera shake. """

        #   Apply camera shake
        t = time.time()
        self.shake_amp *= self.shake_muffle**dt
        self.screen_offset = (sin(t*self.shake_rate)**2 * self.shake_amp,
            sin(t*self.shake_rate)**2 * self.shake_amp)

    def draw_troubleshoot(self):
        """ Draws regions for easier troubleshooting. """

        #   Draw player summary region boundaries
        region = pygame.Surface((PLAYER_REGION_WIDTH, PLAYER_REGION_HEIGHT))
        region.fill((40, 0, 40))
        xpos = int(MID_X - PLAYER_REGION_WIDTH/2) + PLAYER_REGION_X
        ypos = int(MID_Y - PLAYER_REGION_HEIGHT/2) + PLAYER_REGION_Y
        self.screen.blit(region, (xpos, ypos))

        #   Draw sidebar fill
        self.ui.fill((0, 40, 40))

    def move_card(self, origin, destination, card = None,
        name = "_DeckBack", destroy_on_destination = False):
        """ Renders a card moving from one deck to another. """

        if card == None:
            card = CardRender(name, self.screen, pos = origin.send_pos())
            self.cards.append(card)

        card.move_to(destination.receive_pos())
        card.destroy_on_destination = destroy_on_destination


if __name__ == '__main__':
    client = Client()
    client.main()
