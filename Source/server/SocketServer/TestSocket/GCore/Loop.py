
class Loop:
    def __init__(self):
        self.__exit_condition = None
        self.__clauses = []

    def set_exit_condition(self, condition):
        self.__exit_condition = condition

    def add_clause(self, clause):
        self.__clauses.append(clause)