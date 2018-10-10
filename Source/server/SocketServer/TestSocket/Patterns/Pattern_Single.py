
from xml.dom.minidom import parse
import xml.dom.minidom

from Cards.CFigure import CFigure, parse_cfigure
from Cards.CFigure import TOKEN as CFIGURE_TOKEN
from Cards.CType import CType, parse_ctype
from Cards.CType import TOKEN as CTYPE_TOKEN
from GCore.Engine import *
from GCore.Expression import Expression

from Patterns.Pattern import Pattern

class Pattern_Single(Pattern):
    ELEMENT_NAME = "single"
    def __init__(self):
        super(Pattern_Single, self).__init__()
        self.__ctype = CType.Any
        self.__cfigure = CFigure.Undefined

    def load(self, xmlElement):

        if xmlElement.tagName != Pattern_Single.ELEMENT_NAME:
            return False
        try:

            if xmlElement.hasAttribute(CFIGURE_TOKEN):
                self.__cfigure = parse_cfigure(xmlElement.getAttribute(CFIGURE_TOKEN))
            if xmlElement.hasAttribute(CTYPE_TOKEN):
                self.__ctype = parse_ctype(xmlElement.getAttribute(CTYPE_TOKEN))
            if xmlElement.hasAttribute(Pattern.ATTR_NAME_POWER):
                power = xmlElement.getAttribute(Pattern.ATTR_NAME_POWER)
                if power.isnumeric():
                    self.set_power(int(power))
                elif is_attr_expression(power):
                    self.add_power_clause(Expression(power))
            if not xmlElement.hasChild():
                return True
            for c in xmlElement.childNode:
                print(c)
        except Exception as ex:
            return False

    def is_my_pattern(self, cards):
        return False
