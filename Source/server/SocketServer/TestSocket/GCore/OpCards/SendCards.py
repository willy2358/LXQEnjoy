
from GCore.Statement import Statement
import Mains.Log as Log

# send some cards from a variable
# <send_cards player="@drawer" cards="@drawn_card" ></send_cards>
class SendCards(Statement):
    def __init__(self, cards, recv_player):
        self.__cards = cards
        self.__recv_player = recv_player

    def gen_runtime_obj(self, scene):
        def send_cards_rtobj():
            try:
                player = scene.get_obj_value(self.__recv_player)
                cards = scene.get_obj_value(self.__cards)
                if player and cards:
                    player.send_cards(cards)
            except Exception as ex:
                Log.exception(ex)

        return send_cards_rtobj
