
from GCore.Operand import Operand

class FuncCall(Operand):
    def __init__(self, funcName):
        self.__func_name = funcName
        self.__arguments = []

    def add_argument(self, arg):
        self.__arguments.append(arg)
