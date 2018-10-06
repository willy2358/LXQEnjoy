
from GRules.RulePart import RulePart


class RulePart_Cards(RulePart):
    __part_name = "cards"

    def __init__(self, xmlNode):
        super(RulePart_Cards, self).__init__(xmlNode)

    def parse(self):
        return True
