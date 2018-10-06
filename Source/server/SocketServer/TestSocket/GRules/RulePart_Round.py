
from GRules.RulePart import RulePart

class RulePart_Round(RulePart):
    __part_name = "round"

    def __init__(self, xmlNode):
        super(RulePart_Round, self).__init__(xmlNode)

    def parse(self):
        return True