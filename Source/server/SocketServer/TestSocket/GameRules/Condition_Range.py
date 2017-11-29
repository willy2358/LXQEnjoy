
from GameRules.Condition import Condition

class Condition_Range(Condition):
    def __init__(self, min_card, max_card, min_freq, max_freq):
        self.__min_card = min_card
        self.__max_card = max_card
        self.__min_freq = min_freq
        self.__max_freq = max_freq

