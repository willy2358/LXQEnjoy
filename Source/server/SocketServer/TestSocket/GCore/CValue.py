
from GCore.Operand import Operand

#const value
class CValue(Operand):
    def __init__(self, val):
        self.__val = val

    def get_result(self):
        return self.__val