
from GRules.RulePart import RulePart
# import GRules

class RulePart_Actions(RulePart):
    __part_name = "actions"

    def __init__(self, xmlNode, gRule):
        super(RulePart_Actions, self).__init__(xmlNode, gRule)

    def parse(self):
        return True