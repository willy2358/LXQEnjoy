
from GRules.RulePart import RulePart

class RulePart_Trick(RulePart):
    PART_NAME = "trick"

    def __init__(self, xmlNode, gRule):
        super(RulePart_Trick, self).__init__(xmlNode, gRule)

    def parse(self):
        return True

    def get_part_name(self):
        return self.PART_NAME
