
from GCore.Operator import Operator
from GCore.Elements.Case import Case
import Mains.Log as Log


class Cases(Case):
    def __init__(self, op=Operator.And):
        super(Cases, self).__init__(None, None)
        self.__op = op
        self.__cases = []

    def add_case(self, case):
        self.__cases.append(case)

    def is_satisfy(self):
        if self.__op == Operator.And:
            for c in self.__cases:
                if not c:
                    return False  #短路法
            return True
        elif self.__op == Operator.Or:
            for c in self.__cases:
                if c:
                    return True  #短路法
            return False
        else:
            return False

    def gen_runtime_obj(self, scene):
        rt_funcs = []
        for c in self.__cases:
            func = c.gen_runtime_obj(scene)
            if func:
                rt_funcs.append(func)

        def test():
            Log.debug("Executing:{0} ....".format(self.get_step()))
            if self.__op == Operator.And:
                for f in rt_funcs:
                    if not f():
                        return False  # 短路法
                return True
            elif self.__op == Operator.Or:
                for f in rt_funcs:
                    if f():
                        return True  # 短路法
                return False
            else:
                return False

        return test
