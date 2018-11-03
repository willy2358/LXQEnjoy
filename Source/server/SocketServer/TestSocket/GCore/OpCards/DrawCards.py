
import sys
sys.path.append('..')

from GCore.Statement import Statement
from GCore import Engine

#draw some cards from the card stack, but without dealing them to a player, assign these cards to a varialble
# <draw_cards to_var="@drawn_card" count="1"></draw_cards>
class DrawCards(Statement):
    def __init__(self, var, count):
        self.__hold_var = var
        self.__count = count

    def gen_runtime_obj(self, scene):
        def draw_cards():
            cards = scene.draw_cards(self.__count)
            scene.update_variable(Engine.get_variable_name(self.__hold_var), cards)

        return draw_cards





    