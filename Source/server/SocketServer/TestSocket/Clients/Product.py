
class Product:
    def __init__(self, rule, name, times):
        self.__rule = rule
        self.__gameid = -1
        self.__coin_times = times   # the stake = self.__coin_times * coin base of game
        self.__name = name
        self.__player_limits = 0
        self.__expire_date = None

    def get_rule(self):
        return self.__rule

    def get_gameid(self):
        return self.__gameid

    def set_gameid(self, gameid):
        self.__gameid = gameid
