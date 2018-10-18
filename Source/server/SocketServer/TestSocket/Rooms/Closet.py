from PlayScene import PlayScene

class Closet:
    def __init__(self, gRule, roomId = None):
        self.__gRule = gRule
        self.__roomId = roomId
        self.__playScene = PlayScene()
        self._players = []

    def get_rule(self):
        return self.__gRule

    def get_roomId(self):
        return self.__roomId

    def get_scene(self):
        return self.__playScene

    def get_scene_players(self):
        return self.__playScene.get_players()

    def get_players_count(self):
        return len(self._players)

    def is_player_in(self, player):
        return player in self._players

    def add_player(self, player):
        if player not in self._players:
            self._players.append(player)

    def remove_player(self, player):
        if player in self._players:
            self._players.remove(player)

        self.__playScene.remove_player(player)








