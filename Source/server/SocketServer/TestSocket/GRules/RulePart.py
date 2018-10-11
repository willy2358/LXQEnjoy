
from xml.dom.minidom import parse
import xml.dom.minidom

class RulePart:

    __attr_name_valid = "valid"
    def __init__(self, xmlNode, gRule):
        self.__xml_node = xmlNode
        self.__gRule = gRule

    def parse(self):
        pass

    def get_xml_node(self):
        return self.__xml_node

    def getGRule(self):
        return self.__gRule

    @staticmethod
    def is_contain_valid_child_node(tagName, parentNode):

        for child in parentNode.childNodes:
            if type(child) is not xml.dom.minidom.Element:
                continue
            if child.tagName != tagName:
                continue
            valid = True  #the default value is True
            if child.hasAttribute(RulePart.__attr_name_valid):
                val = child.getAttribute(RulePart.__attr_name_valid)
                if val.lower().startswith("f"): #False
                    valid = False
                else:
                    valid = True
            return valid






