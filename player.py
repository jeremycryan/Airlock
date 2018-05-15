#!/usr/bin/env python

#   Python libraries
import random

from deck import Deck

class Player(object):
    """ Player object, in case you couldn't tell from the line above. """

    def __init__(self, game, name):
        self.health = 2
        self.game = game
        self.name = name
        self.hand = Deck(game)
        self.permanents = Deck(game)
        self.next_ally = None
        self.skipped = False
        self.mission = "Crew"
        self.color = "blue"


    def __repr__(self):
        return self.name


    def damage(self):
        """ Take damage to the player. """

        self.health -= 1
        print("Ouch! %s is at %s health." % (self.name, self.health))
        
        if self.health < 1:
            self.game.kill(self)


    def draw_from_deck(self, number):
        """ Draws a number of cards from the deck
        and adds them to the player's hand. """

        cards_drawn = self.game.deck.draw(number)
        self.hand.add(cards_drawn)


    def draw_up(self, handsize = 3):
        """ Draws up to the maximum hand size. """

        if self.hand.size() < handsize:
            self.draw_from_deck(handsize - self.hand.size())

    def discard(self, rand = False):
        """ Puts a card from the player's hand to the discard. """

        #   Don't discard if you have no cards in hand
        if self.hand.size() == 0:
            return

        #   Select the card to be discarded
        if rand:
            card_to_discard = random.choice(self.hand.to_list())
        else:
            card_to_discard = self.prompt(self.hand.to_list(),
                prompt_string = "Choose a card to discard. ")
            card_to_discard.hidden = False

        #   Remove the card from your hand and add it to the discard pile.
        self.hand.remove(card_to_discard)
        self.game.to_discard.add([card_to_discard])


    def prompt(self, choices, hidden = False, prompt_string = None):
        """ Somehow prompts the player to make a choice between items in a list.
        This could be through text or in a GUI. """

        #   TODO make this use a gui and generally be better

        if len(choices) == 1:
            return choices[0]
        elif len(choices) == 0:
            return None

        if prompt_string == None:
            prompt_string = 'Choose between: '
        if hidden:
            choice_strings = [c.visible_name() for c in choices]
        else:
            choice_strings = [str(c) for c in choices]
        print(prompt_string + ", ".join(choice_strings))
        choice = input()
        while choice not in choice_strings:
            if choice.isdigit():
                if int(choice) > 0 and int(choice) <= len(choices):
                    return choices[int(choice)-1]
            print("That's not a valid choice. Choose again.")
            choice = input()

        return choices[choice_strings.index(choice)]
