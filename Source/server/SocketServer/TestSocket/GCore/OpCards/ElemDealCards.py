
from GCore.Statement import Statement

#deal some cards to player, from the card stack
#<deal_cards count="6" player="@player"></deal_cards>
class DealCards(Statement):
    def __init__(self, count, to_player):
        self.__to_player = to_player
        self.__count = count


