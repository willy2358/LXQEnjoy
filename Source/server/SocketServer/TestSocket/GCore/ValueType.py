from enum import Enum


class ValueType(Enum):
    integer = 0
    string = 1
    card = 2
    cards = 3  # list of cards
    player = 4
    players = 5 # list of players