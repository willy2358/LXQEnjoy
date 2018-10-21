
from xml.dom.minidom import parse
import xml.dom.minidom

from Mains import Log
from Cards.GType import GType

from GRules import RulePartFactory


class GRule:
    def __init__(self, xmlConfig):
        self._config_file = xmlConfig
        self.__parts = []
        self.__rule_id = "0"
        self.__game_text = "game"
        self.__game_type = GType.Poker
        self.__max_players_capacity = 0
        self.__min_players_capacity = 0

    def get_max_players_capacity(self):
        return self.__max_players_capacity

    def get_min_players_capacity(self):
        return self.__min_players_capacity

    def load(self):
        try:
            DOMTree = xml.dom.minidom.parse(self._config_file)
            game = DOMTree.documentElement
            if not self.parse_game_attrs(game):
                return False

            for c in game.childNodes:
                if type(c) is xml.dom.minidom.Element:
                    part = RulePartFactory.create_part(c.tagName, c, self)
                    if part.parse():
                        self.__parts.append(part)

            return True
        except Exception as ex:
            Log.exception(ex)
            return False

    def parse_game_attrs(self, gameElem):
        if not gameElem:
            return False

        if not gameElem.hasAttribute("gameid"):
            return False
        self.__rule_id = gameElem.getAttribute("gameid")

        if not gameElem.hasAttribute("text"):
            return False
        self.__game_text = gameElem.getAttribute("text")

        if gameElem.hasAttribute("gtype"):
            gtype = gameElem.getAttribute("gtype").lower()
            if gtype.startswith("p"):
                self.__game_type = GType.Poker
            elif gtype.startswith("m"):
                self.__game_type = GType.Mahong

        return True


    def get_ruleid(self):
        return self.__rule_id

    def get_game_text(self):
        return self.__game_text

    def get_gtype(self):
        return self.__game_type

    # def get_running_part(self):
    #     for p in self.__parts:
    #         if type(p) is RulePart_Running:
    #             return p
    #
    #     return None

    def get_part_of_name(self, partName):
        for p in self.__parts:
            if p.get_part_name() == partName:
                return p

        return None



