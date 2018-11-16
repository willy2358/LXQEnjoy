
from GCore.Statement import Statement

# <act_ref act="playcard"/>
class ActRef(Statement):
    def __init__(self, act_ref, params):
        self.__act_ref = act_ref
        self.__params = params




