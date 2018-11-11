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
    void = 8


def parse_from_str(sType):
    slower = sType.lower()
    if "players" in slower:
        return ValueType.players
    elif "player" in slower:
        return ValueType.player
    elif "int" in slower:
        return ValueType.integer
    elif 'str' in sType:
        return ValueType.string
    elif "bo" in slower:
        return ValueType.bool
    elif "cards" in slower:
        return ValueType.cards
    elif "card" in slower:
        return ValueType.card
    else:
        return ValueType.undef