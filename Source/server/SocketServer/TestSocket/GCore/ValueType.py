from enum import Enum


class ValueType(Enum):
    undef = 0
    integer = 1
    string = 2
    bool = 3
    card = 4
    cards = 5  # list of cards
    player = 6
    players = 7 # list of players