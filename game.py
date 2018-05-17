#!/usr/bin/env python
import random

from deck import Deck
from card import Card, Mission, Character
from player import Player
import card_list
import mission_list
import character_list

class Game(object):
    """ Airlock game object """

    def __init__(self):
        self.missions = ["Saboteur","Crew","Crew","Crew","Chancellor","Accomplice"]
        self.characters = ["Doctor","Captain","Navigator","Engineer","WeaponsExpert","Researcher"]
        self.players = []

    def main(self):
        """ Plays the game """

        self.setup()
        while not self.reset:
            self.take_turn()

    def setup(self, chaos=False):
        """ Deals out roles, hands, and missions """
        self.msg_index = 0
        self.create_oxygen()
        self.create_decks(True)
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

    def add_player(self, name):
        """ Adds a player of name 'name' to the game. """

        self.players.append(Player(self, name))

    def create_decks(self, expansion = True):
        """ Creates the deck objects. """

        self.deck = Deck(self, "Deck", expansion, True)
        self.discard = Deck(self, "Discard")
        self.command_pile = Deck(self, "CommandPile")
        self.to_discard = Deck(self, "ToDiscard") # Cards to be discarded
        self.stage = Deck(self, "Stage") # Cards to be played
        self.global_permanents = Deck(self, "GlobalPermanents") # Includes cards like contaminate


    def create_oxygen(self):
        """ Creates the oxygen cells. """

        self.oxygen = 6
        self.cell_types = ['r','r','b','b','b','b']
        self.force_red = False
        self.safe_next_turn = False
        self.oxygen_protected = False

    def damage_oxygen(self):
        """ Damages an oxygen cell. """

        self.oxygen -= 1
        print("Oxygen cell destroyed: %s cells remaining." % self.oxygen)
        self.publish(self.players, "oxygen", self.oxygen)
        if self.oxygen <= 0:
            self.end_game(False)
            # TODO: Check for martyr

    def repair_oxygen(self):
        """ Adds one to the oxygen supply. """

        self.oxygen += 1
        print("Oxygen cell restored: %s cells remaining." % self.oxygen)
        self.publish(self.players, "oxygen", self.oxygen)

    def is_red_alert(self):
        """ Returns True if the current oxygen cell is a red alert cell """

        return self.cell_types[self.oxygen-1] == 'r' or self.force_red

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
        #TODO nullify
        while self.stage.size():
            card = player.prompt(self.stage.to_list(),
                          prompt_string = "Choose first card to activate: ")
            print("Playing " + card.name)
            self.publish(self.players, "play", card)
            card.play()

        # Use abilities and patch malfunctions
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
        self.next_player()

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
        # TODO: Malfunctions repr should include player name
        abstain = ["Pass"]
        choice = player.prompt(abilities+malfunctions+abstain,
                               prompt_string = "How do you wish to use your energy? ")
        if choice in malfunctions:
            player.permanents.find("Energy")[0].destroy()
            choice.patch()
            if choice in self.global_permanents:
                pile = self.global_permanents
            else:
                pile = self.get_player(choice).permanents
            self.game.publish(self.players, "ability", "patch", pile, choice)
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

    def next_player(self):
        """ Make it the next player's turn. """

        # Change players
        i = self.players.index(self.active_player)
        for j in range(1,len(self.players)):
            successor = self.players[(i+j)%len(self.players)]
            if successor in self.live_players:
                if successor.skipped:
                    successor.skipped = False
                else:
                    self.active_player = successor
                    break

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


    def end_game(self, crew_won):
        """ Handle end of game cleanup """

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
        print(players,message) # TODO: send message
        self.msg_index += 1

if __name__ == '__main__':
    game = Game()
    game.add_player('Paul')
    game.add_player('Daniel')
    game.add_player('Jeremy')
    game.main()
