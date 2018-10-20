

from GRules.RulePart import RulePart

class RulePart_Players(RulePart):
    PART_NAME = "players"

    def __init__(self, xmlNode, gRule):
        super(RulePart_Players, self).__init__(xmlNode, gRule)

    def parse(self):
        return True

    def get_part_name(self):
        return self.PART_NAME