
from GRules.RulePart import RulePart

class RulePart_Round(RulePart):
    PART_NAME = "round"

    def __init__(self, xmlNode, gRule):
        super(RulePart_Round, self).__init__(xmlNode, gRule)

    def parse(self):
        return True

    def get_part_name(self):
        return self.PART_NAME