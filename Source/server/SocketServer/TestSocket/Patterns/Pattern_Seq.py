
from Patterns.Pattern import Pattern

class Pattern_Seq(Pattern):
    ELEMENT_NAME = "seq"
    def __init__(self, ctype, begin, minLen, maxLen):
        super(Pattern_Seq, self).__init__()

    def load(self, xmlElement):
        if xmlElement.tagName != Pattern_Seq.ELEMENT_NAME:
            return False
        return True

    def is_my_pattern(self, cards):
        return False