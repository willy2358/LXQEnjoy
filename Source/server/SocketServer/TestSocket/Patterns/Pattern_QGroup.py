
from Patterns.Pattern import Pattern

#同型组
class Pattern_QGroup(Pattern):
    def __init__(self, minLen, maxLen, beginCfigure = "*"):
        super(Pattern_QGroup, self).__init__()
        self.__group_pattern = None

    def set_group_pattern(self, pattern):
        self.__group_pattern = pattern


