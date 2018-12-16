from Mains.PlayScene import PlayScene
from Mains import InterProtocol
import Mains.Errors as Errors


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

    def get_all_players(self):
        return self.__playScene.get_players()

    def is_player_in(self, player):
        return self.__playScene.is_player_in(player)

    def is_accept_new_player(self):
        return self.__playScene.has_vacancy()

    def add_player(self, player):
        if self.__playScene.add_player(player):
            player.set_closet(self)
            return True
        else:
            return False


    def remove_player(self, player):
        if self.__playScene.remove_player(player):
            self.publish_players_status()

    def process_player_request(self, player, cmd, req_json):
        if cmd == InterProtocol.client_req_type_exe_cmd:
            cmdTxt = req_json[InterProtocol.client_req_exe_cmd]
            cmdArgs = req_json[InterProtocol.client_req_cmd_param]
            self.__playScene.process_player_exed_cmd(player, cmdTxt, cmdArgs, False)
        elif cmd == InterProtocol.client_req_get_cards:
            pack = InterProtocol.create_player_cards_data_pack(player)
            player.send_server_cmd_packet(pack)

    def get_players_status(self):
        players = []
        for p in self.__playScene.get_players():
            players.append({'userid': p.get_userid(), 'seated': p.get_seatid()})

        return players

    def test_to_start_game(self):
        # reached the min players,  start game.
        if len(self.__playScene.get_players()) >= self.__gRule.get_min_players_capacity():
            self.__playScene.start_game()

    def publish_players_status(self):
        players = self.get_players_status()

        pack = InterProtocol.create_game_players_packet(players)
        for p in self.get_all_players():
            p.send_server_cmd_packet(pack)






