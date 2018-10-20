
from GRules.RulePart import RulePart

class RulePart_Running(RulePart):
    PART_NAME = "running"

    def __init__(self, xmlNode, gRule):
        super(RulePart_Running, self).__init__(xmlNode, gRule)

    def parse(self):
        return True

    def get_part_name(self):
        return self.PART_NAME