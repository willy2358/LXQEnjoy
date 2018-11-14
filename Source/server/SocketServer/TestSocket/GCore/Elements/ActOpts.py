
from GCore.Statement import Statement
from Mains.Player import Player

import Mains.InterProtocol as InterProtocol
from Mains.PlayCmd import PlayCmd

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
            # func = self.__to_player.gen_runtime_obj(scene)
            # playerRef = func()
            # player = scene.get_prop_value(playerRef.get_name())
            # if type(player) is Player:
            #     cmd_opts = []
            #     cmd_opts.append(PlayCmd(player, InterProtocol.majiang_player_act_hu, new_cards))
            #     packet = InterProtocol.create_cmd_options_json_packet(player, cmd_opts, self.__timeout_act, self.__timeout_seconds)
            #     player.send_server_cmd_packet(packet)
            pass
        return send_act_opts
