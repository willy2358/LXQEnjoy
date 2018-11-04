from GCore.Statement import Statement

# <proc name="round_end" params="@p1,@p2">
class Proc(Statement):
    def __init__(self, name):
        self.__name = name
        self.__statements = []

    def get_name(self):
        return self.__name

    def add_statement(self, stm):
        self.__statements.append(stm)
