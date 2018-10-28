
import Utils
from GRules.RulePart import RulePart
from GCore.Variable import Variable
import GCore.Engine as Engine

class RulePart_Players(RulePart):
    PART_NAME = "players"

    def __init__(self, xmlNode, gRule):
        super(RulePart_Players, self).__init__(xmlNode, gRule)
        self.__min_players = 0
        self.__max_players = 0
        self.__custom_attrs = []

    def parse(self):
        xmlNode = self.get_xml_node()
        if xmlNode.hasAttribute(Engine.attr_name_max):
            self.__max_players = int(xmlNode.getAttribute(Engine.attr_name_max))

        if xmlNode.hasAttribute(Engine.attr_name_min):
            self.__min_players = int(xmlNode.getAttribute(Engine.attr_name_min))

        rule = self.getGRule()
        rule.set_players_capacity(self.__min_players, self.__max_players)

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

    def get_part_name(self):
        return self.PART_NAME