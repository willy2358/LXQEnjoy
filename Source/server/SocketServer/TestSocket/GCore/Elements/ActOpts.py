
from GCore.Statement import Statement

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
        pass
