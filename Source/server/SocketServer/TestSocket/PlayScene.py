
class PlayScene:
    def __init__(self, rule):
        self.__cur_round = None
        self.__history_rounds = []
        self.__players = []
        self.__rule = rule

    def is_player_in(self, player):
        return player in self.__players

    def get_players(self):
        return self.__players

    def add_player(self, player):
        if player not in self.__players:
            self.__players.append(player)
            return True
        else:
            return False

    def remove_player(self, player):
        if player in self.__players:
            self.__players.remove(player)
            return True
        return False

    def has_vacancy(self):
        return len(self.__players) < self.__rule.get_max_players_capacity()





