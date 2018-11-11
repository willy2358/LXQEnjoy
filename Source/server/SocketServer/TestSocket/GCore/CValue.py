
from GCore.Operand import Operand

#const value
class CValue(Operand):
    def __init__(self, val):
        self.__val = val

    def get_result(self):
        return self.__val

    def gen_runtime_obj(self, scene):
        def ret_val():
            return self.__val
        return ret_val