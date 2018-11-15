
from GCore.Statement import Statement
import Mains.Log as Log

# send some cards from a variable
# <send_cards player="@drawer" cards="@drawn_card" ></send_cards>
class SendCards(Statement):
    def __init__(self, cards, recv_player):
        self.__cards = cards
        self.__recv_player = recv_player

    def gen_runtime_obj(self, scene):

        # player_func = self.__recv_player.gen_runtime_obj(scene)
        # cards_func = self.__cards.gen_runtime_obj(scene)
        def send_cards_rtobj():
            try:
                player = scene.get_obj_value(self.__recv_player)
                cards = scene.get_obj_value(self.__cards)
                if player and cards:
                    player.send_cards(cards)
            except Exception as ex:
                Log.exception(ex)

            # playerRef = player_func()
            # cardsRef = cards_func()
            # player = scene.get_prop_value(playerRef.get_name())
            # cards = scene.get_prop_value(cardsRef.get_name())


        return send_cards_rtobj
