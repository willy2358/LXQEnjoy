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

    def gen_runtime_obj(self, scene):
        def find_players():
            retPs = []
            players = scene.get_players()
            for p in players:
                if p.is_attr_meet(self.__test_prop, self.__test_value):
                    retPs.append(p)
        return find_players