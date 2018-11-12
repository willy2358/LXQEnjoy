
from GRules.RulePart import RulePart
from GCore.Elements.Variable import Variable
import GCore.Engine as Engine
import Utils


class RulePart_Round(RulePart):
    PART_NAME = "round"

    def __init__(self, xmlNode, gRule):
        super(RulePart_Round, self).__init__(xmlNode, gRule)
        self.__custom_attrs = []

    def get_custom_attrs(self):
        return self.__custom_attrs

    def parse(self):
        xmlNode = self.get_xml_node()
        attrsRoot = Utils.getXmlFirstNamedChild(Engine.tag_name_attrs, xmlNode)
        if not attrsRoot:
            attrsRoot = xmlNode

        for elem in Utils.getXmlChildElments(attrsRoot):
            if elem.tagName == Engine.tag_name_attr:
                attrVar = Engine.parse_elem_var(elem)
                if attrVar:
                    self.__custom_attrs.append(attrVar)
        return True

    def get_part_name(self):
       return self.PART_NAME