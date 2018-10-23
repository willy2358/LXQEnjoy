from GCore.Operand import Operand

class Variable(Operand):
    def __init__(self, varName):
        self.__var_name = varName

