#!/usr/bin/env python

from card import Card, Mission
from deck import Deck

class Crew(Mission):
    def __init__(self, game):
        Mission.__init__(self, game, "Crew", True, False)

class Saboteur(Mission):
    def __init__(self, game):
        Mission.__init__(self, game, "Crew", False, True)

class Accomplice(Mission):
    def __init__(self, game):
        Mission.__init__(self, game, "Crew", True, True)

class Chancellor(Mission):
    def __init__(self, game):
        Mission.__init__(self, game, "Crew", False, False)
