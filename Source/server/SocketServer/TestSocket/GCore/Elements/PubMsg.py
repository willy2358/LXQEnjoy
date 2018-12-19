
from GCore.Statement import Statement
import Mains.Log as Log

class PubMsg(Statement):
    def __init__(self, rec_players, msg):
        super(PubMsg, self).__init__()
        self.__recv_players = rec_players
        self.__msg = msg

    def gen_runtime_obj(self, scene):
        def pub_msg_func():
            Log.debug("Executing:{0} ....".format(self.get_step()))
            msgText = scene.get_obj_value(self.__msg)
            players = scene.get_obj_value(self.__recv_players)
            if players:
                for p in players:
                   p.publish_message(msgText)

        return pub_msg_func


