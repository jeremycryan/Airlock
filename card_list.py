#!/usr/bin/env python

from card import Card

class CardName(Card):

    def __init__(self, game):
        name = 'cardname'
        color = 'green'
        Card.__init__(game, name)

    def play(self):
        """ Method that occurs on play """
        self.resolve()

    def resolve(self):
        """ What happens after the card gets played """

        #   Remove card from stage and add to discard
        self.game.stage.remove(self)
        self.game.to_discard.add(self)


class Rupture(Card):

    def __init__(self, game):
        name = 'Rupture'
        color = 'red'
        Card.__init__(game, name)

    def play(self):
        """ Method that occurs on play """

        #   Damage the ship if it isn't protected, or if it's red alert.
        if (not self.game.oxygen_protected) or (self.game.is_red_alert()):
            self.game.damage_oxygen()

        self.resolve()

    def resolve(self):
        """ What happens after the card gets played """

        #   Remove card from stage and add to discard
        self.game.stage.remove(self)
        self.game.to_discard.add(self)


class Recycle(Card):

    def __init__(self, game):
        name = 'Recycle'
        color = 'blue'
        Card.__init__(game, name)

    def play(self):
        """ Method that occurs on play """

        #   Draw a card from the deck
        self.game.active_player.draw_from_deck(1)

        #   Active player discards a card
        self.game.active_player.discard()

        self.resolve()

    def resolve(self):
        """ What happens after the card gets played """

        #   Remove card from stage and add to discard
        self.game.stage.remove(self)
        self.game.to_discard.add(self)


class Impact(Card):

    def __init__(self, game):
        name = 'Impact'
        color = 'red'
        Card.__init__(game, name)

    def play(self):
        """ Method that occurs on play """

        #   Choose to damage character or oxygen supply
        choice = self.game.active_player.prompt(['Damage self',
            'Damage oxygen supply'],
            prompt_string = "Choose where to apply damage. ")

        #   Execute choice
        if choice == 'Damage self':
            self.game.active_player.damage()
        elif choice == 'Damage oxygen supply':
            self.game.damage_oxygen()

        self.resolve()

    def resolve(self):
        """ What happens after the card gets played """

        #   Remove card from stage and add to discard
        self.game.stage.remove(self)
        self.game.to_discard.add(self)


class Aftershock(Card):

    def __init__(self, game):
        name = 'Aftershock'
        color = 'red'
        Card.__init__(game, name)

    def play(self):
        """ Method that occurs on play """

        #   Choose to damage character or oxygen supply
        choice = self.game.active_player.prompt(['Damage self',
            'Return %s to command pile' % self.name],
            prompt_string = "Choose what to do with %s. " % self.name)

        #   Execute choice
        if choice == 'Damage self':
            self.game.active_player.damage()
            self.destination = 'discard'
        else:
            self.destination = 'command'

        self.resolve()

    def resolve(self):
        """ What happens after the card gets played """

        #   Remove card from stage
        self.game.stage.remove(self)

        #   Send card to correct zone
        if self.destination == 'discard':
            self.game.to_discard.add(self)
        elif self.destination == 'command':
            self.game.command_pile.add(self)


class HullBreach(Card):

    def __init__(self, game):
        name = 'Hull Breach'
        color = 'red'
        Card.__init__(game, name)

    def play(self):
        """ Method that occurs on play """
        self.resolve()

    def resolve(self):
        """ What happens after the card gets played """

        #   Remove card from stage
        self.game.stage.remove(self)

        #   Send card to correct zone
        self.game.active_player.permanents.add(self)

    def on_turn_start(self):
        """ This method is called at the start of the player's turn """

        #   Damage an oxygen cell at the start of every turn
        if not self.game.oxygen_protected:
            self.game.damage_oxygen()


class Energy(Card):

    def __init__(self, game):
        name = 'Energy'
        color = 'blue'
        Card.__init__(game, name)

    def play(self):
        """ Method that occurs on play """
        self.resolve()

    def resolve(self):
        """ What happens after the card gets played """

        #   Remove card from stage and add to discard
        self.game.stage.remove(self)
        self.game.active_player.permanents.add(self)


class Safeguard(Card):

    def __init__(self, game):
        name = 'Safeguard'
        color = 'blue'
        Card.__init__(game, name)

    def play(self):
        """ Method that occurs on play """
        self.game.oxygen_protected = True
        self.resolve()

    def resolve(self):
        """ What happens after the card gets played """

        #   Remove card from stage and add to discard
        self.game.stage.remove(self)
        self.game.to_discard.add(self)


class Salvage(Card):

    def __init__(self, game):
        name = 'Salvage'
        color = 'blue'
        Card.__init__(game, name)

    def play(self):
        """ Method that occurs on play """

        #   Look at three cards from the discard
        salvaged = Deck(game)
        salvaged.add(self.game.discard.draw(3))

        choice = self.active_player.prompt(salvaged.to_list(),
            prompt_string = "Choose a card to salvage. ")

        #   Add the other cards back to the discard pile
        salvaged.remove(choice)
        self.game.discard.add(salvaged.to_list())

        #   Shuffle the salvaged card into the deck
        self.game.deck.add(choice)
        self.game.deck.shuffle()

        self.resolve()

    def resolve(self):
        """ What happens after the card gets played """

        #   Remove card from stage and add to discard
        self.game.stage.remove(self)
        self.game.to_discard.add(self)


class Override(Card):

    def __init__(self, game):
        name = 'Override'
        color = 'red'
        Card.__init__(game, name)

    def play(self):
        """ Method that occurs on play """

        #   Automatically play the top card of the deck
        new_card = self.game.deck.draw()[0]
        self.game.stage.add(new_card)
        new_card.play()
        self.resolve()

    def resolve(self):
        """ What happens after the card gets played """

        #   Remove card from stage and add to discard
        self.game.stage.remove(self)
        self.game.to_discard.add(self)
