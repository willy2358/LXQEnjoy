from Mains import Errors
import secrets
import Rooms.Lobby
from Rooms.Lobby import *
import Rooms.Room
import threading

from Mains.Player import Player

class Client:
    field_client_name = "name"
    field_client_id = "clientid"
    field_auth_token = "token"
    field_player_limits = "player-limits"
    field_games = "games"
    field_game_rule_id = "ruleid"
    field_game_game_id = "gameid"
    field_game_coin_base = "coin-base"

    def __init__(self, name, clientid, token):
        self.__name = name
        self.__clientid = clientid
        self.__token = token
        self.__products = []
        
        self.__closets = {}  #{gameid:[]}
        self.__player_limits = 0   #all products share a same player limits
        self.__expire_date = None
        self.__players = {}  #{userid:player}
        self.__closet_lock = threading.Lock()

    def get_clientid(self):
        return self.__clientid

    def get_available_closet(self, gameid):
        try:
            if self.__closet_lock.acquire(10):
                if gameid not in self.__closets:
                    self.__closets[gameid] = []

                for c in self.__closets[gameid]:
                    if c.is_accept_new_player():
                        return c

                rule = self.get_rule_by_gameid(gameid)
                self.__closets[gameid].append(Closet(rule, gameid))
                return self.__closets[gameid]
        except Exception as ex:
            return None
        finally:
            self.__closet_lock.release()

    def get_player_by_id(self, userid):
        return self.__players[userid]

    def get_rule_by_gameid(self, gameid):
        for p in self.__products:
            if p.get_ruleid() == gameid:
                return p.get_rule()
        return None

    def is_player_registered(self, userid, token):
        if userid not in self.__players:
            return False
        if self.__players[userid].get_token() == token:
            return True
        else:
            return False

    def add_product(self, p):
        self.__products.append(p)

    def set_player_limits(self, limits):
        self.__player_limits = limits

    def register_player(self, userid):
        if userid in self.__players:
            return Errors.ok, self.__players[userid]
        if len(self.__players) >= self.__player_limits:
            return Errors.client_reach_players_limit, "not a token"
        player = Player(userid)
        player.set_token(secrets.token_urlsafe(20))
        self.__players[userid] = player
        return Errors.ok, self.__players[userid]

    def create_new_room(self, player, req_json):
        return None

    def process_create_room(self, player, req_json):
        # create room
        err, room = self.create_new_room(player, req_json)
        if err != Errors.ok:
            player.response_err_pack(InterProtocol.client_req_cmd_new_room, err)

        else:
            roomObj = {InterProtocol.room_id: room.get_roomid()}
            pack = InterProtocol.create_success_resp_data_pack(InterProtocol.client_req_cmd_new_room,
                                                               InterProtocol.resp_room, roomObj)
            player.response_success_pack(pack)

    def get_closet(self, gameid, roomid):
        pass

    def process_player_request(self, player, cmd, req_json):

        if cmd == InterProtocol.client_req_cmd_new_room:
            self.process_create_room(player, req_json)

        room_id = InterProtocol.room_id
        if room_id not in req_json or str(req_json[room_id]) == "-1" \
                or str(req_json[room_id]) == "0" \
                or str(req_json[room_id].lower()) == "null" \
                or str(req_json[room_id].lower()) == "none":
            Rooms.Lobby.process_player_request(player, cmd, req_json)
        else:
            Rooms.Room.process_player_request(player, cmd, req_json)