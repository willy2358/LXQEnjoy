
from GRules.RulePart import RulePart
from Cards.Card import Card
import Utils



class RulePart_Cards(RulePart):
    __part_name = "cards"
    __attr_name_sets = "sets"
    __tag_name_excludes = "excludes"
    __tag_name_card = "card"

    def __init__(self, xmlNode):
        super(RulePart_Cards, self).__init__(xmlNode)
        self.__card_sets = 1
        self.__excluded_cards = []

    def parse(self):

        try:
            self.read_card_sets()
            self.read_excludes()

            return  True
        except Exception as ex:
            raise ex


    def read_card_sets(self):

        xmlNode = self.get_xml_node()
        if not xmlNode.hasAttribute(RulePart_Cards.__attr_name_sets):
            self.__card_sets = 1
            return

        self.__card_sets = int(xmlNode.getAttribute(RulePart_Cards.__attr_name_sets))
        if self.__card_sets < 1:
            self.__card_sets = 1

    def read_excludes(self):
        xmlNode = self.get_xml_node()
        if not RulePart.is_contain_valid_child_node(RulePart_Cards.__tag_name_excludes, xmlNode):
            return

        nodeExcludes = Utils.getFirstNamedChild(RulePart_Cards.__tag_name_excludes, xmlNode)
        for child in nodeExcludes.getElementsByTagName(RulePart_Cards.__tag_name_card):
            ctype = "*"
            cfigure = "*"
            if child.hasAttribute(Card.CTYPE):
                ctype = child.getAttribute(Card.CTYPE)
            if child.hasAttribute(Card.CFIGURE):
                cfigure = child.getAttribute(Card.CFIGURE)
            if ctype == "-" or cfigure == "-":  #rule, 不能有未指定
                continue
            if ctype == "*" and cfigure == "*": #rule: 不能是所有牌型，又是所有数字
                continue
            for c in Card.create_cards(self.getGRule().get_gtype(), ctype, cfigure):
                self.__excluded_cards.append(c)



