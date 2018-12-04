

from GCore.Statement import Statement
import Mains.Log as Log

# pick some cards from a player, always in random way
# <pick_cards to_var="@picked_card" count="1" from_player="@player"></pick_cards>
class PickCards(Statement):
    def __init__(self, count, from_player, to_var):
        self.__count = count
        self.__from_player = from_player
        self.__to_var = to_var

    def gen_runtime_obj(self, scene):
        def pick_cards():
            try:
                player = scene.get_obj_value(self.__from_player)
                var = scene.get_rt_var(self.__to_var)
                if player and var:
                    count = scene.get_obj_value(self.__count)
                    cards = player.pick_cards(count)
                    var.set_value(cards)
            except Exception as ex:
                Log.exception(ex)

        return pick_cards