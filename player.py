#!/usr/bin/env python

#   Python libraries
import random

from deck import Deck

AUTO_PLAY = False

class Player(object):
    """ Player object, in case you couldn't tell from the line above. """

    def __init__(self, game, name, socket = None):
        self.health = 2
        self.game = game
        self.name = name
        self.socket = socket
        self.hand = Deck(game, "%s Hand" % name)
        self.permanents = Deck(game, "%s Permanents" % name)
        self.next_ally = None
        self.skipped = False
        self.mission = "Crew"
        self.color = "blue"

    def __repr__(self):
        return self.name


    def damage(self, num = 1):
        """ Take damage to the player. """

        self.health -= num
        if num > 0:
            print("Ouch! %s is at %s health." % (self.name, self.health))
        if num < 0:
            print("%s has been restored to %s health." % (self.name, self.health))
        self.game.publish(self.game.players, "damage", self, self.health)
        if self.health < 1 and self in self.game.live_players:
            self.game.kill(self)


    def draw_from_deck(self, number):
        """ Draws a number of cards from the deck
        and adds them to the player's hand. """

        self.game.draw_card(self.game.deck, self.hand, number)


    def draw_up(self, handsize = 3):
        """ Draws up to the maximum hand size. """

        if self.hand.size() < handsize:
            self.game.draw_card(self.game.deck, self.hand, handsize - self.hand.size())

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
        self.game.move_card(card_to_discard, self.hand, self.game.to_discard)


    def prompt(self, choices, hidden = False, prompt_string = None):
        """ Somehow prompts the player to make a choice between items in a list.
        This could be through text or in a GUI. """

        # Automatically choose at random to test for errors
        if AUTO_PLAY:
            if len(choices):
                return random.choice(choices)
            return choices

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

        # print(prompt_string + ", ".join(choice_strings))
        # choice = input()
        # while choice not in choice_strings:
        #     if choice.isdigit():
        #         if int(choice) > 0 and int(choice) <= len(choices):
        #             return choices[int(choice)-1]
        #     print("That's not a valid choice. Choose again.")
        #     choice = input()

        self.game.publish([self], "prompt", choice_strings)

        choice =  self.socket.recv(1024).decode()
        return choices[choice_strings.index(choice)]


    def reset(self):
        Player.__init__(self, self.game, self.name, socket = self.socket)
