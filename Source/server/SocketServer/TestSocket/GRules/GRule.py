
from xml.dom.minidom import parse
import xml.dom.minidom

import Log

from GRules import RulePartFactory

class GRule:
    def __init__(self, xmlConfig):
        self._config_file = xmlConfig
        self.__parts = []
        self.__game_id = "0"
        self.__game_text = "game"

    def load(self):
        try:
            DOMTree = xml.dom.minidom.parse(self._config_file)
            game = DOMTree.documentElement
            if not self.parse_game_attrs(game):
                return False

            for c in game.childNodes:
                if type(c) is xml.dom.minidom.Element:
                    part = RulePartFactory.create_part(c.tagName, c)
                    if part.parse():
                        self.__parts.append(part)

            return True
        except Exception as ex:
            Log.write_exception(ex)
            return False

    def parse_game_attrs(self, gameElem):
        if not gameElem:
            return False

        if not gameElem.hasAttribute("gameid"):
            return False
        self.__game_id = gameElem.getAttribute("gameid")

        if not gameElem.hasAttribute("text"):
            return False
        self.__game_text = gameElem.getAttribute("text")

        return True


    def get_gameid(self):
        return self.__game_id

    def get_game_text(self):
        return self.__game_text

