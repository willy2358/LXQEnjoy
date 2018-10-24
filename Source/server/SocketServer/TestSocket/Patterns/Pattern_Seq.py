
from Patterns.Pattern import Pattern

class Pattern_Seq(Pattern):
    ELEMENT_NAME = "seq"
    def __init__(self, gRule):
        super(Pattern_Seq, self).__init__(gRule)
        self.__ctype = '*'
        self.__begin = 0
        self.__min_len = 0
        self.__max_len = 0

    def load(self, xmlElement):
        if xmlElement.tagName != Pattern_Seq.ELEMENT_NAME:
            return False
        return True

    def is_my_pattern(self, cards):
        return False