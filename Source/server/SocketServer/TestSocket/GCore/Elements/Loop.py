
from GCore.Statement import Statement

class Loop(Statement):
    def __init__(self):
        self.__exit_cond = None
        self.__clauses = []

    def get_clauses(self):
        return self.__clauses

    def get_exit_condition(self):
        return self.__exit_cond

    def set_exit_case(self, case):
        self.__exit_cond = case

    def add_clause(self, clause):
        self.__clauses.append(clause)



