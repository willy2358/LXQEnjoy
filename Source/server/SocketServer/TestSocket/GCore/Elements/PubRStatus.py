from GCore.Statement import Statement
import Mains.Log as Log

class PubRoundStatus(Statement):
    def __init__(self, rec_players):
        super(PubRoundStatus, self).__init__()
        self.__recv_players = rec_players

    def gen_runtime_obj(self, scene):
        def pub_round_status():
            Log.debug("Executing:{0} ....".format(self.get_step()))
            players = scene.get_obj_value(self.__recv_players)
            if players:
                scene.pub_round_status(players)

        return pub_round_status