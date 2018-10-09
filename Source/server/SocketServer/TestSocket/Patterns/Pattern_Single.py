
from xml.dom.minidom import parse
import xml.dom.minidom

from Patterns.Pattern import Pattern

class Pattern_Single(Pattern):
    ELEMENT_NAME = "single"
    def __init__(self):
        super(Pattern_Single, self).__init__()
        self.__ctype = "*"
        self.__cfigure = 0

    def load(self, xmlElement):
        if xmlElement.tagName != Pattern_Single.ELEMENT_NAME:
            return False

    def is_my_pattern(self, cards):
        return False
