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
        if (self.game.oxygen_protected == 0) or (self.game.is_red_alert()):
            self.game.damage_oxygen()

        self.resolve()
        

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

        #   Send card to correct zone
        if self.destination == 'discard':
            self.game.move_card(self, self.game.stage, self.game.to_discard)
        elif self.destination == 'command':
            self.game.move_card(self, self.game.stage, self.game.command_pile)


class HullBreach(Card):

    def __init__(self, game):
        name = 'Hull Breach'
        self.color = 'red'
        self.is_malfunction = True
        Card.__init__(self, game, name)
        self.patched = 0

    def __repr__(self):
        for player in self.game.live_players:
            if self in player.permanents.to_list():
                return "%s's %s" % (player, self.name)
        return self.name

    def play(self):
        """ Method that occurs on play """
        self.hidden = False
        self.resolve()

    def resolve(self):
        """ What happens after the card gets played """

        #   Send card to correct zone
        self.game.move_card(self, self.game.stage, self.game.active_player.permanents)


    def on_turn_start(self):
        """ This method is called at the start of the player's turn """

        #   Damage an oxygen cell at the start of every turn
        if not self.game.oxygen_protected:
            self.game.damage_oxygen()

    def destroy(self):
        """ Discards the malfunction from play. """

        owner = self.game.get_player(self)
        self.game.move_card(self, owner.permanents, self.game.to_discard)
        
    def patch(self):
        """ Patch the malfunction """
        self.patched += 1
        if self.patched >= 2:
            self.destroy()


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

        #   Remove card from stage and add to permanents
        self.game.move_card(self, self.game.stage, self.game.active_player.permanents)

    def destroy(self):
        """ Discards the card from play. """

        owner = self.game.get_player(self)
        self.game.move_card(self, owner.permanents, self.game.to_discard)
        

class Safeguard(Card):

    def __init__(self, game):
        name = 'Safeguard'
        self.color = 'blue'
        self.is_malfunction = False
        Card.__init__(self, game, name)

    def play(self):
        """ Method that occurs on play """
        self.hidden = False
        self.game.safe_next_turn = True
        self.resolve()


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
        salvaged.add(self.game.discard.draw(3, True))

        choice = self.game.active_player.prompt(salvaged.to_list(),
            prompt_string = "Choose a card to salvage. ")

        #   Shuffle the salvaged card into the deck
        self.game.move_card(choice, self.game.discard, self.game.deck)
        if choice:
            choice.hidden = True
        self.game.deck.shuffle()

        self.resolve()


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
        new_card = self.game.draw_card(self.game.deck, self.game.stage)[0]
        print("Playing " + new_card.name)
        self.game.publish(self.game.players, "play", new_card)
        new_card.play()
        self.resolve()


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
                self.game.move_card(to_worm, player.hand, wormed)

        #   Send wormhole to discard queue
        self.resolve()

        #   Add a card from the top of the deck
        self.game.draw_card(self.game.deck, wormed)

        #   Discard a card at random
        wormed.shuffle()
        self.game.draw_card(wormed, self.game.to_discard)

        #   Add wormhole cards to the stage
        cards = wormed.cards[:]
        self.game.move_all(wormed, self.game.stage)

        #   Play all cards in wormhole one by one
        while len(cards) > 0:
            to_play = self.game.active_player.prompt(cards,
                prompt_string = "Choose a card to resolve. ")
            cards.remove(to_play)

            #   Play the card only if it is red
            if to_play.color == 'red':
                self.game.publish(self.game.players, "play", to_play)
                to_play.play()
            else:
                to_play.resolve()


class Discharge(Card):

    def __init__(self, game):
        name = 'Discharge'
        self.color = 'red'
        self.is_malfunction = False
        Card.__init__(self, game, name)

    def play(self):
        """ Method that occurs on play """
        self.hidden = False
        current_player = self.game.active_player
        for player in self.game.live_players:
            if not player is current_player:
                for card in player.permanents.find('Energy', -1, True):
                    card.destroy()
        self.resolve()


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
        if choice:
            choice.destroy()
        self.resolve()


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
        self.game.move_card(self, self.game.stage, self.game.global_permanents)
        self.game.damage_oxygen()

    def destroy(self):
        """ Discards the card from play """

        self.game.move_card(self, self.game.global_permanents, self.game.to_discard)

        #   Restore the oxygen that was contaminated
        self.game.repair_oxygen()

    def patch(self):
        """ Patch the malfunction """
        self.destroy()


class Overrule(Card):

    def __init__(self, game):
        name = 'Overrule'
        self.color = 'blue'
        self.is_malfunction = False
        Card.__init__(self, game, name)

    def play(self):
        """ Method that occurs on play """
        self.hidden = False

        #   Choose a card in player's hand
        choice = self.game.active_player.prompt( \
            self.game.active_player.hand.to_list(),
            prompt_string = "Choose a card to play with Overrule. ")
        self.game.move_card(choice, self.game.active_player.hand, self.game.stage)
        #   Send overrule to discard queue
        self.resolve()

        #   Play the selected card
        if choice:
            self.game.publish(self.game.players, "play", choice)
            choice.play()

        # TODO: still play card from hand even if player has died


