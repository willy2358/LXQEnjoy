from GCore.Statement import Statement

class Ret(Statement):
    def __init__(self, ret_val):
        self.__ret_val = ret_val

    def get_ret_value(self):
        return self.__ret_val

