
from GCore.Operator import Operator
from GCore.Engine import *
from GCore.Funcs import *
import Mains.Log as Log

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
            try:
                f1 = func1()
                f2 = func2()
                ret = False
                if self.__op == Operator.Equal:
                    ret = (func1() == func2())
                elif self.__op == Operator.NotEqual:
                    ret = (not (func1() == func2()))
                elif self.__op == Operator.LessThan:
                    ret = (int(f1) < int(f2))
                elif self.__op == Operator.NotLessThan:
                    ret = (not int(f1) < int(f2))
                elif self.__op == Operator.GreaterThan:
                    ret = (int(f1) > int(f2))
                elif self.__op == Operator.NotGreaterThan:
                    ret = (not int(f1) > int(f2))
                return ret
            except Exception as ex:
                Log.exception(ex)
                return False
        return test