class EngineFailure(Card):

    def __init__(self, game):
        name = 'Engine Failure'
        self.color = 'red'
        self.is_malfunction = True
        Card.__init__(self, game, name)

    def play(self):
        """ Method that occurs on play """

        self.hidden = False
        self.resolve()

    def resolve(self):
        """ What happens after the card gets played """

        #   Remove the card from stage and add to player permanents
        self.game.move_card(self, self.game.stage, self.game.active_player.permanents)

    def on_discard(self):
        """ Method that affects behavior of discard phase """

        self.game.move_all(self.game.to_discard, self.game.deck)
        self.game.deck.shuffle()

    def on_turn_start(self):
        """ This method is called at the start of the player's turn """

        #   Remove the thing
        self.hard_destroy()

    def destroy(self):
        """ Discards the card from play """
        #   Remove card from play and send to discard queue
        self.game.move_card(self,self.game.get_player(self).permanents, self.game.to_discard)

    def hard_destroy(self):
        """ Discards the card from play, always sending to discard pile """

        #   Remove card from play and send to discard pile
        self.game.move_card(self,self.game.get_player(self).permanents, self.game.discard)

    def patch(self):
        """ Patch the malfunction """
        self.destroy()

class Inflict(Card):

    def __init__(self, game):
        name = 'Inflict'
        self.color = 'red'
        self.is_malfunction = False
        Card.__init__(self, game, name)

    def play(self):
        """ Method that occurs on play """
        self.hidden = False

        choice = self.game.active_player.prompt(["Take damage",
            "Reveal mission"],
            prompt_string = "What do you do with Inflict? ")

        #   Make them choose again if they can't reveal mission
        while choice == "Reveal mission" and \
            not self.game.active_player.mission.is_red:

            print("You can only reveal your mission if you are red.")
            choice = self.game.active_player.prompt(["Take damage",
                "Reveal mission"],
                prompt_string = "What do you do with Inflict? ")

        #   Execute the chosen action
        if choice == "Take damage":
            self.game.active_player.damage()
        elif choice == "Reveal mission":
            self.game.active_player.mission.visible = True
            self.game.publish(self.game.players, "reveal",
                              self.game.active_player, self.game.active_player.mission)
            print("%s has revealed as %s!" % (self.game.active_player,
                self.game.active_player.mission.name))

        self.resolve()


class Airlock(Card):

    def __init__(self, game):
        name = 'Airlock'
        self.color = 'green'
        self.is_malfunction = False
        Card.__init__(self, game, name)

    def play(self):
        """ Method that occurs on play """
        self.hidden = False

        votes = []

        #   Shuffle the player list to start with the active player
        player_list = self.game.live_players[:]
        if self.game.active_player in player_list:
            pos = player_list.index(self.game.active_player)
        else:
            pos = player_list.index(self.game.next_player())
        player_list = player_list[pos:] + player_list[:pos]

        #   Everybody cast your votes!
        for player in player_list:
            choice = player.prompt(self.game.live_players + ["Abstain"],
                prompt_string = "Who do you vote to kill? ")

            if choice == "Abstain":
                print("%s has abstained from the vote." % player)
            else:
                print("%s has voted to airlock %s." % (player, choice))
            votes.append(choice)
            player.character.on_vote(player)

        #   Determine who was most voted and kill that player
        for player in player_list:
            if votes.count(player) > len(player_list)/2.0:
                self.game.kill(player)
                print("%s has been thrown from the airlock." % player)
                break

        self.resolve()


class Execute(Card):

    def __init__(self, game):
        name = 'Execute'
        self.color = 'green'
        self.is_malfunction = False
        Card.__init__(self, game, name)

    def play(self):
        """ Method that occurs on play """
        self.hidden = False

        votes = []

        #   Shuffle the player list to start with the active player
        player_list = self.game.live_players[:]
        if self.game.active_player in player_list:
            pos = player_list.index(self.game.active_player)
        else:
            pos = player_list.index(self.game.next_player())
        player_list = player_list[pos:] + player_list[:pos]

        #   Nominate a player
        nominee = self.game.active_player.prompt(self.game.live_players,
            prompt_string = "Choose a player to execute. ")

        #   Everybody cast your votes!
        for player in player_list:
            choice = player.prompt(["Yes", "No"],
                prompt_string = "Vote to kill %s? " % nominee)

            if choice == "Yes":
                print("%s has voted to kill %s." % (player, nominee))
            else:
                print("%s has voted not to kill %s." % (player, nominee))

            votes.append(choice)
            player.character.on_vote(player)

        #   Determine whether the nominee dies or not
        if votes.count("Yes") > len(player_list)/2.0:
            self.game.kill(nominee)
            print("%s has been killed." % nominee)

        self.resolve()

