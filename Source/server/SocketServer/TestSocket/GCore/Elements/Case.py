
from GCore.Operator import Operator
from GCore.Engine import *
from GCore.Funcs import *

# <case value_of=":(cfigure_of(@drawn_card))" ret_as="@round.bank_cfigure"/>
# <ift  value_of=":(cards_count_not_deal())" ret_is="6">
class Case:
    def __init__(self, expr1, expr2, op = Operator.Equal):
        self.__expr1 = expr1
        self.__expr2 = expr2
        self.__op = op

    def gen_runtime_obj(self, scene):
        func1 = self.__expr1.gen_runtime_obj(scene)
        func2 = self.__expr2.gen_runtime_obj(scene)
        if not func1 or not func2:
            return None

        def test():
            if self.__op == Operator.Equal:
                return func1() == func2()
            elif self.__op == Operator.NotEqual:
                return not func1() == func2()
            elif self.__op == Operator.LessThan:
                return func1() < func2()
            elif self.__op == Operator.NotLessThan:
                return not func1() < func2()
            elif self.__op == Operator.GreaterThan:
                return func1() > func2()
            elif self.__op == Operator.NotGreaterThan:
                return not func1() > func2()
        return test


