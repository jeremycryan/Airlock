#!/usr/bin/env python

from card import Character
from deck import Deck

class Doctor(Character):
    def __init__(self, game):
        Character.__init__(self, game, "Doctor")
        self.abilities["Sedate"] = 1

    def sedate(self):
        player = self.game.get_player(self)
        target = player.prompt(self.game.live_players[:],
                               prompt_string = "Who do you choose to skip?")
        self.game.publish(self.game.players, "ability", "Sedate", target)
        target.skipped = True

class Captain(Character):
    def __init__(self, game):
        Character.__init__(self, game, "Doctor")
        self.abilities["Command"] = 1

    def command(self):
        player = self.game.get_player(self)
        target1 = player.prompt(self.game.live_players[:],
                                prompt_string = "Who do you choose to command?")
        target2 = player.prompt(self.game.live_players[:],
                                prompt_string = "Who must %s ally with next turn?" % target1)
        self.game.publish(self.game.players, "ability", "Command", target1, target2)
        target1.next_ally = target2

class Navigator(Character):
    def __init__(self, game):
        Character.__init__(self, game, "Navigator")
        self.abilities["Maneuver"] = 1

    def maneuver(self):
        self.game.publish(self.game.players, "ability", "maneuver")
        player = self.game.get_player(self)
        temp = Deck(self.game)
        self.game.draw_card(self.game.deck, temp, 3)
        options = temp.to_list()
        if len(options) < 3:
            options += ["None"]
        command = player.prompt(options,
                                prompt_string = "Which card do you add to the command pile?")
        if command != "None":
            self.game.move_card(command, temp, self.game.command_pile)
            options.remove(command)
        elif len(options) == 3: # Player had 2 choices
            options.remove(command)
        discard = player.prompt(options,
                                prompt_string = "Which card do you discard?")
        if discard != "None":
            self.game.move_card(discard, temp, self.game.discard)
        self.game.move_all(temp, self.game.deck)

class Engineer(Character):
    def __init__(self, game):
        Character.__init__(self, game, "Engineer")
        self.abilities["Teleport"] = 1

    def teleport(self):
        player = self.game.get_player(self)
        target1 = player.prompt(self.game.live_players[:],
                                prompt_string = "Select first player.")
        target2 = player.prompt(self.game.live_players[:],
                                prompt_string = "Select second player.")
        self.game.publish(self.game.players, "ability", "Teleport", target1, target2)
        temp = target1.permanents.to_list()
        self.game.move_all(target2.permanents, target1.permanents)
        for card in temp:
            self.game.move_card(card, target1.permanents, target2.permanents)

class WeaponsExpert(Character):
    def __init__(self, game):
        Character.__init__(self, game, "Weapons Expert")
        self.abilities["Disarm"] = 1

    def disarm(self):
        player = self.game.get_player(self)
        target = player.prompt(self.game.live_players[:],
                                prompt_string = "Who do you choose to disarm?")
        self.game.publish(self.game.players, "ability", "Disarm", target)
        target.hand.shuffle()
        self.game.draw_card(target.hand, self.game.to_discard)

class Researcher(Character):
    def __init__(self, game):
        Character.__init__(self, game, "Researcher")
        self.abilities["Investigate"] = 1

    def investigate(self):
        player = self.game.get_player(self)
        target = player.prompt(self.game.live_players[:],
                               prompt_string = "Who do you choose to investigate?")
        self.game.publish(self.game.players, "ability", "Investigate", target)
        target.hand.shuffle()
        if target.hand.size():
            card = self.game.draw_card(target.hand, player.hand)[0]
            replace = player.prompt(["Yes","No"],
                                    prompt_string = "Do you choose to return the card?")
            if replace == "Yes":
                self.game.move_card(card, player.hand, target.hand)

class Quartermaster(Character):
    def __init__(self, game):
        Character.__init__(self, game, "Quartermaster")
        self.abilities["Ration"] = 1

    def ration(self):
        player = self.game.get_player(self)
        target = player.prompt(self.game.live_players[:],
                               prompt_string = "Who do you choose to ration?")
        self.game.publish(self.game.players, "ability", "ration", target)
        if target.health > 1:
            target.damage(1)
        else:
            target.damage(-1)
