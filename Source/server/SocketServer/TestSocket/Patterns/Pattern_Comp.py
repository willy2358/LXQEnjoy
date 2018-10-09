
from Patterns.Pattern import Pattern

#牌型组
class Pattern_Comp(Pattern):
    ELEMENT_NAME = "comp"
    def __init__(self):
        super(Pattern_Comp, self).__init__()
        self.__child_patterns = []

    def append_child_pattern(self, pattern):
        self.__child_patterns.append(pattern)

    def load(self, xmlElement):
        if xmlElement.tagName != Pattern_Comp.ELEMENT_NAME:
            return False
        return True

    def is_my_pattern(self, cards):
        return False