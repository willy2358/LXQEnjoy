
class PlayScene:
    def __init__(self):
        self.__cur_round = None
        self.__history_rounds = []
        self.__players = []


    def get_players(self):
        return self.__players

    def add_player(self, player):
        if player not in self.__players:
            self.__players.append(player)

    def remove_player(self, player):
        if player in self.__players:
            self.__players.remove(player)
