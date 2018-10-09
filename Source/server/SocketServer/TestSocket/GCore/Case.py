
from GCore.Operator import Operator
from GCore.Engine import *

class Case:
    def __init__(self, expr1, expr2, op = Operator.Equal):
        self.__expr1 = expr1
        self.__expr2 = expr2
        self.__op = op

    def is_satisfy(self):
        if self.__op == Operator.Equal:
            return value_of(self.__expr1) == value_of(self.__expr2)
        elif self.__op == Operator.NotEqual:
            return  not value_of(self.__expr1) == value_of(self.__expr2)
        elif self.__op == Operator.LessThan:
            return value_of(self.__expr1) < value_of(self.__expr2)
        elif self.__op == Operator.NotLessThan:
            return not value_of(self.__expr1) < value_of(self.__expr2)
        elif self.__op == Operator.GreaterThan:
            return value_of(self.__expr1) > value_of(self.__expr2)
        elif self.__op == Operator.NotGreaterThan:
            return not value_of(self.__expr1) > value_of(self.__expr2)


