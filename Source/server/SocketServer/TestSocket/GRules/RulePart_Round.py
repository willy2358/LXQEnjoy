
from GRules.RulePart import RulePart
from GCore.Variable import Variable
import GCore.Engine as Engine
import Utils


class RulePart_Round(RulePart):
    PART_NAME = "round"

    def __init__(self, xmlNode, gRule):
        super(RulePart_Round, self).__init__(xmlNode, gRule)
        self.__custom_attrs = []

    def parse(self):
        return True

    def get_part_name(self):
        xmlNode = self.get_xml_node()
        attrsRoot = Utils.getXmlFirstNamedChild(Engine.tag_name_attrs)
        if not attrsRoot:
            attrsRoot = xmlNode

        for elem in Utils.getXmlChildElments(attrsRoot):
            if elem.tag == Engine.tag_name_attr:
                vName = elem.getAttribute(Engine.attr_name_name)
                vType = elem.getAttribute(Engine.attr_name_value_type)
                attr = Variable(vName)
                attr.set_value_type(vType)
                self.__custom_attrs.append(attr)