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

    @staticmethod
    def get_type_str(valType):
        if valType == ValueType.integer:
            return "int"
        elif valType == ValueType.string:
            return "str"
        elif valType == ValueType.bool:
            return "bool"
        elif valType == ValueType.card:
            return "card"
        elif valType == ValueType.cards:
            return "cards"
        elif valType == ValueType.player:
            return "player"
        elif valType == ValueType.players:
            return "players"
        else:
            return "undef"

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