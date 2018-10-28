
from GRules.RulePart import RulePart
# import GRules
import GCore.Engine as Engine
import Utils

class RulePart_Actions(RulePart):
    PART_NAME = "actions"

    def __init__(self, xmlNode, gRule):
        super(RulePart_Actions, self).__init__(xmlNode, gRule)
        self.__actions = []

    def parse(self):
        xmlNode = self.get_xml_node()

        for elem in Utils.getXmlChildElments(xmlNode):
            if elem.tagName == Engine.tag_name_action:
                action = Engine.parse_elem_action(elem)
                if action:
                    self.add_action(action)

    def get_part_name(self):
        return self.PART_NAME

    def add_action(self, act):
        self.__actions.append(act)

