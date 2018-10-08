
from Patterns.Pattern import Pattern

#牌型组
class Pattern_Comp(Pattern):
    def __init__(self):
        super(Pattern_Comp, self).__init__()
        self.__child_patterns = []

    def append_child_pattern(self, pattern):
        self.__child_patterns.append(pattern)
