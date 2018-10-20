from PlayScene import PlayScene

class Closet:
    def __init__(self, gRule, gameid, roomId = None):
        self.__gRule = gRule
        self.__roomId = roomId
        self.__gameid = gameid
        self.__playScene = PlayScene(gRule)

    def get_rule(self):
        return self.__gRule

    def get_roomId(self):
        return self.__roomId

    def get_scene(self):
        return self.__playScene

    def get_scene_players(self):
        return self.__playScene.get_players()

    def is_player_in(self, player):
        return self.__playScene.is_player_in(player)

    def is_accept_new_player(self):
        return self.__playScene.has_vacancy()

    def add_player(self, player):
        self.__playScene.add_player(player)

    def remove_player(self, player):
        self.__playScene.remove_player(player)

    def process_player_request(self, cmd, req_json):
        pass


    def start_game(self):
        pass






