
class Product:
    def __init__(self, gRule, name, times):
        self.__gRule = gRule
        self.__coin_times = times   # the stake = self.__coin_times * coin base of game
        self.__name = name
        self.__player_limits = 0
        self.__expire_date = None