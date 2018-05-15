#!/usr/bin/env python

from card import Card
from deck import Deck

class CardName(Card):

    def __init__(self, game):
        name = 'cardname'
        self.color = 'green'
        self.is_malfunction = False
        Card.__init__(self, game, name)

    def play(self):
        """ Method that occurs on play """
        self.hidden = False
        self.resolve()

    def resolve(self):
        """ What happens after the card gets played """

        #   Remove card from stage and add to discard
        self.game.stage.remove(self)
        self.game.to_discard.add(self)


class Rupture(Card):

    def __init__(self, game):
        name = 'Rupture'
        self.color = 'red'
        self.is_malfunction = False
        Card.__init__(self, game, name)

    def play(self):
        """ Method that occurs on play """

        #   Damage the ship if it isn't protected, or if it's red alert.
        self.hidden = False
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
        self.color = 'blue'
        self.is_malfunction = False
        Card.__init__(self, game, name)

    def play(self):
        """ Method that occurs on play """

        #   Draw a card from the deck
        self.hidden = False
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
        self.color = 'red'
        self.is_malfunction = False
        Card.__init__(self, game, name)

    def play(self, second_time = False):
        """ Method that occurs on play """

        #   Choose to damage character or oxygen supply
        self.hidden = False
        if self.game.active_player in self.game.live_players:
            choice = self.game.active_player.prompt(['Damage self',
                'Damage oxygen supply'],
                prompt_string = "Choose where to apply damage. ")
        else:
            choice = 'Damage oxygen supply'
        #   Execute choice
        if choice == 'Damage self':
            self.game.active_player.damage()
        elif choice == 'Damage oxygen supply':
            self.game.damage_oxygen()

        #    Do it again if in red alert!
        if (not second_time) and (self.game.is_red_alert()):
            self.play(second_time = True)
        else:
            self.resolve()

    def resolve(self):
        """ What happens after the card gets played """

        #   Remove card from stage and add to discard
        self.game.stage.remove(self)
        self.game.to_discard.add(self)


class Aftershock(Card):

    def __init__(self, game):
        name = 'Aftershock'
        self.color = 'red'
        self.is_malfunction = False
        Card.__init__(self, game, name)

    def play(self):
        """ Method that occurs on play """

        #   Choose to damage character or oxygen supply
        self.hidden = False
        if self.game.active_player in self.game.live_players:
            choice = self.game.active_player.prompt(['Damage self',
                'Return %s to command pile' % self.name],
                prompt_string = "Choose what to do with %s. " % self.name)
        else:
            choice = 'Return %s to command pile' % self.name
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
    #   TODO Make possible to patch

    def __init__(self, game):
        name = 'Hull Breach'
        self.color = 'red'
        self.is_malfunction = True
        Card.__init__(self, game, name)

    def play(self):
        """ Method that occurs on play """
        self.hidden = False
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

    def destroy(self):
        """ Discards the malfunction from play. """

        owner = self.game.find_controller(self)
        owner.permanents.remove(self)
        self.game.to_discard.add(self)


class Energy(Card):

    def __init__(self, game):
        name = 'Energy'
        self.color = 'blue'
        self.is_malfunction = False
        Card.__init__(self, game, name)

    def play(self):
        """ Method that occurs on play """
        self.hidden = False
        self.resolve()

    def resolve(self):
        """ What happens after the card gets played """

        #   Remove card from stage and add to discard
        self.game.stage.remove(self)
        self.game.active_player.permanents.add(self)

    def destroy(self):
        """ Discards the card from play. """

        owner = self.game.find_controller(self)
        owner.permanents.remove(self)
        self.game.to_discard.add(self)


class Safeguard(Card):

    def __init__(self, game):
        name = 'Safeguard'
        self.color = 'blue'
        self.is_malfunction = False
        Card.__init__(self, game, name)

    def play(self):
        """ Method that occurs on play """
        self.hidden = False
        self.safe_next_turn = True
        self.resolve()

    def resolve(self):
        """ What happens after the card gets played """

        #   Remove card from stage and add to discard
        self.game.stage.remove(self)
        self.game.to_discard.add(self)


