import time
from threading import Timer
import threading

from GRules.RulePart_Cards import RulePart_Cards
from GRules.RulePart_Actions import RulePart_Actions
from GRules.RulePart_Following import RulePart_Following
from GRules.RulePart_Players import RulePart_Players
from GRules.RulePart_Round import RulePart_Round
from GRules.RulePart_Running import RulePart_Running
from GRules.RulePart_Scene import RulePart_Scene
from GRules.RulePart_Procs import RulePart_Procs
from GCore.Elements.Loop import Loop

from GCore.VarRef import VarRef
from Mains.Player import Player
from GCore.FuncCall import FuncCall
from GCore.GArray import GArray

from Mains.GVar import GVar
from GCore.ValueType import ValueType
from Mains.ExtAttrs import ExtAttrs
from Mains.Round import Round
from Cards import Card
from GCore.CValue import CValue
from Cards.CFigure import CFigure
from Cards.CType import CType
from GCore.Operator import Operator

from Mains import Errors
import Mains.InterProtocol as InterProtocol
import Mains.Log as Log

import Utils

class PlayScene(ExtAttrs):
    def __init__(self, rule):
        super(PlayScene, self).__init__()
        self.__cur_round = None
        self.__history_rounds = []
        self.__players = []
        self.__rule = rule
        self.__runtimes = []
        self.__cards_space = []
        self.__pending_player = None
        self.__pending_cmds = None
        self.__pending_seconds = 0
        self.__timeout_cmd = None
        self.__pending_start_tm = time.time() #seconds

        # for exec action
        self.__cmd_player = None
        self.__cmd_args = None

        self.__procs_vars = {} #{proc_name:{var_name,gvar}}
        self.__cur_proc_ctx = ""
        self.__procs = {}
        self.__actions = {} # {act_name: (check_param, func)}
        self.__pending_cmd_lock = threading.Lock()
        self.__running_thread = None
        self.__timer_robot_exe_cmd = None

        self.parse_rule(self.__rule)


    def is_player_in(self, player):
        return player in self.__players

    def get_cur_proc_rtx(self):
        return self.__cur_proc_ctx

    def get_players(self):
        return self.__players

    def get_rule(self):
        return self.__rule

    def get_next_player(self, ref_player):
        idx = self.__players.index(ref_player)
        idx += 1
        if idx >= len(self.__players):
            idx = 0

        return self.__players[idx]

    def get_proc_local_var(self, varName, procName = None):
        Log.debug("getting var {1} of proc {0} ....".format(procName, varName))
        obj = None
        if procName in self.__procs_vars:
            if varName in self.__procs_vars[procName]:
                obj = self.__procs_vars[procName][varName]
        # if varName in self.__local_vars:
        #     return self.__local_vars[varName]
        # else:
        #     return None
        if isinstance(obj, GVar):
            Log.debug("got var {1} with value {2} in proc {0}  at obj {3}".format(procName, varName, obj.get_value(), obj))
        else:
            Log.debug("got var {1} in proc {0} with obj {2}".format(procName, varName, obj))
        return obj

    # scene has default attribute:players
    def get_runtime_objs(self, varStr):
        varStr = varStr.strip()
        if varStr.startswith("@round."):
            r = self.get_current_round()
            return r.get_attr(varStr[len("@round."):])
        elif varStr.startswith("@scene."):
            return self.get_attr(varStr[len("@scene."):])
        elif varStr == "@players":
            return self.get_attr("players")
        elif varStr == "@cmd_args":
            return self.__cmd_args
        elif varStr == "@cmd_player":
            return self.__cmd_player
        elif varStr.startswith("@cmd_player."):
            if not self.__cmd_player:
                Log.error("cmd_player should not none when used by:" + varStr)
                return None
            else:
                return self.__cmd_player.get_attr(varStr[len("@cmd_player."):])
        elif varStr.startswith("@#"):
            return self.get_proc_local_var(varStr.lstrip("@"), self.__cur_proc_ctx)
        elif varStr.startswith("@"):
            if ".[]." in varStr:
                # format  "@players.[].IsMainPlayer"
                ps = varStr.split(".[].")
                objsVar = self.get_runtime_objs(ps[0])
                insts = self.get_obj_value(objsVar)
                if isinstance(insts, list):
                    attrObjs = []
                    for inst in insts:
                        # inst is a ExtAttrs, mostly a player
                        attrObjs.append(inst.get_prop(ps[1].lstrip('@')))
                    return attrObjs
                else:
                    return objsVar
            else:
                # format @player
                return self.get_var(varStr.lstrip("@"))
        else:
            return None

    def get_obj_value(self, obj):
        if isinstance(obj, CFigure):
            return int(obj)
        if isinstance(obj, CType):
            return obj
        elif isinstance(obj, int) or isinstance(obj, bool) or isinstance(obj, str):
            return obj
        elif isinstance(obj, Player):
            return obj
        elif isinstance(obj, list):
            return obj
        elif isinstance(obj, GArray):
            return obj.gen_runtime_obj(self)()
        elif type(obj) is GVar:
            return self.get_obj_value(obj.get_value())
        elif isinstance(obj, CValue):
            return obj.get_value()
        elif type(obj) is VarRef:
            return self.get_obj_value(obj.gen_runtime_obj(self)())
        elif isinstance(obj, FuncCall):
            return self.get_obj_value(obj.gen_runtime_obj(self)())
        elif callable(obj):
            return self.get_obj_value(obj())
        else:
            return None

    def get_rt_var(self, obj):
        if isinstance(obj, GVar):
            return obj
        elif isinstance(obj, list):
            varsList = []
            for o in obj:
                if isinstance(o, GVar):
                    varsList.append(o)
                else:
                    varsList.append(self.get_rt_var(o))
            return varsList
        elif isinstance(obj, VarRef):
            return self.get_rt_var(obj.gen_runtime_obj(self)())
        elif callable(obj):
            return self.get_rt_var(obj())
        else:
            return None

    def set_cur_proc_ctx(self, ctx):
        self.__cur_proc_ctx = ctx

    def set_obj_value(self, obj, value):
        if isinstance(obj, VarRef):
            var = obj.gen_runtime_obj(self)()
            if isinstance(var, GVar):
                var.set_value(value)

    def add_proc_local_var(self, varName, vType, value, scope):
        if not scope:
            scope = self.__cur_proc_ctx

        if scope not in self.__procs_vars:
            self.__procs_vars[scope] = {}
        Log.debug("creating var {1} for proc {0} with value {2}".format(scope, varName, value))
        self.__procs_vars[scope][varName] = GVar(varName, vType, value)
        # if varName not in self.__procs_vars[scope]:
        #     self.__procs_vars[scope][varName] = GVar(varName, vType, value)
        # self.__local_vars[varName] = GVar(varName, vType, value)

    def get_current_round(self):
        return self.__cur_round

    def is_meet_conditions(self, inst, named_attrs, op):
        # no requirements, return false
        if not named_attrs:
            return False

        if op == Operator.Or:
            for k in named_attrs:
                if self.get_obj_value(named_attrs[k]) == self.get_obj_value(inst.get_prop(k)):
                    return True
            return False
        if op == Operator.And:

            for k in named_attrs:
                val1 = self.get_obj_value(named_attrs[k])
                val2 = self.get_obj_value(inst.get_prop(k))
                # if len(named_attrs) == 1 and val1 == val2:
                #     return True
                if val1 != val2:
                    return False
            return True
        return False

    def draw_cards(self, count):
        return  self.__cur_round.draw_cards(count)

    def add_player(self, player):
        if player not in self.__players:
            self.__players.append(player)
            self.init_player_attrs(player)
            return True
        else:
            return False

    def is_waiting_player_act(self):
        return self.__pending_player

    def init_player_attrs(self, player):
        playerPart = self.__rule.get_part_by_name(RulePart_Players.PART_NAME)
        if not playerPart:
            return

        for attr in playerPart.get_custom_attrs():
            name = attr.get_name()
            vtype = attr.get_value_type()
            val = attr.get_value()
            player.add_cus_attr(name, vtype, val)

    def _append_rt_obj(self, obj, nodeName):
        self.__runtimes.append((obj, nodeName))


    def remove_player(self, player):
        if player in self.__players:
            self.__players.remove(player)
            return True
        return False

    def has_vacancy(self):
        return len(self.__players) < self.__rule.get_max_players_capacity()

    def parse_rule(self, rule):
        self.load_cards_space(rule)
        self.load_scene_attrs(rule)
        self.load_procedures(rule)
        self.load_actions(rule)

        partRun = rule.get_part_by_name(RulePart_Running.PART_NAME)
        assert partRun
        rt = None
        for stm in partRun.get_statements():
            obj = stm.gen_runtime_obj(self)
            if obj:
                self._append_rt_obj(obj, type(stm))

    def load_cards_space(self, rule):
        cards_set= Card.get_cards(rule.get_gtype())
        cardsPart = rule.get_part_by_name(RulePart_Cards.PART_NAME)
        if not cardsPart:
            self.__cards_space = cards_set
            return
        excludes = cardsPart.get_excluded_cards()
        for ex in excludes:
            while cards_set.index(ex) >= 0:
                cards_set.remove(ex)

        sets = 1
        c = cardsPart.get_card_sets()
        if c > 1:
            sets = c
        self.__cards_space = cards_set * sets

    def load_scene_attrs(self, rule):
        scenePart = rule.get_part_by_name(RulePart_Scene.PART_NAME)
        if scenePart:
            for attr in scenePart.get_custom_attrs():
                name = attr.get_name()
                vtype = attr.get_value_type()
                val = attr.get_value()
                self.add_cus_attr(name, vtype, val)

    def load_procedures(self, rule):
        procsPart = rule.get_part_by_name(RulePart_Procs.PART_NAME)
        for proc in procsPart.get_procs():
            func = proc.gen_runtime_obj(self)
            if callable(func):
                self.__procs[proc.get_name()] = (proc.get_param_names(), func)

    def load_actions(self, rule):
        actsPart = rule.get_part_by_name(RulePart_Actions.PART_NAME)
        if not actsPart:
            return

        for act in actsPart.get_actions():
            funcObj = act.gen_runtime_obj(self)
            if callable(funcObj):
                self.__actions[act.get_name()] = (act.gen_param_check_func(self), funcObj)

    def start_game(self):
        self.init_player_type_attrs()

        self.__running_thread = threading.Thread(group=None, target=self.run)
        self.__running_thread.setDaemon(True)
        self.__running_thread.start()


    def waiting_for_player_exe_cmd(self):
            waiting = True
            while self.__pending_player and waiting:
                if self.__pending_cmd_lock.acquire():
                    if not self.__pending_player and not self.__pending_cmds:
                        waiting = False
                    if waiting:
                        time.sleep(0.2)  # sleep 0.2 seconds
                        if int(time.time()) % 10 == 0:
                            # Log.debug("waiting_for_player_exe_cmd, thread:{0}".format(threading.get_ident()))
                            Log.debug("waiting for player {0} action, in thread:{1} ...".format(self.__pending_player.get_userid(),threading.get_ident()))
                        # 超时, 执行默认命令
                        if 0 < self.__pending_seconds < time.time() - self.__pending_start_tm:
                            if self.__timeout_cmd:
                                defcmd = self.__timeout_cmd
                            else:
                                defcmd = self.__pending_cmds[0]

                            cmd, cmd_args = defcmd.get_cmd(), defcmd.get_cmd_param()
                            self.auto_exe_default_cmd(self.__pending_player, cmd, cmd_args)

                    self.__pending_cmd_lock.release()

    def next_statement(self):
        # if self.__pending_player:
        #     yield None
        # else:
        for (rtObj,tName) in self.__runtimes:
            if self.is_waiting_player_act():
                return
            if str(tName) == str(Loop):
                yield from rtObj()
            else:
                yield rtObj

    def init_player_type_attrs(self):
        if not self.__players:
            return
        attrs = self.get_attrs()
        for attr in attrs:
            # attr is a GVar
            if attrs[attr].get_value_type() == ValueType.player:
                val = attrs[attr].get_value()
                if type(val) is CValue:
                    if val.get_value() == "random":
                        attrs[attr].set_value(self.__players[0])
        self.add_cus_attr("players", ValueType.players, self.__players)

    def call_proc(self, proc_name, args):
        if proc_name in self.__procs:
            params = self.__procs[proc_name][0]
            if params:
                for i in range(len(params)):
                    if i < len(args):
                        gVar = self.get_proc_local_var(params[i], proc_name)
                        if gVar:
                            gVar.set_value(args[i])

            return self.__procs[proc_name][1]()
        else:
            return None

    def create_new_round(self):
        newRound = Round()
        roundPart = self.__rule.get_part_by_name(RulePart_Round.PART_NAME)
        if roundPart:
            for attr in roundPart.get_custom_attrs():
                name = attr.get_name()
                vtype = attr.get_value_type()
                val = attr.get_value()
                newRound.add_cus_attr(name, vtype, val)
            newRound.set_debug_cards(roundPart.get_debug_cards())

        newRound.init_cards_pack(self.__cards_space)
        newRound.add_cus_attr("players", ValueType.players, self.__players)
        self.__history_rounds.append(newRound)
        self.__cur_round = newRound


    def send_player_cmd_opts(self, player, cmds, timeout_seconds, timeout_act):
        pack = InterProtocol.create_cmd_options_json_packet(player, cmds, timeout_act, timeout_seconds)
        if player and player.send_server_cmd_packet(pack):
            self.__pending_player = player
            self.__pending_cmds = cmds
            self.__pending_seconds = int(timeout_seconds)
            self.__timeout_cmd = timeout_act
            self.__pending_start_tm = time.time()

            if self.__timer_robot_exe_cmd:
                self.__timer_robot_exe_cmd.cancel()

            self.__timer_robot_exe_cmd = Timer(self.__pending_seconds, self.timer_exe_default_cmd)
            self.__timer_robot_exe_cmd.start()

    def timer_exe_default_cmd(self):
        if self.__timer_robot_exe_cmd and self.__timer_robot_exe_cmd.is_alive():
            with self.__pending_cmd_lock:
                if self.__timeout_cmd:
                    defcmd = self.__timeout_cmd
                else:
                    defcmd = self.__pending_cmds[0]

                self.__timer_robot_exe_cmd.cancel()

                cmd, cmd_args = defcmd.get_cmd(), defcmd.get_cmd_param()
                self.auto_exe_default_cmd(self.__pending_player, cmd, cmd_args)

                self.__timer_robot_exe_cmd = None
            # for stm in self.next_statement():
            #     if callable(stm):
            #         stm()
            #     if not stm:
            #         break
            self.go_progress()

        Log.debug("XXXXXXXXXLeaving act")

    def process_player_play_cards(self, player, cards, cmd_alias = InterProtocol.server_push_play_cards,
                                  faces_up = True, quiet = False):
        cmd = cmd_alias if cmd_alias else InterProtocol.server_push_play_cards
        pack = InterProtocol.create_play_cards_packet(player, cards, cmd)
        player.send_server_cmd_packet(pack)

        if not quiet:
            cmd_args = cards
            if not faces_up:
                cmd_args = ['*' for i in range(len(cards))]

            pack = InterProtocol.create_play_cards_packet(player, cmd_args, cmd_alias)
            for p in self.get_players():
                if p is not player:
                    p.send_server_cmd_packet(pack)

        player.play_cards(cards)

    #当相同命令只有一个时，玩家可以不发送命令参数，只发送命令即可
    #当相同命令有多个时，玩家需要发送命令参数，且参数需匹配
    def check_player_cmd_param(self, player, cmd, cmd_args):
        cmdObjs = []
        for c in self.__pending_cmds:
            if c.get_cmd() == cmd:
                cmdObjs.append(c)

        if not cmdObjs:
            player.response_err_pack(InterProtocol.client_req_type_exe_cmd, Errors.invalid_cmd)
            return None, None

            # 多个相同的命令，但参数不同，需要进一步检查实参，确定玩家选择
        validCmd, validParam = cmd, cmd_args
        if len(cmdObjs) > 1:
            argMatch = False
            for c in cmdObjs:
                if c.get_cmd_param() == cmd_args:
                    argMatch = True
            if not argMatch:
                player.response_err_pack(InterProtocol.client_req_type_exe_cmd, Errors.invalid_cmd_param)
                return None, None
        else:
            args = cmdObjs[0].get_cmd_param()
            validCmdParam = args if args else cmd_args

        return validCmd, validCmdParam

    def auto_exe_default_cmd(self, player, cmd, cmd_args):

        act_stms = None
        if cmd in self.__actions:
            act_stms = self.__actions[cmd]

        # 准备参数
        self.__cmd_player = player
        self.__cmd_args = cmd_args

        if callable(act_stms[0]):  # has param checker
            # 优先使用param_check检查参数
            ret = act_stms[0]()
            if not ret:
                player.response_err_pack(InterProtocol.client_req_type_exe_cmd, Errors.invalid_cmd_param)
                return

        # 执行内部逻辑
        if callable(act_stms[1]):
            act_stms[1]()

        Log.debug("Auto exed default action, player: {0}, exed action: {1}".format(self.__pending_player.get_userid(), cmd))
        # 重置，允许继续执行后面的命令
        self.__pending_player = None
        self.__pending_cmds = None

    def process_player_exed_cmd(self, player, cmd, cmd_args):
        with self.__pending_cmd_lock:
            if player != self.__pending_player:
                player.response_err_pack(InterProtocol.client_req_type_exe_cmd, Errors.player_not_pending_cmd)
            else:
                args = cmd_args
                c, args = self.check_player_cmd_param(player, cmd, cmd_args)
                if not c:
                    return

                act_stms = None
                if cmd in self.__actions:
                    act_stms = self.__actions[cmd]

                if not act_stms:
                    Log.error("Action {0} lacking of configuration".format(cmd))
                    player.response_err_pack(InterProtocol.client_req_type_exe_cmd, Errors.invalid_cmd)
                    return

                # 准备参数
                self.__cmd_player = player
                self.__cmd_args = args

                if callable(act_stms[0]):  # has param checker
                    # 优先使用param_check检查参数
                    ret = act_stms[0]()
                    if not ret:
                        player.response_err_pack(InterProtocol.client_req_type_exe_cmd, Errors.invalid_cmd_param)
                        return

                if self.__timer_robot_exe_cmd:
                    self.__timer_robot_exe_cmd.cancel()
                    self.__timer_robot_exe_cmd = None

                # 执行内部逻辑
                if callable(act_stms[1]):
                    act_stms[1]()

                Log.debug("player {0} exed action {1}".format(self.__pending_player.get_userid(), cmd))
                # 重置，允许继续执行后面的命令
                self.__pending_player = None
                self.__pending_cmds = None
    def go_progress(self):
        for stm in self.next_statement():
            stm()

    def run(self):
        self.create_new_round()
        # stm = None
        # while True:
        #     stm = self.next_statement()
        #     if callable(stm):
        #         stm()
        #     if not stm:
        #         break
        self.go_progress()
            # if callable(stm):
            #     stm()
            # if not stm and self.__pending_player:
            #     break
        Log.debug("XXXXXXXXXLeaving run")
        # for rtObj in self.__runtimes:
        #     rtObj()
        #     self.waiting_for_player_exe_cmd()

