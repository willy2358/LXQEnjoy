
from GRules.RulePart import RulePart

class RulePart_Running(RulePart):
    __part_name = "running"

    def __init__(self, xmlNode):
        super(RulePart_Running, self).__init__(xmlNode)

    def parse(self):
        return True
