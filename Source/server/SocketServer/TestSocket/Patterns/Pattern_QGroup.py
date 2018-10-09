
from Patterns.Pattern import Pattern

#同型组
class Pattern_QGroup(Pattern):
    ELEMENT_NAME = "qgroup"
    def __init__(self, minLen, maxLen, beginCfigure = "*"):
        super(Pattern_QGroup, self).__init__()
        self.__group_pattern = None

    def load(self, xmlElement):
        if xmlElement.tagName != Pattern_QGroup.ELEMENT_NAME:
            return False
        return True

    def set_group_pattern(self, pattern):
        self.__group_pattern = pattern


    def is_my_pattern(self, cards):
        return False