class Product:
    def __init__(self, rule, gameid, times):
        self.__rule = rule
        self.__gameid = gameid
        self.__coin_times = times   # the stake = self.__coin_times * coin base of game


    def get_rule(self):
        return self.__rule

    def get_gameid(self):
        return self.__gameid

    def set_gameid(self, gameid):
        self.__gameid = gameid

    

