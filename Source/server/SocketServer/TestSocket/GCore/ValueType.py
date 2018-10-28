from enum import Enum


class ValueType(Enum):
    integer = 0
    string = 1
    bool = 2
    card = 3
    cards = 4  # list of cards
    player = 5
    players = 6 # list of players