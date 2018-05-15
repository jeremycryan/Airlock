#!/usr/bin/env python

from card_objects import Card

class CardName(Card):

    def __init__(self, game):
        name = 'cardname'
        Card.__init__(game, name)

    def play(self):
        """ Method that occurs on play """
        pass


class Rupture(Card):

    def __init__(self, game):
        name = 'Rupture'
        Card.__init__(game, name)

    def play(self):
        """ Method that occurs on play """

        #   Damage the ship if it isn't protected, or if it's red alert.
        if (not self.game.oxygen_protected) or (self.game.is_red_alert()):
            self.game.damage_oxygen()


class Recycle(Card):

    def __init__(self, game):
        name = 'Recycle'
        Card.__init__(game, name)

    def play(self):
        """ Method that occurs on play """

        #   Draw a card from the deck
        self.game.active_player.draw_from_deck(1)

        #   Active player discards a card
        self.game.active_player.discard()


class Impact(Card):

    def __init__(self, game):
        name = 'Impact'
        Card.__init__(game, name)

    def play(self):
        """ Method that occurs on play """

        #   Choose to damage character or oxygen supply
        choice = self.game.active_player.prompt(['Damage self',
            'Damage oxygen supply'],
            prompt_string = "Choose where to apply damage. ")


class Aftershock(Card):

    def __init__(self, game):
        name = 'Aftershock'
        Card.__init__(game, name)

    def play(self):
        """ Method that occurs on play """

        #   Choose to damage character or oxygen supply
        choice = self.game.active_player.prompt(['Damage self and discard %s' % self.name,
            'Return %s to command pile' % self.name],
            prompt_string = "Choose what to do with %s. " % self.name)
