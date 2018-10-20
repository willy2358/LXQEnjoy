
from GRules.RulePart import RulePart
# import GRules

class RulePart_Actions(RulePart):
    PART_NAME = "actions"

    def __init__(self, xmlNode, gRule):
        super(RulePart_Actions, self).__init__(xmlNode, gRule)

    def parse(self):
        return True

    def get_part_name(self):
        return self.PART_NAME

