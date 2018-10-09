
from Patterns.Pattern import Pattern

class Pattern_Seqm:
    ELEMENT_NAME = "seqm"
    def __init__(self, m, ctype, begin, minLen, maxLen):
        super(Pattern_Seqm, self).__init__()

    def load(self, xmlElement):
        if xmlElement.tagName != Pattern_Seqm.ELEMENT_NAME:
            return False
        return True

    def is_my_pattern(self, cards):
        return False