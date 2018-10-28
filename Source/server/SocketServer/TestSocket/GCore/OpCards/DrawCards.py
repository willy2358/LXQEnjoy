
from GCore.Statement import Statement

#draw some cards from the card stack, but without dealing them to a player, assign these cards to a varialble
# <draw_cards to_var="@drawn_card" count="1"></draw_cards>
class DrawCards(Statement):
    def __init__(self, var, count):
        self.__var = var
        self.__count = count

    