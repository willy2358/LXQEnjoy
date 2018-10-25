from GCore.Operand import Operand
from GCore.ValueType import ValueType

class Variable(Operand):
    def __init__(self, varName):
        self.__name = varName
        self.__value_type = ValueType.integer
        self.__value = None

    def get_value(self):
        return self.__value

    def set_value_type(self, vtype):
        self.__value_type = vtype

    def set_value(self, val):
        self.__value = val


