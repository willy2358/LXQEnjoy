
from GRules.RulePart import RulePart

class RulePart_Round(RulePart):
    __part_name = "round"

    def __init__(self, xmlNode, gRule):
        super(RulePart_Round, self).__init__(xmlNode, gRule)

    def parse(self):
        return True