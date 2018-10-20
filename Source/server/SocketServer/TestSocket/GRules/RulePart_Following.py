
from GRules.RulePart import RulePart

class RulePart_Following(RulePart):
    PART_NAME = "following"

    def __init__(self, xmlNode, gRule):
        super(RulePart_Following, self).__init__(xmlNode, gRule)

    def parse(self):
        return True

    def get_part_name(self):
        return self.PART_NAME