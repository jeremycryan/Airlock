#!/usr/bin/env python

from constants import *
from log import Log
from card_render import CardRender
from deck_render import DeckRender
from card_array import CardArray
from oxygen_cells import OxygenCells
from player_summary import PlayerSummary
from client_helpers import source_path

#   Python libraries
import time
import random
from math import sin

#   Outside libraries
import pygame

class Client(object):

    def __init__(self):

        #   Initialize pygame
        pygame.init()
        pygame.mouse.set_visible(True)

        #   Actual screen
        self.screen_commit = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
        pygame.display.set_caption("Project Airlock")
        self.last_fps_blit = 0
        self.fps = 0
        self.zoomed_path = None

        #   Set up objects
        self.screen = pygame.Surface([WINDOW_WIDTH, WINDOW_HEIGHT])
        self.ui = pygame.Surface([SIDEBAR_WIDTH, WINDOW_HEIGHT])
        self.log = Log(self.ui)
        self.screen_offset = (0, 0)

        #   Screen shake settings
        self.anim = True
        self.shake_amp = 0
        self.shake_impulse = 300
        self.shake_muffle = 0.01
        self.shake_rate = 30

        self.cards = []
        self.decks = []

        self.msg_queue = []

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
        self.ui.fill((0, 0, 0))

        if troubleshoot:
            self.draw_troubleshoot()

    def get_hover_card(self):
        """ Returns the card the cursor is hovering over. """

        #   Get current mouse position
        x, y = pygame.mouse.get_pos()

        #   Look for cards in card arrays
        for card in self.cards[::-1]:
            if card.render_pos[0] < x and x < card.render_pos[0] + CARD_WIDTH:
                if card.render_pos[1] < y and y < card.render_pos[1] + CARD_HEIGHT:
                    return card

        #   Look for character cards
        for player in self.players:
            x_off = player.pos[0]
            y_off = player.pos[1]
            char_x = x_off + player.character_card.render_pos[0]
            char_y = y_off + player.character_card.render_pos[1]
            if char_x < x and x < char_x + CARD_WIDTH and char_y < y and y < char_y + CARD_HEIGHT:
                return player.character_card

        return False

    def update_pygame_events(self):
        """ Weird pygame stuff. Events don't happen unless you look at them. """
        for event in pygame.event.get():
            pass

    def assemble_players(self, player_list):
        """ Assumes the last item in player_list is the active player. Generates
        player objects for each in list. """

        self.players = []
        for idx, item in enumerate(player_list[:-1]):
            self.players.append(PlayerSummary(item, self.screen, pos=idx+1))
        self.players.append(PlayerSummary(player_list[-1], self.screen, pos=6,
            is_main_player = True))

    def parse_players(self, player_string, player_name):
        """ Parses the received player list and reorders the players such that
        the active player is at the end of the list. """

        players = player_string.split("/")

        #   Make sure active player is at the end
        pidx = players.index(player_name)
        players = players[pidx:] + players[:pidx]
        players += [players.pop(0)]

        #   Create player objects.
        self.assemble_players(players)


    def demo_card(self, player_string, player_name):
        """ Makes a card that jumps around the screen a bit. """

        self.parse_players(player_string, player_name)

        self.deck = DeckRender("Deck", self.screen, pos = DRAW_PILE_POS, deck_size = 50)
        self.discard = DeckRender("Discard", self.screen, pos = DISCARD_PILE_POS, deck_size = 0)
        self.command_pile = DeckRender("CommandPile", self.screen, pos = COMMAND_PILE_POS, deck_size = 0)
        self.to_discard = DeckRender("ToDiscard", self.screen, pos = TO_DISCARD_POS, deck_size = 0)
        self.decks.append(self.deck)
        self.decks.append(self.discard)
        self.decks.append(self.command_pile)
        self.decks.append(self.to_discard)
        self.generate_oxygen('bbbbrr', self.screen)

        self.stage = CardArray(STAGE_POS)
        self.hand = CardArray(HAND_POS, hand = True)

        self.generate_deck_dict()

        up = 0
        since_last = 0

        thing_list = ["Aftershock", "Deck", "Mission", "Unknown"] * 30

        send_froms = ["Deck", "Deck", "Ray Hand", "Ray Hand", "Deck"]*10
        send_tos = ["Ray Hand", "Ray Hand", "Discard", "Stage", "Jeremy Hand"]*10

        while True:
            self.update_pygame_events()
            nup = time.time()
            dt = nup - up
            up = nup
            since_last += dt

            self.draw_things(dt)

            new = time.time()
            if since_last > 1:
                since_last -= 1

                if since_last > 1:
                    since_last = 0

                if len(self.msg_queue):
                    print(self.msg_queue)
                    self.interpret_msg(self.msg_queue[0])
                #since_last -= 2
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

    def draw_things(self, dt):
        """ Draws essential items on the screen. """

        #   Clears the screen
        self.clear_screen(troubleshoot = True)

        #   Draw players, oxygen, and other cards
        for player in self.players:
            player.draw()
        self.oxygen.draw()
        self.update_card_movement(dt)
        self.draw_cards()

        #   Draw card preview and lighten selected card
        for card in self.cards[::-1]:
            card.lighten_amt = 0
        for card in [player.character_card for player in self.players]:
            card.lighten_amt = 0
        hovered = self.get_hover_card()
        if hovered:
            self.draw_preview(hovered)
            hovered.lighten_amt = 50

        #   Draw FPS and log on the side
        self.draw_fps(dt)
        self.log.draw()

        #   Commit items to screen and display
        self.update_screen(dt)

    def draw_preview(self, card):
        """ Draws a zoom-in of a card the player is hovering over. """
        try:
            if card:
                if self.zoomed_path != card.path:
                    self.zoomed = pygame.image.load(source_path(card.path))
                    self.zoomed = pygame.transform.scale(self.zoomed,
                        (int(LOG_WIDTH), int(7*LOG_WIDTH/5)))
                    self.zoomed_path = card.path
                self.ui.blit(self.zoomed, (LOG_XPOS, PREVIEW_MARGIN))
        except:
            pass

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

        #   Draw sidebar fill
        self.ui.fill((0, 40, 40))
        region = pygame.Surface((LOG_WIDTH, LOG_HEIGHT))
        region.fill((0, 50, 50))
        self.ui.blit(region, (LOG_XPOS, LOG_YPOS))

    def move_card(self, origin, destination, card = None,
        name = "Deck", destroy_on_destination = False):
        """ Renders a card moving from one deck to another. """

        #   These methods are relevant if the objects are decks.
        num = origin.remove_card(1, obj = card)
        destination.add_card(num)

        if num:

            #   TODO Make this if statement better, currently is super
            #   sketchy. More generally, make card arrays and decks
            #   work more similarly to each other.
            if card == None and hasattr(origin, "find_with_name"):
                card = origin.find_with_name(name)
                origin.send_pos(card)
            elif card == None:
                card = CardRender(name, self.screen, pos=origin.send_pos(name))
                self.cards.append(card)
            else:
                origin.send_pos(card)
            card.transform(name)
            card.move_to(destination.receive_pos(card))
            card.destroy_on_destination = destination.pile

    def generate_deck_dict(self):
        """ Links the name of a hand to the actual hand object. """

        self.deck_dict = {}

        #   Add basic piles
        self.deck_dict["Deck"] = self.deck
        self.deck_dict["Discard"] = self.discard
        self.deck_dict["Stage"] = self.stage
        self.deck_dict["ToDiscard"] = self.to_discard
        self.deck_dict["CommandPile"] = self.command_pile

        #   Add hands for players
        for player in self.players[:-1]:
            self.deck_dict["%s Hand" % player.name] = player.hand
        self.deck_dict["%s Hand" % self.players[-1].name] = self.hand

    def read_msg(self, msg):
        """ Reads the message and adds to queue. """

        split = msg.split(";")
        for item in split:
            self.msg_queue.append(item)

    def interpret_msg(self, msg):
        """ Does whatever the message says. """

        if msg in self.msg_queue:
            self.msg_queue.remove(msg)

        if msg == "":
            return
        split = msg.split(":")

        print(msg)
        #   What to do if the update type is "move"
        if split[1] == "move":
            params = split[2].split(",")
            origin = params[0]
            destination = params[1]
            if len(params) > 2:
                card = params[2]
            else:
                card = "Deck"

            #   Find objects for the deck names
            origin_obj = self.deck_dict[origin]
            dest_obj = self.deck_dict[destination]

            #   Determine whether object should be destroyed or not on
            #   being received

          # TODO destroy cards going to facedown piles

            self.log_print("Moving %s from %s to %s." % (card, origin, destination))
            self.move_card(origin_obj, dest_obj, name=card)

        #   What to do if the update type is "activate"
        elif split[1] == "play":

            #   TODO currently just flashes... maybe something more interesting?
            card = split[2]
            card_obj = self.stage.find_with_name(card)
            if hasattr(card_obj, "flash"):
                card_obj.flash()

            self.log_print("%s was played." % card)

        #   What to do if the update type is "ability"
        if split[1] == "ability":

            #   TODO again, currently just flashes the character card.
            new_split = split[2].split(",")
            ability = new_split[0]
            user = new_split[1]
            for player in self.players:
                if player.name == user:
                    player.character_card.flash()

            self.log_print("%s has used the %s ability." % (user.capitalize(), ability))
            if len(new_split) > 2:
                self.log_print("Targets: %s." % ", ".join(new_split[2:]))

        if split[1] == "oxygen":

            if int(split[2]) >= 0:
                while self.oxygen.count > int(split[2]):
                    self.log_print("An oxygen cell has been destroyed!")
                    self.destroy_oxygen()

                if int(split[2]) > self.oxygen.count:
                    diff = int(split[2]) - self.oxygen.count
                    self.log_print("%s oxygen cell%s restored.") % (int(diff),
                        "s"*(diff>1))
                    self.oxygen_count = int(split[2])

        if split[1] == "damage":

            msg = split[2].split(",")
            playername = msg[0]
            new_hp = int(msg[1])

            for player in self.players:
                if player.name == playername:
                    break

            if new_hp == 2:
                player.reveal_character(player.character)
                self.log_print("%s has been restored to health." % self.player.capitalize())
            if new_hp <= 1:
                player.reveal_character("%sDamaged" % player.character)
                self.log_print("%s has taken character damage." % player.name.capitalize())

        if split[1] == "kill":

            msg = split[2].split(",")
            playername = msg[0]
            mission = msg[1]

            for player in self.players:
                if player.name == playername:
                    break

            player.reveal_character("%sDamaged" % player.character)
            player.reveal_mission(mission)
            self.log_print("%s has died! Their mission has been revealed to be \
                %s." % (player.name.capitalize(), mission))

        if split[1] == "reveal":

            msg = split[2].split(",")
            playername = msg[0]
            mission = msg[1]

            for player in self.players:
                if player.name == playername:
                    break

            player.reveal_mission(mission)

            self.log_print("%s's mission has been revealed to be \
                %s." % (player.name.capitalize(), player.mission))

        if split[1] == "win":

            winners = split[2]
            self.log_print("The %s team has won!" % winners)


    def log_print(self, msg):
        """ Print the update to the log. """

        self.log.add_line(msg)


    def deck_name_to_object(self, deck_name):
        """ Finds the object given a deck's name. """

        return self.deck_dict[deck_name]


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
    client.demo_card("Jeremy/Paul/Daniel", "Jeremy")
