
import Utils
from GRules.RulePart import RulePart
from GCore.Elements.Variable import Variable
import GCore.Engine as Engine

class RulePart_Players(RulePart):
    PART_NAME = "players"

    def __init__(self, xmlNode, gRule):
        super(RulePart_Players, self).__init__(xmlNode, gRule)
        self.__min_players = 0
        self.__max_players = 0
        self.__custom_attrs = []

    def get_custom_attrs(self):
        return self.__custom_attrs

    def parse(self):
        xmlNode = self.get_xml_node()
        if xmlNode.hasAttribute(Engine.attr_name_max):
            self.__max_players = int(xmlNode.getAttribute(Engine.attr_name_max))

        if xmlNode.hasAttribute(Engine.attr_name_min):
            self.__min_players = int(xmlNode.getAttribute(Engine.attr_name_min))

        rule = self.getGRule()
        rule.set_players_capacity(self.__min_players, self.__max_players)

        attrsRoot = Utils.getXmlFirstNamedChild(Engine.tag_name_attrs, xmlNode)
        if not attrsRoot:
            attrsRoot = xmlNode

        for elem in Utils.getXmlChildElments(attrsRoot):
            if elem.tagName == Engine.tag_name_attr:
                attrVar = Engine.parse_elem_attr(elem, self.getGRule(), "player.")
                if attrVar:
                    self.__custom_attrs.append(attrVar)
        return True

    def get_part_name(self):
        return self.PART_NAME