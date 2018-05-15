#!/usr/bin/env python
from deck import Deck
from card import Card
from player import Player

class Game(object):
    """ Airlock game object """

    def __init__(self):
        self.create_oxygen()
        self.create_decks(True)
        self.players = []
        self.active_player = None


    def main(self):
        """ Plays the game """

        print(self.deck)


    def add_player(self, name):
        """ Adds a player of name 'name' to the game. """

        self.players.append(Player(self, name))


    def create_decks(self, expansion = True):
        """ Creates the deck objects. """

        self.deck = Deck(self, expansion, True)
        self.discard = Deck(self)
        self.command_pile = Deck(self)
        self.to_discard = Deck(self) # Cards to be discarded
        self.stage = Deck(self) # Cards to be played


    def create_oxygen(self):
        """ Creates the oxygen cells. """

        self.oxygen = 6
        self.cell_types = ['r','r','b','b','b','b']
        self.force_red = False
        self.oxygen_protected = False

    def damage_oxygen(self):
        """ Damages an oxygen cell. """

        #   TODO consider end game situation
        self.oxygen -= 1

    def is_red_alert(self):
        """ Returns True if the current oxygen cell is a red alert cell """

        return self.oxygen[-1] == 'red' or self.force_red

    def take_turn(self):
        """ Carries out a single turn """
        player = self.active_player
        player.draw_up()
        for card in player.permanents:
            if card.hasattr("on_turn_start"):
                card.on_turn_start()
        self.request_card(player)
        allies = self.players[:]
        allies.remove(player)
        if player.next_ally:
            if len(player.next_ally.hand) and player.next_ally.health:
                allies = [player.next_ally]
        for ally in allies:
            if not len(ally.hand):
                allies.remove(ally)
        ally = player.prompt(allies, prompt_string = "Select an ally: ")
        self.request_card(ally)
        self.command_pile.add(self.deck.draw())
        self.command_pile.shuffle()
        self.stage = draw(self.command_pile, num = 3 if is_red_alert() else 2)
        for card in range():
            
            card.play()
            
    def request_card(self, player):
        """ Prompts target player to play a card into the command pile """
        if len(player.hand) > 0:
            self.command_pile.add(player.prompt(player.hand, \
                                prompt_string = "Play a card facedown: "))


if __name__ == '__main__':
    game = Game()
    game.add_player('Paul')
    game.add_player('Daniel')
    game.add_player('Jeremy')
    game.main()
