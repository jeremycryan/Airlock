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


class Mission(Card):
    """ Represents a player's Mission card """

    def __init__(self, game, name, can_die, is_red):
        Card.__init__(self, game, name)
        self.visible = False
        self.can_die = can_die
        self.is_red = is_red

    def on_death(self):
        """ Actions to carry out when the player dies """
        self.to_discard.add(player.hand.remove_all())
        self.visible = True
        if not self.can_die:
            if self.is_red:
                self.game.end_game(True)
            else:
                self.game.end_game(False)


class Character(Card):
    """ Represents a player's Character card """

    def __init__(self, game):
        Card.__init__(self, game, "Grunt")
        self.abilities = {"Refresh":1}

    def on_vote(self, player):
        """ Promps player to use an ability during a vote """
        pass

    def use_ability(self, ability):
        """ Attempt to use a given ability """
        if ability in self.abilities:
            getattr(self, ability.replace(" ","_").lower())()

    def refresh(self):
        self.game.active_player.discard()
        self.game.active_player.draw_from_deck(1)
