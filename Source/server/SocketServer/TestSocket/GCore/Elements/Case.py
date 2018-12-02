
from GCore.Operator import Operator
from GCore.Engine import *
from GCore.Funcs import *
import Mains.Log as Log
from GCore.Statement import Statement

# <case value_of=":(cfigure_of(@drawn_card))" ret_as="@round.bank_cfigure"/>
# <ift  value_of=":(cards_count_not_deal())" ret_is="6">
class Case(Statement):
    def __init__(self, expr1, expr2, op = Operator.Equal):
        super(Case, self).__init__()
        self.__expr1 = expr1
        self.__expr2 = expr2
        self.__op = op

    def gen_runtime_obj(self, scene):
        def test():
            # func1 = self.__expr1.gen_runtime_obj(scene)
            # func2 = self.__expr2.gen_runtime_obj(scene)
            # if not func1 or not func2:
            #     return False
            Log.debug("Executing:{0} ....".format(self.get_step()))
            try:
                f1 = scene.get_obj_value(self.__expr1)
                f2 = scene.get_obj_value(self.__expr2)
                if isinstance(f1, list) and len(f1) == 0:
                    f1 = None
                ret = False
                if self.__op == Operator.Equal:
                    ret = (str(f1).lower() == str(f2).lower())
                elif self.__op == Operator.NotEqual:
                    ret = (not (str(f1).lower() == str(f2).lower()))
                elif self.__op == Operator.LessThan:
                    ret = (int(f1) < int(f2))
                elif self.__op == Operator.NotLessThan:
                    ret = (not (int(f1) < int(f2)))
                elif self.__op == Operator.GreaterThan:
                    ret = (int(f1) > int(f2))
                elif self.__op == Operator.NotGreaterThan:
                    ret = (not (int(f1) > int(f2)))
                return ret
            except Exception as ex:
                Log.exception(ex)
                return False
        return test


