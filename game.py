#!/usr/bin/env python
import random

from deck import Deck
from card import Card, Mission, Character
from player import Player
import card_list
import mission_list
import character_list

import socket
import threading
import time

DECK_FILE = "expansion_cards"
CHAOS = False

class Game(object):
    """ Airlock game object """

    def __init__(self):
        self.players = []

    def main(self):
        """ Plays the game """

        if not self.load_settings(DECK_FILE):
            self.load_settings("base_cards") # Default option
        self.setup(CHAOS)
        while not self.reset:
            self.take_turn()

    def setup(self, chaos=False):
        """ Deals out roles, hands, and missions """
        for player in self.players:
            player.reset()
        self.msg_index = 0
        self.create_oxygen()
        self.create_decks()
        self.reset = False
        random.shuffle(self.players)
        self.live_players = self.players[:]
        # Create characters
        characters = Deck(self)
        for name in self.characters:
            character = self.load_card(name, character_list)
            if character:
                characters.add(character(self))
            else:
                print("Character not found: %s" % name)
        characters.shuffle()
        # Create missions
        missions = Deck(self)
        for name in self.missions if chaos else self.missions[:len(self.players)]:
            mission = self.load_card(name, mission_list)
            if mission:
                missions.add(mission(self))
            else:
                print("Mission not found: %s" % name)
        missions.shuffle()
        # Deal cards
        for player in self.players:
            player.mission = missions.draw()[0]
            player.character = characters.draw()[0]
            player.draw_up(2)
        self.active_player = self.players[0]
        self.draw_card(self.deck, self.command_pile)

    def add_player(self, name, socket = None):
        """ Adds a player of name 'name' to the game. """

        self.players.append(Player(self, name, socket = socket))

    def load_settings(self, file_name):
        """ Initializes deck from a text file """
        try:
            with open("%s.txt" % file_name, 'r') as file:
                self.missions = []
                self.characters = []
                self.cell_types = []
                self.cards = []
                text = file.read().split("\n")
                for line in text:
                    line = line.replace(" ","")
                    (key, value) = line.split(":")
                    args = value.split(",")
                    if key == "Oxygen":
                        self.cell_types += [arg[0] for arg in args]
                    elif key == "Missions":
                        self.missions += args
                    elif key == "Characters":
                        self.characters += args
                    else:
                        self.cards += [key for i in range(int(args[0]))]
        except:
            print("Could not read file: %s" % file_name)
            return False
        return True

    def create_decks(self):
        """ Creates the deck objects. """

        self.deck = Deck(self, "Deck", True)
        self.discard = Deck(self, "Discard")
        self.command_pile = Deck(self, "CommandPile")
        self.to_discard = Deck(self, "ToDiscard") # Cards to be discarded
        self.stage = Deck(self, "Stage") # Cards to be played
        self.global_permanents = Deck(self, "GlobalPermanents") # Includes cards like contaminate

    def create_oxygen(self):
        """ Creates the oxygen cells. """

        self.oxygen = len(self.cell_types)
        self.force_red = 0
        self.safe_next_turn = False
        self.oxygen_protected = False

    def damage_oxygen(self):
        """ Damages an oxygen cell. """

        self.oxygen -= 1
        print("Oxygen cell destroyed: %s cells remaining." % self.oxygen)
        self.publish(self.players, "oxygen", self.oxygen)
        if self.oxygen == 1:
            if self.check_martyr(False):
                self.damage_oxygen()
                return
        if self.oxygen == 0:
            if self.check_martyr(True):
                self.repair_oxygen()
            else:
                self.end_game(False)

    def repair_oxygen(self):
        """ Adds one to the oxygen supply. """

        self.oxygen += 1
        print("Oxygen cell restored: %s cells remaining." % self.oxygen)
        self.publish(self.players, "oxygen", self.oxygen)
        if self.oxygen == 1:
            if self.check_martyr(False):
                self.damage_oxygen()
                return

    def is_red_alert(self):
        """ Returns True if the current oxygen cell is a red alert cell """
        if self.force_red:
            return self.force_red > 0

        return self.cell_types[max(0,self.oxygen-1)].lower() == 'r'

    def take_turn(self):
        """ Carries out a single turn """
        player = self.active_player
        print("Start of " + player.name + "'s turn")
        # Start of turn effects
        if self.safe_next_turn:
            self.safe_next_turn = False
            self.oxygen_protected = True
        player.draw_up()
        for card in player.permanents.to_list():
            if hasattr(card, "on_turn_start"):
                card.on_turn_start()

        # Use abilities and patch malfunctions
        spent = self.main_phase(player)

        # Play cards into command pile
        self.request_card(player)
        allies = self.live_players[:]
        if player in allies:
            allies.remove(player)
        if player.next_ally:
            if player.next_ally.hand.size() and player.next_ally in self.live_players:
                allies = [player.next_ally]
        for ally in allies:
            if not ally.hand.size():
                allies.remove(ally)
        ally = player.prompt(allies, prompt_string = "Select an ally: ")
        if ally:
            self.request_card(ally)
        else:
            self.draw_card(self.deck, self.command_pile)
        self.draw_card(self.deck, self.command_pile)
        self.command_pile.shuffle()
        # Play cards from command pile
        self.draw_card(self.command_pile, self.stage, 3 if self.is_red_alert() else 2)
        self.draw_card(self.command_pile, self.to_discard, self.command_pile.size()-1)
        while self.stage.size():
            options = self.stage.to_list()
            max_priority = max([card.priority for card in options])
            for card in options[:]:
                if card.priority < max_priority:
                    options.remove(card)
            card = player.prompt(options,
                          prompt_string = "Choose first card to activate: ")
            print("Playing " + card.name)
            self.publish(self.players, "play", card)
            card.play()
            if self.reset:
                return

        # Use abilities and patch malfunctions
        self.force_red = 0
        if not spent and player in self.live_players:
            self.main_phase(player)

        # Discard
        for card in self.find_all_malfunctions():
            if hasattr(card, "on_discard"):
                card.on_discard()
        while self.to_discard.size():
            card = player.prompt(self.to_discard.to_list(), True,
                                 prompt_string = "Choose first card to discard: ")
            self.move_card(card, self.to_discard, self.discard)
        self.oxygen_protected = False

        # Check for game over
        if not self.deck.size():
            self.end_game(True)

        #   Go to the next player
        self.active_player = self.next_player(True)

    def main_phase(self, player):
        """ Gives player an opportunity to use energy """
        energy = player.permanents.count("Energy")
        if not energy:
            return False
        abilities = [name for name, value in player.character.abilities.items()
                     if energy >= value]
        if player.health < 2:
            abilities = []
        malfunctions = self.find_all_malfunctions()
        abstain = ["Pass"]
        choice = player.prompt(abilities+malfunctions+abstain,
                               prompt_string = "How do you wish to use your energy? ")
        if choice in malfunctions:
            player.permanents.find("Energy", replace = True)[0].destroy()
            if choice in self.global_permanents.to_list():
                pile = self.global_permanents
            else:
                pile = self.get_player(choice).permanents
            choice.patch()
            self.publish(self.players, "ability", "patch", self.active_player.name, pile, choice)
        elif choice in abilities:
            player.character.use_ability(choice)
        return choice != abstain[0]

    def move_card(self, card, deck1, deck2):
        """ Moves a card from deck1 to deck2 """
        if not card:
            return
        global_piles = [self.stage] + [p.permanents
                                       for p in self.players] + [self.global_permanents]
        if deck1 in global_piles or deck2 in global_piles:
            players = self.players[:]
            hidden = []
        else:
            players = []
            hidden = self.players[:]
            for player in self.players:
                if deck1 is player.hand or deck2 is player.hand:
                    players += [player]
                    hidden.remove(player)
        if len(players):
            self.publish(players, "move", deck1, deck2, card)
            if len(hidden):
                self.msg_index -= 1
        if len(hidden):
            self.publish(hidden, "move", deck1, deck2)
        deck2.add(deck1.remove(card))
        return card

    def move_all(self, deck1, deck2):
        """ Moves all cards from deck1 to deck2 """

        return self.draw_card(deck1, deck2, len(deck1.to_list()))

    def draw_card(self, deck1, deck2, num=1):
        """ Moves a given number of cards from deck1 to deck2 """

        return [self.move_card(card, deck1, deck2) for card in deck1.draw(num, True)]

    def next_player(self, skips = False):
        """ Make it the next player's turn. """

        # Change players
        i = self.players.index(self.active_player)
        for j in range(1,len(self.players)):
            successor = self.players[(i+j)%len(self.players)]
            if successor in self.live_players:
                if skips:
                    if successor.skipped:
                        successor.skipped = False
                    else:
                        return successor
                else:
                    return successor
        return self.active_player

    def request_card(self, player):
        """ Prompts target player to play a card into the command pile """

        if player.hand.size() > 0:
            card = player.prompt(player.hand.to_list(),
                                prompt_string = "Play a card facedown: ")
            self.move_card(card, player.hand, self.command_pile)
        else:
            self.draw_card(self.deck, self.command_pile)

    def kill(self, player):
        """ Removes a player from the game, ends game if needed """

        self.live_players.remove(player)
        print(player.name + " is dead!")
        self.publish(self.players, "kill", player, player.mission)
        player.mission.on_death()

    def find_permanent_card(self, name, excluded_player = None):
        """ Determines if a permanent card is in play """

        for player in self.live_players:
            if player != excluded_player:
                for card in player.permanents.to_list():
                    if card.name == name:
                        return card

        for card in self.global_permanents.to_list():
            if card.name == name:
                return card
        return None

    def get_player(self, card):
        """ Determines which player a card belongs to """
        for player in self.players:
            if card in player.permanents.to_list() + player.hand.to_list():
                return player
            if card is player.mission or card is player.character:
                return player
        return None

    def find_controller(self, perm_card):
        """ Returns the player class for whoever owns the permanent. """

        for player in self.live_players:
            for card in player.permanents.to_list():
                if card is perm_card:
                    return player
        return None


    def find_all_malfunctions(self):
        """ Returns a list of all malfunction cards currently in play. """

        malfunctions = []

        #   Looks through all malfunctions in player permanents
        for player in self.live_players:
            for card in player.permanents.to_list():
                if card.is_malfunction:
                    malfunctions.append(card)

        #   Looks through all malfunctions in global region
        for card in self.global_permanents.to_list():
            if card.is_malfunction:
                malfunctions.append(card)

        return malfunctions


    def check_martyr(self, crew = True):
        """ Determines if martyr exists, and acts accordingly """
        for player in self.live_players:
            for card in player.hand.to_list():
                if card.name == "Martyr":
                    if player.mission.is_red != crew:
                        self.move_card(card, player.hand, self.stage)
                        card.play()
                        if crew:
                            self.kill(player)
                            print("%s died to save the last oxygen cell" % player)
                        else:
                            print("%s died to destroy the last oxyge cell" % player)
                        return True
        return False


    def end_game(self, crew_won):
        """ Handle end of game cleanup """
        if self.reset:
            return # Too late!
        if crew_won:
            print("The crew was victorious!")
            self.publish(self.players, "win", "blue")
        else:
            print("The saboteur was victorious!")
            self.publish(self.players, "win", "red")
        self.reset = True

    def load_card(self, name, module=card_list):
        """ Returns constructor for instantiating a card """
        return getattr(module, name, False)


    def publish(self, players, event_type, *args):
        """ Sends a message to given players (None indicates all players) """
        arglist = ",".join([str(arg) for arg in args])
        message = "%d:%s:%s;" % (self.msg_index, event_type, arglist)

        #print(players,message) # TODO: send message
        self.msg_index += 1

        for player in players:
            print(player, message)
            num = self.player_to_number(player)
            sock = self.player_sockets[num]
            sock.send(message.encode())

    def server_init(self, ip):
        """ Returns a socket object to listen to players. """

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        IP_address = ip
        PORT = 52801

        server.bind((IP_address,PORT))
        server.listen(500)

        return server

