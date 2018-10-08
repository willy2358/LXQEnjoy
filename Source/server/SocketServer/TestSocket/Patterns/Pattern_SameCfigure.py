
from Patterns.Pattern import Pattern

class Pattern_SameCfigure(Pattern):
    def __init__(self, multiply, cfigure):
        super(Pattern_SameCfigure, self).__init__()
        self.__multiply = multiply
        self.__cfigure = cfigure

