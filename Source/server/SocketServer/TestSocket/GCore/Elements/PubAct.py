
from GCore.Statement import Statement
import Mains.Log as Log
import Mains.InterProtocol as InterProtocol


class PubAct(Statement):
    def __init__(self, exe_player, to_players, act, act_args):
        super(PubAct, self).__init__()
        self.__to_players = to_players
        self.__act = act
        self.__act_args = act_args
        self.__exe_player = exe_player

    def gen_runtime_obj(self, scene):
        def pub_act_func():
            try:
                rec_players = scene.get_obj_value(self.__to_players)
                exe_player = scene.get_obj_value(self.__exe_player)
                if rec_players and scene and exe_player:
                    cmd_args = scene.get_obj_value(self.__act_args)
                    pack = InterProtocol.create_player_exed_cmd_json_packet(exe_player, self.__act, cmd_args)

                    if isinstance(rec_players, list):
                        for p in rec_players:
                            p.send_server_cmd_packet(pack)
                    else:  # most time, rec_players is #cmd_player
                        rec_players.send_server_cmd_packet(pack)
            except Exception as ex:
                Log.exception(ex)

        return pub_act_func