class Salvage(Card):

    def __init__(self, game):
        name = 'Salvage'
        self.color = 'blue'
        self.is_malfunction = False
        Card.__init__(self, game, name)

    def play(self):
        """ Method that occurs on play """

        #   Look at three cards from the discard
        self.hidden = False
        salvaged = Deck(self.game)
        salvaged.add(self.game.discard.draw(3))

        choice = self.game.active_player.prompt(salvaged.to_list(),
            prompt_string = "Choose a card to salvage. ")

        #   Add the other cards back to the discard pile
        salvaged.remove(choice)
        self.game.discard.add(salvaged.to_list())

        #   Shuffle the salvaged card into the deck
        self.game.deck.add(choice)
        if choice:
            choice.hidden = True
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
        self.color = 'red'
        self.is_malfunction = False
        Card.__init__(self, game, name)

    def play(self):
        """ Method that occurs on play """

        #   Automatically play the top card of the deck
        self.hidden = False
        new_card = self.game.deck.draw()[0]
        self.game.stage.add(new_card)
        print("Playing " + new_card.name)
        new_card.play()
        self.resolve()

    def resolve(self):
        """ What happens after the card gets played """

        #   Remove card from stage and add to discard
        self.game.stage.remove(self)
        self.game.to_discard.add(self)


class Wormhole(Card):

    def __init__(self, game):
        name = 'Wormhole'
        self.color = 'red'
        self.is_malfunction = False
        Card.__init__(self, game, name)

    def play(self):
        """ Method that occurs on play """

        self.hidden = False
        wormed = Deck(self.game)

        #   TODO more efficient way to do this simultaneously so I don't have
        #   to wait for other players?
        #   Each player adds a card to the wormhole
        for player in self.game.live_players:
            to_worm = player.prompt(player.hand.to_list(),
                prompt_string = "Choose a card to put into the wormhole. ")
            if to_worm != None:
                player.hand.remove(to_worm)
                wormed.add(to_worm)

        #   Add a card from the top of the deck
        wormed.add(self.game.deck.draw())

        #   Discard a card at random
        wormed.shuffle()
        self.game.to_discard.add(wormed.draw())

        #   Add wormhole cards to the stage
        self.game.stage.add(wormed.to_list())

        #   Play all cards in wormhole one by one
        while len(wormed.to_list()) > 0:
            to_play = self.game.active_player.prompt(wormed.to_list(),
                prompt_string = "Choose a card to resolve. ")
            wormed.remove(to_play)

            #   Play the card only if it is red
            if to_play.color == 'red':
                to_play.play()
            else:
                to_play.resolve()

        self.resolve()

    def resolve(self):
        """ What happens after the card gets played """

        #   Remove card from stage and add to discard
        self.game.stage.remove(self)
        self.game.to_discard.add(self)


class Discharge(Card):

    def __init__(self, game):
        name = 'Discharge'
        self.color = 'red'
        self.is_malfunction = False
        Card.__init__(self, game, name)

    def play(self):
        """ Method that occurs on play """
        self.hidden = False

        #   Remove all energy from play that doesn't belong to active player
        while self.game.find_permanent_card('Energy',
            excluded_player = self.game.active_player):

            #   TODO Find a more efficient way to find and kill energy that
            #   doesn't involve looping through all permenents three times
            #   per iteration
            found_energy = self.game.find_permanent_card('Energy',
                excluded_player = self.game.active_player)
            found_energy.destroy()

        self.resolve()

    def resolve(self):
        """ What happens after the card gets played """

        #   Remove card from stage and add to discard
        self.game.stage.remove(self)
        self.game.to_discard.add(self)


class Repair(Card):

    def __init__(self, game):
        name = 'Repair'
        self.color = 'blue'
        self.is_malfunction = False
        Card.__init__(self, game, name)

    def play(self):
        """ Method that occurs on play """
        self.hidden = False

        malfunctions = self.game.find_all_malfunctions()
        choice = self.game.active_player.prompt(malfunctions,
            "Choose a malfunction to destroy. ")
        choice.destroy()
        self.resolve()

    def resolve(self):
        """ What happens after the card gets played """

        #   Remove card from stage and add to discard
        self.game.stage.remove(self)
        self.game.to_discard.add(self)


class Contaminate(Card):

    def __init__(self, game):
        name = 'Contaminate'
        self.color = 'red'
        self.is_malfunction = True
        Card.__init__(self, game, name)

    def play(self):
        """ Method that occurs on play """
        self.hidden = False
        self.resolve()

    def resolve(self):
        """ What happens after the card gets played """

        #   Remove card from stage and add to global permanents, and reduce the
        #   oxygen cell count by 1
        self.game.stage.remove(self)
        self.game.global_permanents.add(self)
        self.game.damage_oxygen()

    def destroy(self):
        """ Discards the card from play """

        self.game.global_permanents.remove(self)
        self.game.to_discard.add(self)

        #   Restore the oxygen that was contaminated
        self.game.repair_oxygen()
