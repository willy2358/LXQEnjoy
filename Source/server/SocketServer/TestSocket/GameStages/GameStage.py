

class GameStage:
    def __init__(self, rule):
        self.__my_rule = rule
        self.__my_round = None
        self.__my_players = None

    def get_my_rule(self):
        return self.__my_rule

    def get_my_round(self):
        return self.__my_round

    def set_my_round(self, my_round):
        self.__my_round = my_round

    def begin(self):
        pass


