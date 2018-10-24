
from Patterns.Pattern import Pattern

#同型组
class Pattern_QGroup(Pattern):
    ELEMENT_NAME = "qgroup"
    def __init__(self, gRule):
        super(Pattern_QGroup, self).__init__(gRule)
        self.__group_pattern = None
        self.__min_len = 0;
        self.__max_len = 0;
        self.__begin_cfigure = "*"

    def load(self, xmlElement):
        if xmlElement.tagName != Pattern_QGroup.ELEMENT_NAME:
            return False
        return True

    def set_group_pattern(self, pattern):
        self.__group_pattern = pattern


    def is_my_pattern(self, cards):
        return False