
from GCore.Operator import Operator
from GCore.Expression import Expression

class Clause(Expression):
    def __init__(self, Op = Operator.And):
        self.__case = None
        self.__updates = []

    def set_case(self, case):
        self.__case = case

    def add_update(self, update):
        self.__updates.append(update)

    def execute(self):
        if self.__case is not None and self.__case.is_satisfy():
            for u in self.__updates:
                u.execute()


