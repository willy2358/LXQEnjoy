from GCore.Statement import Statement

# pick some cards from a player, always in random way
# <pick_cards to_var="@picked_card" count="1" from_player="@player"></pick_cards>
class PickCards(Statement):
    def __init__(self, count, from_player, to_var):
        self.__count = count
        self.__from_player = from_player
        self.__to_var = to_var


