
from GRules.RulePart import RulePart

class RulePart_Trick(RulePart):
    __part_name = "trick"

    def __init__(self, xmlNode):
        super(RulePart_Trick, self).__init__(xmlNode)

    def parse(self):
        return True

