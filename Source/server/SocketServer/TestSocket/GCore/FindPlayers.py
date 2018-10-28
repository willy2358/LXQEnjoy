from GCore.Statement import Statement

class FindPlayers(Statement):
    def __init__(self):
        self.__test_prop = None
        self.__test_value = ""
        self.__from_var = None
        self.__statements = []

    def set_from_var(self, var_name):
        self.__from_var = var_name

    def set_test_property(self, propName, value):
        self.__test_prop = propName
        self.__test_value = value

    def add_statement(self, statement):
        self.__statements.append(statement)