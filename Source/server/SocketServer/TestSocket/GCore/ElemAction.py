from GCore.Statement import Statement

class Action(Statement):
    def __init__(self, name):
        self.__name = name
        self.__statements = []

    def add_statement(self, stm):
        self.__statements.append(stm)
