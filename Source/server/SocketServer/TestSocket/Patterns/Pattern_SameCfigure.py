
from Patterns.Pattern import Pattern

class Pattern_SameCfigure(Pattern):
    ELEMENT_NAME = "same_cfigure"
    ELEMENT_PAIR = "pair"
    ELEMENT_TRIPLE = "triple"
    ELEMENT_QUAD = "quad"

    def __init__(self, multiply, cfigure):
        super(Pattern_SameCfigure, self).__init__()
        self.__multiply = multiply
        self.__cfigure = cfigure

    def load(self, xmlElement):
        if xmlElement.tagName != Pattern_SameCfigure.ELEMENT_NAME \
            and xmlElement.tagName != Pattern_SameCfigure.ELEMENT_PAIR\
            and xmlElement.tagName != Pattern_SameCfigure.ELEMENT_TRIPLE\
            and xmlElement.tagName != Pattern_SameCfigure.ELEMENT_QUAD:
            return False
        return True

    def is_my_pattern(self, cards):
        return False