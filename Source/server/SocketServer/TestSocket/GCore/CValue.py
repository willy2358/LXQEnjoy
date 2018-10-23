
from GCore.Operand import Operand

class CValue(Operand):
    def __init__(self, val):
        self.__val = val

    def get_result(self):
        return self.__val