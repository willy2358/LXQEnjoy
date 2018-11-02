
from GCore.Statement import Statement

# send some cards from a variable
# <send_cards player="@drawer" cards="@drawn_card" ></send_cards>
class SendCards(Statement):
    def __init__(self, cards, recv_player):
        self.__cards = cards
        self.__recv_player = recv_player

    def gen_runtime_obj(self, scene):
        def send_cards_rtobj():
            player = scene.find_player(self.__recv_player)
            if player:
                player.send_cards(self.__cards)

        return send_cards_rtobj
