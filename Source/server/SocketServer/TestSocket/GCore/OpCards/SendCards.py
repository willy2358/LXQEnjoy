
from GCore.Statement import Statement

# send some cards from a variable
# <send_cards player="@drawer" cards="@drawn_card" ></send_cards>
class SendCards(Statement):
    def __init__(self, cards, recv_player):
        self.__cards = cards
        self.__recv_player = recv_player

