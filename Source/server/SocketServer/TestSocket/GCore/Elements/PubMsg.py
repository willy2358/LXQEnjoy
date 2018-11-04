
from GCore.Statement import Statement

class PubMsg(Statement):
    def __init__(self, rec_players, msg):
        self.__recv_players = rec_players
        self.__msg = msg
