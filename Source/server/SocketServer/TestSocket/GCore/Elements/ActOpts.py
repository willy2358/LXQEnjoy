
from GCore.Statement import Statement
from Mains.Player import Player
import Mains.Log as Log

import Mains.InterProtocol as InterProtocol
# from Mains.PlayScene import PlayScene

# <act_opts timeout="30" timeout_act="pass" to_player="@drawer">
#                     <act_opt act="jiaozhu"/>
#                     <act_opt act="pass"/>
#                 </act_opts>

class ActOpts(Statement):
    def __init__(self, to_player, timeout_sec, timeout_act):
        self.__to_player = to_player
        self.__timeout_seconds = timeout_sec
        self.__timeout_act = timeout_act
        self.__opts = []

    def add_act_opt(self, act_opt):
        self.__opts.append(act_opt)

    def gen_runtime_obj(self, scene):
        def send_act_opts():
            try:
                recv_player = scene.get_obj_value(self.__to_player)
                cmd_opts = []
                def_act = None
                for opt in self.__opts:
                    cmdObj = opt.gen_runtime_obj(scene)()
                    cmdObj.set_cmd_player(recv_player)
                    cmd_opts.append(cmdObj)
                    if opt.get_act_name() == self.__timeout_act:
                        def_act = cmdObj

                pack = InterProtocol.create_cmd_options_json_packet(recv_player, cmd_opts, def_act, self.__timeout_seconds)
                if recv_player.send_server_cmd_packet(pack):
                    scene.set_pending_player_and_cmds(cmd_opts, self.__timeout_seconds, def_act)
            except Exception as ex:
                Log.exception(ex)
        return send_act_opts
