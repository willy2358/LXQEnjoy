import threading

from Mains import Log, InterProtocol, Errors

from Rooms.Closet import Closet

class Room:
    def __init__(self, roomId):

        self.__room_id = roomId
        self.__all_players = []

        self.__player_num_limit = 30

        self._lock_seated_players = threading.Lock()
        self._lock_all_players = threading.Lock()


        self.__closets = []
        self.__closet_limts = 10


    def get_room_id(self):
        return self.__room_id

    def get_closet(self, closetid):
        sid = str(closetid)
        for c in self.__closets:
            if str(c.get_closetId()) == sid:
                return c

        return None

    def get_all_players(self):
        return self.__all_players

    def is_player_in(self, player):
        return  player in self.__all_players

    def is_accept_new_player(self):
        return len(self.__all_players) < self.__player_num_limit

    def create_closet(self, gRule):
        closet = Closet(gRule, len(self.__closets) + 1)
        self.__closets.append(closet)

    def add_new_enter_player(self, player):
        try:
            if self._lock_all_players.acquire(5):
                if self.is_accept_new_player():
                    self.__all_players.append(player)
                    return True, Errors.ok
                else:
                    return False, Errors.room_is_full
        except Exception as ex:
            Log.exception(ex)
            return False, Errors.unknown_error
        finally:
            self._lock_all_players.release()

    def remove_player(self, player):
        try:
            if self._lock_all_players.acquire(5):
                if self.is_player_in(player):
                    self.__all_players.remove(player)
                    return True, Errors.ok
                else:
                    return False, Errors.player_not_in_room
        except Exception as ex:
            Log.exception(ex)
            return False, Errors.unknown_error
        finally:
            self._lock_all_players.release()

    def process_player_request(self, player, cmd, req_json):
        req_cmd = cmd.lower()
        if req_cmd == InterProtocol.client_req_cmd_enter_room:
            self.process_player_enter_room(player)
        elif req_cmd == InterProtocol.client_req_cmd_new_closet:
            self.process_player_create_closet(player, req_json)
        elif req_cmd == InterProtocol.client_req_cmd_leave_room:
            self.process_player_leave_room(player)
        elif req_cmd == InterProtocol.client_req_cmd_join_game \
                or req_cmd == InterProtocol.client_req_cmd_leave_game \
                or req_cmd == InterProtocol.client_req_type_exe_cmd \
                or req_cmd == InterProtocol.client_req_play_cards \
                or req_cmd == InterProtocol.client_req_robot_play:
            self.process_closet_request(player, req_cmd, req_json)

    def process_player_leave_room(self, player):
        cmd = InterProtocol.client_req_cmd_leave_room
        resp_pack = None
        if self.is_player_in(player):
            ret, err = self.remove_player(player)
            if ret:
                player.set_room(None)
                player.set_closet(None)
                resp_pack = InterProtocol.create_success_resp_pack(cmd)
            else:
                resp_pack = InterProtocol.create_error_pack(cmd, err)
        else:
            resp_pack = InterProtocol.create_error_pack(cmd, Errors.player_not_in_room)

        player.send_server_cmd_packet(resp_pack)

    def process_player_enter_room(self, player):
        cmd = InterProtocol.client_req_cmd_enter_room
        if self.is_player_in(player):
            resp_pack = InterProtocol.create_error_pack(cmd, Errors.player_already_in_room)
            player.send_server_cmd_packet(resp_pack)
        elif not self.is_accept_new_player():
            resp_pack = InterProtocol.create_error_pack(cmd, Errors.room_is_full)
            player.send_server_cmd_packet(resp_pack)
        else:
            ret, err = self.add_new_enter_player(player)
            resp_pack = None
            if ret:
                player.set_room(self)

                roomObj = {
                    InterProtocol.room_id : self.__room_id,
                    InterProtocol.resp_players: self.get_players_status(),
                    InterProtocol.field_closets: self.get_closets_status()
                }
                resp_pack = InterProtocol.create_success_resp_data_pack(cmd, InterProtocol.resp_room, roomObj)
            else:
                resp_pack = InterProtocol.create_error_pack(cmd, err)
            player.send_server_cmd_packet(resp_pack)

            if ret:
                self.publish_players_status()

    def process_player_create_closet(self, player, req_json):
        pass

    def process_closet_request(self, player, cmd, req_json):
        cmd = InterProtocol.client_req_cmd_join_game

        if InterProtocol.field_closetid not in req_json:
            player.send_server_cmd_packet(InterProtocol.create_error_pack(cmd, Errors.lack_field, InterProtocol.field_closetid))

        closetid = req_json[InterProtocol.field_closetid]
        closet = self.get_closet(closetid)
        if not closet:
            resp_pack = InterProtocol.create_error_pack(cmd, Errors.invalid_closetid)
            player.send_server_cmd_packet(resp_pack)

        closet.process_player_request(player, cmd, req_json)


    def get_players_status(self):
        players = []
        for p in self.__all_players:
            info = {
                InterProtocol.user_id: p.get_userid(),
            }
            players.append(info)

        return players

    def get_closets_status(self):
        infos = []
        for c in self.__closets:
            info = {
                InterProtocol.field_gameid: c.get_rule().get_ruleid(),
                InterProtocol.field_closetid: c.get_closetId(),
                InterProtocol.field_players: c.get_players_status()
            }
            infos.append(info)
        return infos

    def publish_players_status(self):
        players = self.get_players_status()

        pack = InterProtocol.create_game_players_packet(players)
        for p in self.__all_players:
            p.send_server_cmd_packet(pack)


    def update_player_total_score(self, player):
        if player not in self._players_total_score:
            self._players_total_score[player] = player.get_won_score()
        else:
            self._players_total_score[player] += player.get_won_score()

    def close_room(self):
        packet = InterProtocol.create_game_status_packet("Room will be closed")
        if self._current_round:
            self._current_round.publish_round_states(packet)

