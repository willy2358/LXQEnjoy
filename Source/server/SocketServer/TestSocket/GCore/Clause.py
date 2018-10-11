
from GCore.Operator import Operator
from GCore.Statement import Statement

class Clause(Statement):
    def __init__(self, Op = Operator.And):
        self.__case = None
        self.__true_updates = []
        self.__false_updates = []

    def set_case(self, case):
        if case:
            self.__case = case

    def add_true_update(self, update):
        self.__true_updates.append(update)

    def add_false_update(self, update):
        self.__false_updates.append(update)

    def set_true_updates(self, updates):
        self.__true_updates = updates

    def set_false_updates(self, updates):
        self.__false_updates = updates

    def execute(self):
        if self.__case is not None and self.__case.is_satisfy():
            for u in self.__true_updates:
                u.execute()


