
from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
import base64

import Mains.Errors as Err
import secrets
import Rooms.Lobby
from Rooms.Lobby import *
import Rooms.Room
from Rooms.Closet import Closet
from Rooms.Room import Room
import threading
import Mains.Log as Log

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
    field_key_file = "key-file"

    def __init__(self, name, clientid, token):
        self.__name = name
        self.__clientid = clientid
        self.__token = token
        self.__products = []
        
        self.__lobby_closets = {}  #{gameid:[]}
        self.__rooms = {} # {roomid:room}
        self.__player_limits = 0   #all products share a same player limits
        self.__expire_date = None
        self.__players = {}  #{userid:player}
        self.__closet_lock = threading.Lock()
        self.__rsaKey = None

    def init_rsakey(self, keyFile):
        self.__rsaKey = RSA.importKey(open(keyFile).read())

    def get_clientid(self):
        return self.__clientid

    def get_token(self):
        return self.__token

    def get_available_lobby_closet(self, gameid):
        try:
            if self.__closet_lock.acquire(10):
                if gameid not in self.__lobby_closets:
                    self.__lobby_closets[gameid] = []

                for c in self.__lobby_closets[gameid]:
                    if c.is_accept_new_player():
                        return c

                rule = self.get_rule_by_gameid(gameid)
                newCloset = Closet(rule, gameid)
                self.__lobby_closets[gameid].append(newCloset)
                return newCloset
        except Exception as ex:
            Log.exception(ex)
            return None
        finally:
            self.__closet_lock.release()

    def get_player_by_id(self, userid):
        return self.__players[userid]

    def get_rule_by_gameid(self, gameid):
        for p in self.__products:
            if str(p.get_gameid()) == str(gameid):
                return p.get_rule()
        return None

    def is_player_registered(self, userid):
        if userid in self.__players:
            return True
        # if self.__players[userid].get_token() == token:
        #     return True
        else:
            return False

    def add_product(self, p):
        self.__products.append(p)

    def set_player_limits(self, limits):
        self.__player_limits = limits

    def verify_token(self, token):
        oriSalt = token[InterProtocol.field_salt]
        sig = token[InterProtocol.field_signature]

        h = SHA.new(oriSalt.encode('utf-8'))
        verifier = PKCS1_v1_5.new(self.__rsaKey)
        return verifier.verify(h, base64.b64decode(sig))

    def register_player(self, userid):
        if userid in self.__players:
            return Err.ok, self.__players[userid]
        if len(self.__players) >= self.__player_limits:
            return Err.client_reach_players_limit, "not a token"
        player = Player(userid)
        player.set_token(secrets.token_urlsafe(20))
        self.__players[userid] = player
        return Err.ok, self.__players[userid]

    def create_new_room(self, player, req_json):
        return None

    def process_create_room(self, player, req_json):
        # create room
        err, room = self.create_new_room(player, req_json)
        if err != Err.ok:
            player.response_err_pack(InterProtocol.client_req_cmd_new_room, err)

        else:
            roomObj = {InterProtocol.room_id: room.get_roomid()}
            pack = InterProtocol.create_success_resp_data_pack(InterProtocol.client_req_cmd_new_room,
                                                               InterProtocol.resp_room, roomObj)
            player.response_success_pack(pack)

    def process_player_request(self, player, cmd, req_json):

        if cmd == InterProtocol.client_req_cmd_new_room:
            self.process_create_room(player, req_json)
            return

        if InterProtocol.room_id not in req_json or str(req_json[InterProtocol.room_id]) == "-1" \
                or str(req_json[InterProtocol.room_id]) == "0" \
                or str(req_json[InterProtocol.room_id]).lower() == "null" \
                or str(req_json[InterProtocol.room_id]).lower() == "none":
            Rooms.Lobby.process_player_request(player, cmd, req_json)
        else:
            room_id = req_json[InterProtocol.room_id]
            if cmd == InterProtocol.client_req_cmd_enter_room:
                if InterProtocol.field_roomtoken not in req_json:
                    player.response_err_pack(InterProtocol.client_req_cmd_enter_room, Errors.lack_field, InterProtocol.field_roomtoken)
                    return

                roomtoken = req_json[InterProtocol.field_roomtoken]
                if not self.verify_token(roomtoken):
                    player.response_err_pack(InterProtocol.client_req_cmd_enter_room, Errors.invalid_room_token)
                    return

                # valide room token
                if room_id not in self.__rooms:
                    self.__rooms[room_id] = Room(room_id)
                    if InterProtocol.game_id in req_json:
                        gameid = req_json[InterProtocol.game_id]
                        gRule = self.get_rule_by_gameid(gameid)
                        if not gRule:
                            player.response_err_pack(InterProtocol.client_req_cmd_enter_room, Errors.invalid_gameid)
                        else:
                            self.__rooms[room_id].create_closet(gRule)

                self.__rooms[room_id].process_player_request(player, InterProtocol.client_req_cmd_enter_room, req_json)

            else:
                if room_id not in self.__rooms:
                    player.response_err_pack(cmd, Errors.did_not_call_enter_room)
                else:
                    self.__rooms[room_id].process_player_request(player, cmd, req_json)
