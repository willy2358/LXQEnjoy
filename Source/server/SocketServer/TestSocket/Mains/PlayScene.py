
from GRules.RulePart_Cards import RulePart_Cards
from GRules.RulePart_Actions import RulePart_Actions
from GRules.RulePart_Following import RulePart_Following
from GRules.RulePart_Players import RulePart_Players
from GRules.RulePart_Round import RulePart_Round
from GRules.RulePart_Running import RulePart_Running
from GRules.RulePart_Scene import RulePart_Scene
from GRules.RulePart_Procs import RulePart_Procs

from GCore.Elements.Variable import Variable
from GCore.Elements.Loop import Loop
from GCore.Elements.ActRefs import ActRefs
from GCore.Elements.ActRef import ActRef
from GCore.Elements.ProcRef import ProcRef
from GCore.Elements.Action import Action
from GCore.Elements.Delay import Delay
from GCore.Elements.PubMsg import PubMsg
from GCore.Elements.FindPlayer import FindPlayer
from GCore.Elements.FindPlayers import FindPlayers
from GCore.Elements.Clause import Clause
from GCore.Elements.ActOpts import ActOpts
from GCore.Elements.Case import Case
from GCore.Elements.Cases import Cases

class PlayScene:
    def __init__(self, rule):
        self.__cur_round = None
        self.__history_rounds = []
        self.__players = []
        self.__rule = rule
        self.__cus_attrs = {}
        self.__vars = {} # name:['val_type', 'value']
        self.parse_rule(self.__rule)
        self.__runtimes = []

    def is_player_in(self, player):
        return player in self.__players

    def get_players(self):
        return self.__players

    def get_attr_value(self, attrName):
        if attrName in self.__cus_attrs:
            return self.__cus_attrs[attrName]
        else:
            return None

    def add_cus_attr(self, attrName, attrVal=None):
        self.__cus_attrs[attrName] = attrVal

    def add_player(self, player):
        if player not in self.__players:
            self.__players.append(player)
            return True
        else:
            return False

    def __append_rt_obj(self, obj):
        self.__runtimes.append(obj)

    def add_variable(self, name, vtype, value):
        if name not in self.__vars:
            self.__vars[name] = [vtype, value]

    def update_variable(self, name, value):
        if name not in self.__vars:
            self.__vars[name] = ['undef', value]
        else:
            self.__vars[name][1] = value

    def remove_player(self, player):
        if player in self.__players:
            self.__players.remove(player)
            return True
        return False

    def has_vacancy(self):
        return len(self.__players) < self.__rule.get_max_players_capacity()

    def parse_rule(self, rule):
        partRun = rule.get_part_by_name(RulePart_Running.PART_NAME)
        assert partRun
        rt = None
        for stm in partRun.get_statements():
            obj = stm.gen_runtime_obj(self)
            if obj:
                self.__append_rt_obj(obj)

    def prepare_start(self):
        player_part = self.__rule.get_part_by_name(RulePart_Players.PART_NAME)

    def start_game(self):
        self.prepare_start()

        run_part = self.__rule.get_part_by_name(RulePart_Running.PART_NAME)

        codeBlocks = run_part.get_code_blocks()
        for i in range(len(codeBlocks)):
            self.exe_block(codeBlocks[i])

    def exe_block(self, code_block):
        pass





