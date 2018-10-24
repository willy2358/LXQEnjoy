
from Patterns.Pattern import Pattern

class Pattern_Seqm:
    ELEMENT_NAME = "seqm"
    def __init__(self, gRule):
        super(Pattern_Seqm, self).__init__(gRule)
        self.__ctype = '*'
        self.__begin = 0
        self.__min_len = 0
        self.__max_len = 0
        self.__m = 1

    def load(self, xmlElement):
        if xmlElement.tagName != Pattern_Seqm.ELEMENT_NAME:
            return False
        return True

    def is_my_pattern(self, cards):
        return False