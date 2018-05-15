#!/usr/bin/env python

#   Python libraries
import random

from card_objects import Deck

class Player(object):
    """ Player object, in case you couldn't tell from the line above. """

    def __init__(self, game, name):
        self.alive = True
        self.game = game
        self.name = name
        self.hand = Deck(game)
        self.max_hand_size = 3


    def __repr__(self):
        return "Player: %s" % self.name


    def draw_from_deck(self, number):
        """ Draws a number of cards from the deck
        and adds them to the player's hand. """

        cards_drawn = self.game.deck.draw(number)
        self.hand.add(cards_drawn)


    def draw_up(self):
        """ Draws up to the maximum hand size. """

        self.draw_from_deck(self.max_hand_size - len(self.hand))

    def discard(self, rand = False):
        """ Puts a card from the player's hand to the discard. """

        #   Don't discard if you have no cards in hand
        if len(self.hand) == 0:
            return

        #   Select the card to be discarded
        if rand:
            card_to_discard = random.choice(self.hand)
        else:
            card_to_discard = self.prompt(self.hand,
                prompt_string = "Choose a card to discard. ")

        #   Remove the card from your hand and add it to the discard pile.
        self.hand.remove(card_to_discard)
        self.game.discard.add([card_to_discard])


    def prompt(self, choices, prompt_string = None):
        """ Somehow prompts the player to make a choice between items in a list.
        This could be through text or in a GUI. """

        #   TODO make this use a gui and generally be better

        if prompt_string == None:
            prompt_string == 'Choose between: '

        print(prompt_string + str(choices))
        choice = raw_input()

        while choice not in choices:
            print("That's not a valid choice. Choose again.")
            choice = raw_input()
