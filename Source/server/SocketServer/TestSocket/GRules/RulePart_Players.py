

from GRules.RulePart import RulePart

class RulePart_Players(RulePart):
    __part_name = "players"

    def __init__(self, xmlNode):
        super(RulePart_Players, self).__init__(xmlNode)

    def parse(self):
        return True