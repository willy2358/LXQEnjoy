from GCore.Statement import Statement

class Proc(Statement):
    def __init__(self, name):
        self.__name = name
        self.__statements = []

    def get_name(self):
        return self.__name

    def add_statement(self, stm):
        self.__statements.append(stm)
