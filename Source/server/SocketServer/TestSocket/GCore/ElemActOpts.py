
from GCore.Statement import Statement

class ActOpts(Statement):
    def __init__(self, to_player, timeout_sec, timeout_act):
        self.__to_player = to_player
        self.__timeout_seconds = timeout_sec
        self.__timeout_act = timeout_act
        self.__opts = []

    def add_act_opt(self, act_opt):
        self.__opts.append(act_opt)

