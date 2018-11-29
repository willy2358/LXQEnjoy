
import random
from Mains.GVar import GVar

import Utils

from Mains.ExtAttrs import ExtAttrs

class Round(ExtAttrs):
    def __init__(self):
        super(Round, self).__init__()
        self.__player_wins = {}
        self.__undealing_cards = []
        self.__debug_cards = []

    def init_cards_pack(self, cards):
        self.__undealing_cards = cards[:]

    def draw_cards(self, count):
        cards = []
        if self.__debug_cards:
            if len(self.__debug_cards) >= count:
                cards = self.__debug_cards[0:count]
                Utils.list_remove_parts(self.__debug_cards, cards)
            else:
                cards = self.__debug_cards[:]
                tmpStack = self.__undealing_cards[:]
                Utils.list_remove_parts(tmpStack, self.__debug_cards)
                cards = cards + random.sample(tmpStack, count - len(self.__debug_cards))
                self.__debug_cards.clear()
        else:
            cards = random.sample(self.__undealing_cards, count)

        Utils.list_remove_parts(self.__undealing_cards, cards)
        return cards

    def undealing_cards_count(self):
        return len(self.__undealing_cards)

    def set_debug_cards(self, cards):
        self.__debug_cards = cards
