
from GCore.Statement import Statement

class DealCards(Statement):
    def __init__(self, cards, to_player):
        self.__cards = cards
        self.__to_player = to_player
