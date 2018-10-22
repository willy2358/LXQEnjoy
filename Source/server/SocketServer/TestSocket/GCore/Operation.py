
from GCore.Operator import Operator
class Operation:
    def __init__(self, operand1, operand2, operator = Operator.Add):
        self.__result_name = None
        self.__operator = operator
        self.__operand1 = operand1
        self.__operand2 = operand2

    def set_result_name(self, name):
        self.__result_name = name
