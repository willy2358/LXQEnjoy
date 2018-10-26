
from GCore.Operator import Operator
from GCore.Statement import Statement

class Clause(Statement):
    def __init__(self, Op = Operator.And):
        self.__case = None
        self.__true_statements = []
        self.__false_statements = []

    def get_true_statements(self):
        return self.__true_statements

    def get_false_statements(self):
        return self.__false_statements

    def set_case(self, case):
        if case:
            self.__case = case

    def add_true_statement(self, update):
        self.__true_statements.append(update)

    def add_false_statement(self, update):
        self.__false_statements.append(update)

    def set_true_statements(self, updates):
        self.__true_statements = updates

    def set_false_statements(self, updates):
        self.__false_statements = updates


    def execute(self):
        if self.__case is not None and self.__case.is_satisfy():
            for u in self.__true_statements:
                u.execute()


