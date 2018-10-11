
from GCore.Operator import Operator
from GCore.Case import Case


class Cases(Case):
    def __init__(self, op=Operator.And):
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