######################### SERVER AND CONNECTION BELOW ##########################

    def player_to_number(self, player):
        """ Returns the player number based on player name. """

        print(player, [self.player_names[item] for item in self.player_names])
        for item in self.player_names:
            if self.player_names[item] == player.name:
                return item

    def wait_for_players(self):
        """ Waits for players to send IPs and names. Adds players to the game
        as they are received. """

        print("Waiting for players...")
        self.player_sockets = {}
        self.player_names = {}

        #   Open a socket to Google to find network ip
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self.ip = s.getsockname()[0]

        print("Server IP: %s" % self.ip)

        #   Initialize a socket
        self.server = self.server_init(self.ip)

        self.accepting_players = True
        player_thread = threading.Thread(target=self.accept_players)
        player_thread.start()

        msg = input("Press Enter to kick off.")
        while len(self.player_sockets) < 2:
            print("Need at least two players to start.")
            msg = input("Press Enter to kick off.")

        print("Waiting for all players to choose names:")

        while len(self.player_sockets) > len(self.player_names):
            pass

        print("The game has started!")
        print("Players: %s" % " ".join([self.player_names[i] for i in self.player_names]))

        self.send_player_list_to_sockets()


    def send_player_list_to_sockets(self):
        """ Sends a list of players to each socket as a string separated by
        slashes. """

        player_string = "/".join(self.player_names[i] for i in self.player_names)
        sockets = [self.player_sockets[i] for i in self.player_sockets]
        for socket in sockets:
            socket.send(player_string.encode())

    def accept_players(self):
        """ Thread to add players as they connect. """

        id = 1
        while self.accepting_players:
            conn, addr = self.server.accept()

            if not self.accepting_players:
                break   #   Kill if not accepting players anymore

            self.player_sockets[id] = conn
            conn.send(str(id).encode())
            print("Player %s added at %s." % (id, addr[0]))

            #   Listen for the player's name, but continue accepting connections
            a = threading.Thread(target=self.collect_name, args = (id, conn, addr))
            a.start()
            id += 1

    def collect_name(self, id, conn, addr):
        """ Collects the name for a player and compiles a list. """

        #   Listen for a name
        name = None
        while not name:
            msg = conn.recv(1024)
            if msg:
                name = msg.decode()

        #   Great! That's a name.
        self.player_names[id] = name
        print("%s has joined the game (Player %s)." % (name, id))
        self.add_player(name, socket = conn)


if __name__ == '__main__':
    game = Game()
    game.wait_for_players()
    time.sleep(1)
    while 1:
        game.main()
