

from GCore.Statement import Statement
import Mains.Log as Log

class PubPlayerStatus(Statement):
    def __init__(self, rec_players):
        super(PubPlayerStatus, self).__init__()
        self.__recv_players = rec_players

    def gen_runtime_obj(self, scene):
        def pub_player_status():
            Log.debug("Executing:{0} ....".format(self.get_step()))
            players = scene.get_obj_value(self.__recv_players)
            if players:
                for p in players:
                    scene.pub_player_status(p)
                   # p.pub_my_status()

        return pub_player_status
