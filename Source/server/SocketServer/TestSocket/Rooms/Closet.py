from PlayScene import PlayScene

class Closet:
    def __init__(self, gRule, roomId = None):
        self.__gRule = gRule
        self.__roomId = roomId
        self.__playScene = PlayScene()
        self.__seated_players = []

    def get_rule(self):
        return self.__gRule

    def get_roomId(self):
        return self.__roomId

    def get_scene(self):
        return self.__playScene

    def get_seated_players(self):
        return self.__seated_players

    def get_seated_players_count(self):
        return len(self.__seated_players)

    def is_player_in(self, player):
        return player in self.__seated_players

    def add_seated_player(self, player):
        if player not in self.__seated_players:
            self.__seated_players.append(player)

    def remove_seated_player(self, player):
        if player in self.__seated_players:
            self.__seated_players.remove(player)








