
from GRules.RulePart import RulePart

class RulePart_Following(RulePart):
    __part_name = "following"

    def __init__(self, xmlNode, gRule):
        super(RulePart_Following, self).__init__(xmlNode, gRule)

    def parse(self):
        return True