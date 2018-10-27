from GCore.Statement import Statement

class FindPlayer(Statement):
    def __init__(self):
        self.__test_prop = None
        self.__test_value = ""
        self.__from_var = None

    def set_from_var(self, var_name):
        self.__from_var = var_name


    def set_test_property(self, propName, value):
        self.__test_prop = propName
        self.__test_value = value



