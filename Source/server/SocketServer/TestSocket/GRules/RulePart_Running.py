
from GRules.RulePart import RulePart

class RulePart_Running(RulePart):
    __part_name = "running"

    def __init__(self, xmlNode, gRule):
        super(RulePart_Running, self).__init__(xmlNode, gRule)

    def parse(self):
        return True
