from Rooms.Closet import Closet
import Errors
import secrets
import InterProtocol
import Rooms.Lobby

from Player import Player

class Client:
    def __init__(self, name, clientid, token):
        self.__name = name
        self.__clientid = clientid
        self.__token = token
        self.__products = []
        
        self.__closets = {}  #{gameid:[]}
        self.__player_limits = 0   #all products share a same player limits
        self.__expire_date = None
        self.__players = {}  #{userid:player}

    def get_clientid(self):
        return self.__clientid

    def get_available_closet(self, gameid):
        if gameid not in self.__closets:
            self.__closets[gameid] = []

        for c in self.__closets[gameid]:
            if c.is_accept_new_player():
                return c

        rule = self.get_rule_by_gameid(gameid)
        self.__closets[gameid].append(Closet(rule, gameid))

    def get_player_by_id(self, userid):
        return self.__players[userid]

    def get_rule_by_gameid(self, gameid):
        for p in self.__products:
            if p.get_gameid() == gameid:
                return p.get_rule()
        return None

    def is_player_registered(self, userid, token):
        if userid not in self.__players:
            return False
        if self.__players[userid].get_token() == token:
            return True
        else:
            return False

    def register_player(self, userid):
        if userid in self.__players:
            return  Errors.ok, self.__players[userid]
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

    def process_player_request(self, player, cmd, req_json):

        if cmd == InterProtocol.client_req_cmd_new_room:
            self.process_create_room(player, req_json)

        roomid = str(req_json[InterProtocol.room_id])
        if not roomid or roomid == "-1" or roomid == "0" or roomid.lower() == "null" or roomid.lower() == "none":
            Rooms.Lobby.process_player_request(player, req_json)
        # # cmd = req_json[InterProtocol.sock_req_cmd]
        # user_id = req_json[InterProtocol.user_id]
        # if user_id not in Players:
        #     player = PlayerClient(conn, user_id)
        #     Players[user_id] = player
        #     Log.write_info("new player:" + str(user_id))
        #     Conn_Players[conn] = player
        #     Log.write_info("client number:" + str(len(Conn_Players)))
        # else:
        #     player = Players[user_id]
        #     if player.get_socket_conn() != conn:
        #         if player.get_is_online():
        #             send_err_pack_to_client(conn, cmd, Errors.player_already_in_game)
        #             return
        #         else:
        #             player.update_connection(conn)
        #             return
        # if player:
        #     player.update_last_alive()
        #
        # roomid = str(req_json[InterProtocol.room_id])
        # if not roomid or roomid == "-1" or roomid == "0" or roomid.lower() == "null" or roomid.lower() == "none":
        #     Lobby.process_player_request(player, req_json)
        # else:
        #     room, err = get_room(cmd, roomid, req_json[InterProtocol.game_id])
        #     if not room:
        #         send_err_pack_to_client(conn, cmd, err)
        #     else:
        #         room.process_player_cmd_request(player, req_json)
        #
        # pass




