#!/usr/bin/env python

class Card(object):
    """   An airlock card object """

    def __init__(self, game, name = 'Energy'):
        self.game = game
        self.name = name
        self.hidden = True

    def __repr__(self):
        return self.name

    def visible_name(self):
        return "Unknown" if self.hidden else self.name

    def resolve(self):
        """ What happens after the card gets played """

        #   Remove card from stage and add to discard
        self.game.move_card(self, self.game.stage, self.game.to_discard)


class Mission(Card):
    """ Represents a player's Mission card """

    def __init__(self, game, name, can_die, is_red):
        Card.__init__(self, game, name)
        self.visible = False
        self.can_die = can_die
        self.is_red = is_red

    def on_death(self):
        """ Actions to carry out when the player dies """
        if self.game.get_player(self) is self.game.active_player:
            for card in self.game.active_player.hand.to_list():
                card.hidden = False
        self.game.move_all(self.game.get_player(self).hand, self.game.to_discard)
        self.game.move_all(self.game.get_player(self).permanents, self.game.to_discard)
        self.visible = True
        if not self.can_die:
            if self.is_red:
                self.game.end_game(True)
            else:
                self.game.end_game(False)


class Character(Card):
    """ Represents a player's Character card """

    def __init__(self, game, name):
        Card.__init__(self, game, name)
        self.abilities = {"Refresh":1}

    def on_vote(self, player):
        """ Promps player to use an ability during a vote """
        pass

    def use_ability(self, ability):
        """ Attempt to use a given ability """
        if ability in self.abilities:
            for energy in self.game.get_player(self).permanents.find(
                "Energy", self.abilities[ability], True):
                energy.destroy()
            getattr(self, ability.replace(" ","_").lower())()

    def refresh(self):
        self.game.active_player.discard()
        self.game.active_player.draw_from_deck(1)
        self.game.publish(self.game.players, "ability", "Refresh")
