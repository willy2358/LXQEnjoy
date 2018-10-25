
from xml.dom.minidom import parse
import xml.dom.minidom

from GRules.RulePart import RulePart
from Cards.Card import Card
from GRules.Kitty import Kitty
from Patterns.PatternFactory import *
import GCore.Engine
import Utils





class RulePart_Cards(RulePart):
    PART_NAME = "cards"
    __attr_name_sets = "sets"
    __tag_name_excludes = "excludes"
    tag_name_card = "card"
    TAG_NAME_SCORE_CARDS = "score_cards"
    ATTR_NAME_SCORE = "score"
    TAG_NAME_PATTERNS = "patterns"

    def __init__(self, xmlNode, gRule):
        super(RulePart_Cards, self).__init__(xmlNode, gRule)
        self.__card_sets = 1
        self.__excluded_cards = []
        self.__kitty = None
        self.__score_cards = []
        self.__patterns = []

    def get_part_name(self):
        return self.PART_NAME

    def get_patterns(self):
        return self.__patterns

    def parse(self):
        try:
            self.read_card_sets()
            self.read_excludes()
            self.read_kitty()
            self.read_score_cards()
            self.read_patterns()

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

        nodeExcludes = Utils.getXmlFirstNamedChild(RulePart_Cards.__tag_name_excludes, xmlNode)
        for child in nodeExcludes.getElementsByTagName(RulePart_Cards.tag_name_card):
            ctype = "*"
            cfigure = "*"
            if child.hasAttribute(Card.CTYPE):
                ctype = child.getAttribute(Card.CTYPE)
            if child.hasAttribute(Card.CFIGURE):
                cfigure = child.getAttribute(Card.CFIGURE)
            if ctype == "-" or cfigure == "-":  #rule: 不能有未指定
                continue
            if ctype == "*" and cfigure == "*": #rule: 不能是所有牌型，又是所有数字
                continue
            for c in Card.create_cards(self.getGRule().get_gtype(), ctype, cfigure):
                self.__excluded_cards.append(c)

    def read_kitty(self):
        xmlNode = self.get_xml_node()
        if not RulePart.is_contain_valid_child_node(Kitty.TAG_NAME_KITTY, xmlNode):
            return
        kittyNode = Utils.getXmlFirstNamedChild(Kitty.TAG_NAME_KITTY, xmlNode)
        count = 0
        if kittyNode.hasAttribute(Kitty.ATTR_NAME_COUNT):
            count = int(kittyNode.getAttribute(Kitty.ATTR_NAME_COUNT))
        pub_shown = False
        if kittyNode.hasAttribute(Kitty.ATTR_NAME_PUBLIC_SHOWN):
            val = kittyNode.getAttribute(Kitty.ATTR_NAME_PUBLIC_SHOWN)
            if val.lower().startswith("t"):
                pub_shown = True

        if count > 0:
            self.__kitty = Kitty(count, pub_shown)


    def read_score_cards(self):
        xmlNode = self.get_xml_node()
        if not RulePart.is_contain_valid_child_node(RulePart_Cards.TAG_NAME_SCORE_CARDS, xmlNode):
            return
        sNode = Utils.getXmlFirstNamedChild(RulePart_Cards.TAG_NAME_SCORE_CARDS, xmlNode)
        for child in sNode.getElementsByTagName(GCore.Engine.tag_name_card):
            ctype = "*"
            cfigure = "*"
            if child.hasAttribute(Card.CTYPE):
                ctype = child.getAttribute(Card.CTYPE)
            if child.hasAttribute(Card.CFIGURE):
                cfigure = child.getAttribute(Card.CFIGURE)
            if ctype == "-" or cfigure == "-":  # rule: 不能有未指定
                continue
            if ctype == "*" and cfigure == "*":  # rule: 不能是所有牌型，又是所有数字
                continue

            score = 0
            if child.hasAttribute(RulePart_Cards.ATTR_NAME_SCORE):
                score = int(child.getAttribute(RulePart_Cards.ATTR_NAME_SCORE))

            for c in Card.create_cards(self.getGRule().get_gtype(), ctype, cfigure):
                c.set_score(score)
                self.__score_cards.append(c)

    def read_patterns(self):
        xmlNode = self.get_xml_node()
        if not RulePart.is_contain_valid_child_node(RulePart_Cards.TAG_NAME_PATTERNS, xmlNode):
            return
        patterns = Utils.getXmlFirstNamedChild(RulePart_Cards.TAG_NAME_PATTERNS, xmlNode)
        for c in Utils.getXmlChildElments(xmlNode):

            pat = create_pattern(c.tagName, c, self.getGRule())

            if pat and pat.load(c):
                self.__patterns.append(pat)



