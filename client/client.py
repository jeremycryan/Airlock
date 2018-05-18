#!/usr/bin/env python

from constants import *
from card_render import CardRender
from deck_render import DeckRender
from card_array import CardArray
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
        self.last_fps_blit = 0
        self.fps = 0

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
        self.deck = DeckRender("Deck", self.screen, pos = DRAW_PILE_POS, deck_size = 20)
        self.discard = DeckRender("Discard", self.screen, pos = DISCARD_PILE_POS, deck_size = 0)
        self.cards.append(a)
        self.decks.append(self.deck)
        self.decks.append(self.discard)
        self.generate_oxygen('bbbbrr', self.screen)

        self.stage = CardArray(STAGE_POS)
        self.hand = CardArray(HAND_POS, hand = True)

        p1 = PlayerSummary("Paul", self.screen, pos = 1)
        p2 = PlayerSummary("Jeremy", self.screen, pos = 2)
        p3 = PlayerSummary("Daniel", self.screen, pos = 3)
        p4 = PlayerSummary("Adam", self.screen, pos = 4)
        p5 = PlayerSummary("Nick", self.screen, pos = 5)
        p6 = PlayerSummary("Ray", self.screen, pos = 6, is_main_player = True)
        self.players = [p1, p2, p3, p4, p5, p6]
        self.generate_deck_dict()

        up = 0
        since_last = 0

        thing_list = ["Aftershock", "Impact", "Mission", "Recycle", "Unknown"] * 30

        while True:
            nup = time.time()
            dt = nup - up
            up = nup
            since_last += dt

            self.clear_screen(troubleshoot = True)
            for player in self.players:
                player.draw()
            self.oxygen.draw()
            self.update_card_movement(dt)
            self.draw_cards()

            self.draw_fps(dt)
            self.update_screen(dt)

            new = time.time()
            if since_last > 2:
                since_last -= 2
                # if len(hand.cards) > 2:
                    #self.move_card(hand, stage, card = hand.cards[0], name = hand.cards[0].name)
                #self.move_card(deck, discard, name = "Discard")

                #self.move_card(deck, hand, name = thing_list.pop())
                #self.destroy_oxygen()
                # if len(hand.cards) < 3:
                #     since_last += 1.5
                # else:
                #     self.move_card(deck, p4.hand, name = "Aftershock", destroy_on_destination = True)
                # a.move_to((random.randrange(0, WINDOW_WIDTH),
                #    random.randrange(0, WINDOW_HEIGHT)))

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

        #   Draws boxes around player regions
        for player in self.players:
            player.surf.fill((60, 20, 60))

        #   Draw player summary region boundaries
        region = pygame.Surface((PLAYER_REGION_WIDTH, PLAYER_REGION_HEIGHT))
        region.fill((40, 0, 40))
        xpos = int(MID_X - PLAYER_REGION_WIDTH/2) + PLAYER_REGION_X
        ypos = int(MID_Y - PLAYER_REGION_HEIGHT/2) + PLAYER_REGION_Y
        self.screen.blit(region, (xpos, ypos))

        #   Fills player surfaces to distinguish from background

        #   Draw sidebar fill
        self.ui.fill((0, 40, 40))

    def move_card(self, origin, destination, card = None,
        name = "_DeckBack", destroy_on_destination = False):
        """ Renders a card moving from one deck to another. """

        #   These methods are relevant if the objects are decks.
        num = origin.remove_card(1, obj = card)
        destination.add_card(num)

        if num:
            if card == None:
                card = CardRender(name, self.screen, pos = origin.send_pos(card))
                self.cards.append(card)
            else:
                origin.send_pos(card)
            card.transform(name)
            card.move_to(destination.receive_pos(card))
            card.destroy_on_destination = destroy_on_destination

    def generate_deck_dict(self):
        """ Links the name of a hand to the actual hand object. """

        self.deck_dict = {}

        #   Add deck and discard
        self.deck_dict["Deck"] = self.deck
        self.deck_dict["Discard"] = self.discard

        #   Add hands for players
        for player in self.players:
            self.deck_dict["%s Hand" % player.name] = player.hand

    def interpret_msg(self, msg):
        """ Does whatever the message says. """

        split = msg.split(":")

        if split[1] == "move":
            params = split[2].split(",")
            origin = params[0]
            destination = params[1]
            if len(params) > 2:
                card = params[2]
            else:
                card = "Deck"


    def draw_fps(self, dt):
        """ Draws the frames per second on the screen. """

        t = time.time()
        if t - self.last_fps_blit > 0.1:
            self.fps = int(0.2*1/dt + 0.8*self.fps)
            self.last_fps_blit = time.time()
        color = (255, 255, 255)
        font = pygame.font.SysFont(PLAYERFONT, 25)
        string = font.render("FPS: %s" % self.fps, 1, color)
        self.ui.blit(string, (20, 20))


if __name__ == '__main__':
    client = Client()
    client.main()
