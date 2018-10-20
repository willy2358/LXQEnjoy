from PlayScene import PlayScene
import InterProtocol

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
        if self.__playScene.add_player(player):
            self.publish_players_status()

    def remove_player(self, player):
        if self.__playScene.remove_player(player):
            self.publish_players_status()

    def process_player_request(self, cmd, req_json):
        pass

    def get_players_status(self):
        players = []
        for p in self.__playScene.get_players():
            players.append({'userid': p.get_userid(), 'seated': p.get_seatid()})

        return players

    def publish_players_status(self):
        players = self.get_players_status()

        pack = InterProtocol.create_game_players_packet(players)
        for p in self._all_players:
            p.send_server_cmd_packet(pack)






