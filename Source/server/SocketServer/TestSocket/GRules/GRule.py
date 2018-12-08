
from xml.dom.minidom import parse
import xml.dom.minidom

from Mains import Log
from Cards.GType import GType
from GCore.ValueType import ValueType
from GCore.Operator import Operator

from GRules import RulePartFactory
import Utils


class GRule:
    def __init__(self, xmlConfig):
        self._config_file = xmlConfig
        self.__parts = []
        self.__rule_id = "0"
        self.__game_text = "game"
        self.__game_type = GType.Poker
        self.__max_players_capacity = 0
        self.__min_players_capacity = 0

        self.__vars = []  #[Variable]
        self.__acts = []
        self.__procs = []

    def get_max_players_capacity(self):
        return self.__max_players_capacity

    def get_min_players_capacity(self):
        return self.__min_players_capacity

    def get_ruleid(self):
        return self.__rule_id

    def get_game_text(self):
        return self.__game_text

    def get_gtype(self):
        return self.__game_type

    def get_part_by_name(self, partName):
        for p in self.__parts:
            if p.get_part_name() == partName:
                return p

        return None
    def set_players_capacity(self, minPlayers, maxPlayers):
        self.__min_players_capacity = minPlayers
        self.__max_players_capacity = maxPlayers

    def add_act(self, act, xmlNode):
        if self.is_act_exists(act.get_name()):
            Log.warn("Duplicated def of action, name:{0}, xmlNode:{1}".format(act.get_name(),xmlNode.toxml()))
        else:
            self.__acts.append(act)

    def check_op_var(self, varName, op, xmlElem):
        if not self.is_var_exists(varName):
            Log.warn("Not existing var {0} with {1},xml node:{2}".format(varName, op, xmlElem.toxml()))
            return False

        var = None
        for v in self.__vars:
            if v.get_name() == varName:
                var = v
                break

        # if not var:
        #     Log.warn("Not existing var {0} with {1},xml node:{2}".format(varName, op, xmlElem.toxml()))
        #     return False

        if var and (var.get_value_type() == ValueType.cards \
                    or var.get_value_type() == ValueType.players):
            if op != Operator.Remove and op != Operator.Append and op != Operator.Update:
                Log.warn("Invalid op {0} on list {1}".format(op, varName))
                return False

    def is_act_exists(self, actName):
        for a in self.__acts:
            if a.get_name() == actName:
                return True

        return False

    def add_var(self, var, xmlNode):
        if self.is_var_exists(var.get_name()):
            Log.warn("Duplicated def of var, name:{0}, xmlnode:{1}".format(var.get_name(),xmlNode.toxml()))
        else:
            self.__vars.append(var)

    def is_var_exists(self, varName):
        if varName == "#arg_player" or varName == "#arg_cards" \
                or varName == "cmd_player" or varName == "cmd_args"\
                or varName == "round.players" or varName == "scene.players":
            return True

        if varName.startswith("#arg_player."):
            varName = varName[5:]
        if varName.startswith("cmd_player."):
            varName = varName[4:]

        #sometimes, player is a variable.
        ps = varName.split('.')
        if len(ps) == 2 and ps[0] != "round" and ps[0] != "scene" and ps[0] != "trick":
            varName = "player." + ps[1]
        elif '.[].' in varName:
            ps = varName.split('.[].')
            if len(ps) == 2 and ps[0].startswith('round.') or ps[0].startswith('scene.'):
                varName = "player." + ps[1]


        for v in self.__vars:
            if v.get_name() == varName:
                return True

        return False

    def add_proc(self, proc, xmlNode):
        if self.is_proc_exists(proc.get_name()):
            Log.warn("Duplicated def of proc, name:{0}, xmlnode:{1}".format(proc.get_name(), xmlNode.toxml()))
        else:
            self.__procs.append(proc)

    def is_proc_exists(self, procName):
        for p in self.__procs:
            if p.get_name() == procName:
                return True

        return False

    def parse_game_attrs(self, gameElem):
        if not gameElem:
            return False

        if not gameElem.hasAttribute("ruleid"):
            return False
        self.__rule_id = gameElem.getAttribute("ruleid")

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

    def load(self):

        try:
            DOMTree = xml.dom.minidom.parse(self._config_file)
            game = DOMTree.documentElement
            if not self.parse_game_attrs(game):
                return False

            for c in Utils.getXmlChildElments(game):
                part = RulePartFactory.create_part(c.tagName, c, self)
                if part.parse():
                    self.__parts.append(part)

            return True
        except Exception as ex:
            Log.exception(ex)
            return False





