#!/usr/bin/env python

from constants import *
from log import Log
from card_render import CardRender
from deck_render import DeckRender
from card_array import CardArray
from oxygen_cells import OxygenCells
from player_summary import PlayerSummary
from client_helpers import source_path
from button_array import ButtonArray

#   Python libraries
import time
import random
from math import sin
import sys

#   Outside libraries
import pygame

class Client(object):

    def __init__(self):

        #   Initialize pygame
        pygame.init()
        pygame.mouse.set_visible(True)

        #   Actual screen
        self.screen_commit = pygame.Surface([WINDOW_WIDTH, WINDOW_HEIGHT])
        self.real_display = pygame.display.set_mode([ALT_WINDOW_WIDTH,
                                                    ALT_WINDOW_HEIGHT])
        pygame.display.set_caption("Project Airlock")

        self.last_fps_blit = 0
        self.fps = 0
        self.zoomed_path = None

        #   Set up objects
        self.screen = pygame.Surface([WINDOW_WIDTH, WINDOW_HEIGHT])
        self.ui = pygame.Surface([SIDEBAR_WIDTH, WINDOW_HEIGHT])
        self.log = Log(self.ui)
        self.screen_offset = (0, 0)
        pygame.display.flip()

        #   Screen shake settings
        self.anim = True
        self.shake_amp = 0
        self.shake_impulse = 300
        self.shake_muffle = 0.01
        self.shake_rate = 30

        self.cards = []
        self.decks = []

        self.msg_queue = []
        self.prompt_options = None
        pygame.display.toggle_fullscreen ()


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

        player_chars = [player.character_card for player in self.players]
        player_missions = [player.mission_card for player in self.players]
        for card in self.cards + player_chars + player_missions:
            if not self.anim:
                card.move_render_to(card.target_pos)
            else:
                card.update_movement(dt)

        self.remove_extra_cards()

    def activate_card(self, card):
        """ Sends a response to the server that the card was selected, if the
        server is listening. """

        #   Check to see whether a card has been clicked at all
        if card:

            #   See if server is awaiting a response from the player, and that
            #   the card is a valid response
            if self.prompt_options:
                if card.name in self.prompt_options:

                    self.prompt_options = None
                    self.server_socket.send(card.name.encode())

                else:

                    self.log_print("%s is not a valid choice." % card.name)

    def activate_button(self, option):
        """ Sends a response to the surver that the button option was selected. """

        if option:
            if self.prompt_options:
                if option in self.prompt_options:
                    self.prompt_options = None
                    self.server_socket.send(option.encode())


    def clear_screen(self, troubleshoot = False):
        """ Clears the screen to all black. """
        self.screen.fill((0, 0, 0))
        self.ui.fill((0, 0, 0))

        if troubleshoot:
            self.draw_troubleshoot()

    def get_hover_card(self):
        """ Returns the card the cursor is hovering over. """

        #   Get current mouse position
        x, y = self.mouse_pos()

        for card in self.cards[::-1] + [player.character_card for player in self.players] + [player.mission_card for player in self.players]:
            card.is_hovered = False

        #   Look for cards in card arrays
        for card in self.cards[::-1]:
            if card.render_pos[0] < x and x < card.render_pos[0] + CARD_WIDTH:
                if card.render_pos[1] < y and y < card.render_pos[1] + CARD_HEIGHT:
                    card.is_hovered = True
                    return card

        #   Look for character cards
        for player in self.players:
            x_off = player.pos[0]
            y_off = player.pos[1]
            char_x = x_off + player.character_card.render_pos[0]
            char_y = y_off + player.character_card.render_pos[1]
            if char_x < x and x < char_x + CARD_WIDTH and char_y < y and y < char_y + CARD_HEIGHT:
                player.character_card.is_hovered = True
                return player.character_card
            miss_x = x_off + player.mission_card.render_pos[0]
            miss_y = y_off + player.mission_card.render_pos[1]
            if miss_x < x and x < miss_x + CARD_WIDTH and miss_y < y and y < miss_y + CARD_HEIGHT:
                player.mission_card.is_hovered = True
                return player.mission_card

        return False

    def update_pygame_events(self):
        """ Weird pygame stuff. Events don't happen unless you look at them. """
        self.clicked = False

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                self.clicked = True
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    print("AErgoierng")
                    self.real_display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                if event.key == pygame.K_ESCAPE:
                    self.real_display = pygame.display.set_mode([ALT_WINDOW_WIDTH,
                                                                ALT_WINDOW_HEIGHT])

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
        players = players[::-1]

        #   Make sure active player is at the end
        pidx = players.index(player_name)
        players = players[pidx:] + players[:pidx]
        players += [players.pop(0)]

        #   Create player objects.
        self.assemble_players(players)


    def demo_card(self, player_string, player_name):
        """ Makes a card that jumps around the screen a bit. """

        self.parse_players(player_string, player_name)

        #   Assemble decks
        self.generate_oxygen('bbbbrr', self.screen)
        self.deck = DeckRender("Deck", self.screen, pos = DRAW_PILE_POS, deck_size = 0)
        self.discard = DeckRender("Discard", self.screen, pos = DISCARD_PILE_POS, deck_size = 0)
        self.command_pile = DeckRender("Command Pile", self.screen, pos = COMMAND_PILE_POS, deck_size = 0)
        self.to_discard = DeckRender("To Discard", self.screen, pos = TO_DISCARD_POS, deck_size = 0)
        self.temp = DeckRender("Temporary", self.screen, pos = TEMP_POS, deck_size = 0)
        self.global_permanents = DeckRender("Contaminate", self.screen, pos = self.oxygen.most_recent_damaged_pos(), deck_size = 0, has_name = False)

        #   Add all of the decks to a list to render
        for deck in [self.deck, self.discard, self.command_pile, self.to_discard,
            self.temp, self.global_permanents]:
            self.decks.append(deck)

        #   Initialize a button array
        self.option_buttons = ButtonArray(self.ui, max_dims = OPTION_ARRAY_DIMS,
            pos = OPTION_ARRAY_POS)

        #   Initialize stage and hand
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
            dt = min(0.05, dt)
            up = nup
            since_last += dt

            self.draw_things(dt)

            new = time.time()

            #   If you have animations turned off, do all messages immediately.
            if not self.anim:
                self.flush_msg_queue()

            self.global_permanents.move_to(self.oxygen.most_recent_damaged_pos())

            #   Don't delay between prompt messages for usability
            if len(self.msg_queue):

                for i, item in enumerate(self.msg_queue):
                    if (":deck:" in item) or (":character:" in item) or (":reveal:" in item):
                        self.interpret_msg(item)
                        since_last = ACTION_LENGTH
                    if (":prompt:" in item):
                        self.interpret_msg(item)
                        since_last = ACTION_LENGTH
                                        
                #if ":prompt:" in self.msg_queue[0]:
                #    self.interpret_msg(self.msg_queue[0])

            #   Have a small delay between animating items.
            if since_last >= ACTION_LENGTH:
                since_last = 0

                #   If there is a message in the queue, execute it
                if len(self.msg_queue):
                    self.interpret_msg(self.msg_queue[0])

    def flush_msg_queue(self):
        """ Runs all commands in the message queue. """

        while len(self.msg_queue):
            self.interpret_msg(self.msg_queue[0])

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

        #   Make buttons for the choices the player needs to make
        if self.prompt_options:
            self.option_buttons.options = self.prompt_options
        else:
            self.option_buttons.clear()

        #   Draw card preview and lighten selected card
        for card in self.cards[::-1]:
            card.lighten_amt = 0
        for card in [player.character_card for player in self.players]:
            card.lighten_amt = 0
        for card in [player.mission_card for player in self.players]:
            card.lighten_amt = 0
            
        hovered = self.get_hover_card()
        button_hovered = self.button_hovered()
        if hovered:
            self.draw_preview(hovered)
            hovered.lighten_amt = max(50, hovered.lighten_amt)

        #   Activate cards that are clicked!
        if self.clicked and hovered:
            self.activate_card(hovered)
        elif self.clicked and button_hovered:
            self.activate_button(button_hovered)


        #   Draw FPS and log on the side
        self.draw_fps(dt)
        self.log.draw()

        #   Draw option buttons
        self.option_buttons.draw()

        #   Commit items to screen and display
        self.update_screen(dt)

    def button_hovered(self):
        """ Returns the option the mouse is hovering over, or None. """

        mouse_pos = self.mouse_pos()
        return self.option_buttons.get_clicked(mouse_pos)

    def mouse_pos(self):
        """ Returns the position of the mouse, accounting for
        screen scaling. """

        mp = pygame.mouse.get_pos()
        yscale = self.screen.get_height()/self.real_display.get_height()
        xscale = self.screen.get_width()/self.real_display.get_width()
        mouse_pos = (int(mp[0]*xscale), int(mp[1]*yscale))

        return mouse_pos

    def draw_preview(self, card):
        """ Draws a zoom-in of a card the player is hovering over. """
        try:
            if card:
                if self.zoomed_path != card.path:
                    self.zoomed = pygame.image.load(source_path(card.path))
                    self.zoomed = pygame.transform.smoothscale(self.zoomed,
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
        frame = pygame.transform.smoothscale(self.screen_commit,
            [self.real_display.get_width(),
            self.real_display.get_height()])
        self.real_display.blit(frame, [0, 0])
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

        #   FIXME get better solution to this problem. Malfunctions need the
        #   player name so they are distinguishable from each other, but adding
        #   the name in breaks everything that relies on the original card name.

        #   Strip out special cases where names break the thing
        if "Hull Breach" in name:
            name = "Hull Breach"

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
        self.deck_dict["temp"] = self.temp
        self.deck_dict["GlobalPermanents"] = self.global_permanents

        #   Add permanents piles for each player
        for player in self.players:
            self.deck_dict["%s Permanents" % player.name] = player.permanents

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

        #   What to do if the update type is "move"
        if split[1] == "move":
            params = split[2].split(",")
            origin = params[0]
            destination = params[1]
            if len(params) > 2:
                card = params[2]
            else:
                card = "Unknown"

            #   Find objects for the deck names
            origin_obj = self.deck_dict[origin]
            dest_obj = self.deck_dict[destination]

            #   Determine whether object should be destroyed or not on
            #   being received


            self.log_print("Moving %s from %s to %s." % (card, origin, destination))
            self.move_card(origin_obj, dest_obj, name=card)

        #   What to do if the update type is "activate"
        elif split[1] == "play":

            #   TODO currently just flashes... maybe something more interesting?
            card = split[2]
            card_obj = self.stage.find_with_name(card)
            if hasattr(card_obj, "flash") and self.anim:
                card_obj.flash()

            self.log_print("%s was played." % card)

        #   What to do if the update type is "ability"
        elif split[1] == "ability":

            #   TODO again, currently just flashes the character card.
            new_split = split[2].split(",")
            ability = new_split[0]
            user = new_split[1]
            for player in self.players:
                if player.name == user and self.anim:
                    player.character_card.flash()

            self.log_print("%s has used the %s ability." % (user.capitalize(), ability))
            if len(new_split) > 2:
                self.log_print("Targets: %s." % ", ".join(new_split[2:]))

        elif split[1] == "oxygen":

            if int(split[2]) >= 0:
                while self.oxygen.count > int(split[2]):
                    self.log_print("An oxygen cell has been destroyed!")
                    self.destroy_oxygen()

                if int(split[2]) > self.oxygen.count:
                    diff = int(split[2]) - self.oxygen.count
                    self.log_print("%s oxygen cell%s restored." % (int(diff),
                        "s"*(diff>1)))
                    self.oxygen.count = int(split[2])

        elif split[1] == "damage":

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

            #   Add a flash effect
            if self.anim:
                player.character_card.flash()

        elif split[1] == "kill":

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

        elif split[1] == "reveal":

            msg = split[2].split(",")
            playername = msg[0]
            mission = msg[1]

            for player in self.players:
                if player.name == playername:
                    break

            player.reveal_mission(mission)

            self.log_print("%s's mission has been revealed to be \
                %s." % (player.name.capitalize(), player.mission))

        elif split[1] == "character":

            msg = split[2].split(",")
            playername = msg[0]
            character = msg[1]

            for player in self.players:
                if player.name == playername:
                    break

            player.character = character
            player.reveal_character(character)

            self.log_print("%s has been dealt the %s card." % \
                (player.name.capitalize(), character))

        elif split[1] == "deck":

            self.deck.deck_size = int(split[2])
            self.deck.refresh_name_surface()
            self.log_print("The deck is starting with %s cards." % split[2])

        elif split[1] == "win":

            winners = split[2]
            self.log_print("The %s team has won!" % winners)
            pygame.quit()
            sys.exit()

        elif split[1] == "prompt":

            options = split[2]
            options = options.split(",")
            option_string = ", ".join(options)
            self.log_print("Choose between the following: %s." % option_string)
            self.prompt_options = options

        elif split[1] == "turn":

            player = split[2]
            self.log_print("%s has started their turn." % player.capitalize())
            #   TODO Add visual indicator for active player


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
        font = pygame.font.Font(PLAYERFONT, 25)
        string = font.render("FPS: %s" % self.fps, 1, color)
        self.ui.blit(string, (20, 20))


if __name__ == '__main__':
    client = Client()
    client.demo_card("Jeremy/Paul/Daniel", "Jeremy")
