
from GRules.RulePart import RulePart
import GCore.Engine

import Utils

class RulePart_Running(RulePart):
    PART_NAME = "running"

    def __init__(self, xmlNode, gRule):
        super(RulePart_Running, self).__init__(xmlNode, gRule)
        self.__statements = []

    def parse(self):
        xmlNode = self.get_xml_node()
        if not xmlNode:
            return False

        try:
            for elem in Utils.getXmlChildElments(xmlNode):
                st = GCore.Engine.parse_elem(elem, self.getGRule())
                if st:
                    self.__statements.append(st)

            return  True
        except Exception as ex:
            raise ex

    def get_part_name(self):
        return self.PART_NAME

    def get_statements(self):
        return self.__statements