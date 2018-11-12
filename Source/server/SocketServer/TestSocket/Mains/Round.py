
import random
from Mains.GVar import GVar

import Utils

from Mains.ExtAttrs import ExtAttrs

class Round(ExtAttrs):
    def __init__(self):
        super(Round, self).__init__()
        self.__player_wins = {}
        self.__undealing_cards = []

    def init_cards_pack(self, cards):
        self.__undealing_cards = cards[:]

    def draw_cards(self, count):
        cards = random.sample(self.__undealing_cards, count)
        Utils.list_remove_parts(self.__undealing_cards, cards)
        return cards