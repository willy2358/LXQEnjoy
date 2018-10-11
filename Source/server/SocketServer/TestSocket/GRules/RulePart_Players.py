

from GRules.RulePart import RulePart

class RulePart_Players(RulePart):
    __part_name = "players"

    def __init__(self, xmlNode, gRule):
        super(RulePart_Players, self).__init__(xmlNode, gRule)

    def parse(self):
        return True