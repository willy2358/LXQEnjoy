from GCore.Operand import Operand

class VarRef(Operand):
    def __init__(self, var):
        self.__var = var