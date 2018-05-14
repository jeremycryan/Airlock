#!/usr/bin/env python
from card_objects import Card, Deck

class Game(object):
    """ Airlock game object """

    def __init__(self):
        self.create_oxygen()
        self.create(self, True)


    def create_deck(self, expansion = True):
        """ Creates the deck. """

        self.deck = Deck(self, expansion)


    def create_oxygen(self):
        """ Creates the oxygen cells. """

        self.oxygen = ['red', 'red', 'blue', 'blue', 'blue', 'blue']
        self.force_red = False


    def is_red_alert(self):
        """ Returns True if the current oxygen cell is a red alert cell """

        return self.oxygen[-1] == 'red' or self.force_red


    def prompt(self, choices, prompt_string = None):
        """ Somehow prompts the player to make a choice between items in a list.
        This could be through text or in a GUI. """

        #   TODO make this use a gui and generally be better

        if prompt_string == None:
            prompt_string == 'Choose between: '

        print(prompt_string + str(choices))
        choice = input()

        while choice not in choices:
            print("That's not a valid choice. Choose again.")
            choice = input()
