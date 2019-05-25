import threading

from Mains.PlayScene import PlayScene
from Mains import Log, InterProtocol, Errors
import Mains.Errors as Errors

#ToDo need to support next round,  created: 20190525

#最小的游戏空间，入坐即进入空间，没有旁观玩家
class Closet:
    def __init__(self, gRule, closetId = None):
        self.__gRule = gRule
        # self.__roomId = roomId
        self.__playScene = PlayScene(gRule)
        self._lock_seated_players = threading.Lock()
        self.__closetId = closetId

        self.__seated_players = []
        self._max_seated_players = 0
        self._min_seated_players = 0

        self._round_num = 12
        self._current_round_order = 0
        self._current_round = None
        self._fee_stuff_id = 0
        self._fee_stuff_name = ""
        self._stake_stuff_id = 0
        self._stake_stuff_name = ""
        self._last_winners = []
        self._players_total_score = {}

    def get_rule(self):
        return self.__gRule

    def get_closetId(self):
        return self.__closetId

    def get_scene(self):
        return self.__playScene

    def get_players(self):
        return self.__playScene.get_players()

    def get_player_acc_score(self, player):
        pass

    def is_player_in(self, player):
        return self.__playScene.is_player_in(player)

    def is_accept_new_player(self):
        return self.__playScene.has_vacancy()

    def is_seatid_valid(self, seatid):
        seatids = self.__gRule.get_seats_ids()
        # if seatids is None or len(seatids) < 2: #at least two players
        #     return True

        return seatid in seatids

    def is_seatid_has_been_occupied(self, seatid):
        if seatid < 1:
            return False

        for p in self.__seated_players:
            if p.get_seatid() == seatid:
                return True

        return False

    def remove_player(self, player):
        if self.__playScene.remove_player(player):
            self.__seated_players.remove(player)
            self.publish_players_status()

    def process_player_request(self, player, cmd, req_json):

        if cmd == InterProtocol.client_req_cmd_join_game:
            self.process_join_game(player, req_json)
        elif cmd == InterProtocol.client_req_cmd_leave_game:
            self.process_player_leave_game(player)
        elif cmd == InterProtocol.client_req_type_exe_cmd:
            cmdTxt = req_json[InterProtocol.client_req_exe_cmd]
            cmdArgs = req_json[InterProtocol.client_req_cmd_param]
            self.__playScene.process_player_exed_cmd(player, cmdTxt, cmdArgs)
            self.__playScene.go_progress()
        elif cmd == InterProtocol.client_req_get_cards:
            pack = InterProtocol.create_player_cards_data_pack(player)
            player.send_server_cmd_packet(pack)

        elif cmd == InterProtocol.client_req_robot_play:
            flag = str(req_json[InterProtocol.client_req_robot_play])
            if flag.lower().startswith('y'):
                player.set_is_robot_play(True)
            elif flag.lower().startswith('n'):
                player.set_is_robot_play(False)

            pack = InterProtocol.create_success_resp_pack(cmd)
            player.send_server_cmd_packet(pack)

    def process_join_game(self, player, req_json):
        cmd = InterProtocol.client_req_cmd_join_game
        if InterProtocol.field_seatid not in req_json:
            player.send_server_cmd_packet(
                InterProtocol.create_error_pack(cmd, Errors.lack_field, InterProtocol.field_seatid))
            return
    #
        seatid = req_json[InterProtocol.seat_id]
        if not self.is_seatid_valid(seatid):
            resp_pack = InterProtocol.create_error_pack(cmd, Errors.invalid_seat_id)
            player.send_server_cmd_packet(resp_pack)
        elif player in self.__seated_players:
            resp_pack = InterProtocol.create_error_pack(cmd, Errors.player_already_in_game)
            player.send_server_cmd_packet(resp_pack)
        elif self.is_seatid_has_been_occupied(seatid):
            resp_pack = InterProtocol.create_error_pack(cmd, Errors.seat_id_occupied)
            player.send_server_cmd_packet(resp_pack)
        else:
            ret, errCode = self.add_seated_player(player, seatid)
            if not ret:
                resp_pack = InterProtocol.create_error_pack(cmd, errCode)
                player.send_server_cmd_packet(resp_pack)
            else:
                player.set_closet(self)
                player.set_seatid(seatid)

                resp_pack = InterProtocol.create_success_resp_pack(cmd)
                player.send_server_cmd_packet(resp_pack)

                self.publish_players_status()
                self.test_to_start_game()

    def process_player_leave_game(self, player):
        cmd = InterProtocol.client_req_cmd_leave_game
        resp_pack = None
        if player in self._seated_players:
            self.remove_player(player)
            resp_pack = InterProtocol.create_success_resp_pack(cmd)
        else:
            resp_pack = InterProtocol.create_error_pack(cmd, Errors.player_not_in_game)

        player.send_server_cmd_packet(resp_pack)

    def add_seated_player(self, player, seatid):
        try:
            if self._lock_seated_players.acquire(5):
                if self.is_accept_new_player() and not self.is_seatid_has_been_occupied(seatid):
                    self.__seated_players.append(player)
                    player.set_seatid(seatid)
                    self.__playScene.add_player(player)
                    return True, Errors.ok
                else:
                    return False, Errors.room_no_empty_seat
        except Exception as ex:
            Log.exception(ex)
            return False, Errors.unknown_error
        finally:
            self._lock_seated_players.release()

    def get_players_status(self):
        players = []
        for p in self.__playScene.get_players():
            players.append({'userid': p.get_userid(), 'seatid': p.get_seatid()})

        return players

    def test_continue_next_round(self):
        if self._current_round_order < self._round_num:
            self.is_accept_new_player()
        else:
            self.close_room()

    def test_to_start_game(self):
        # reached the min players,  start game.
        if len(self.__playScene.get_players()) >= self.__gRule.get_min_players_capacity():
            self.__playScene.start_game()

    def publish_players_status(self):
        players = self.get_players_status()

        pack = InterProtocol.create_game_players_packet(players)
        for p in self.get_players():
            p.send_server_cmd_packet(pack)

    def close_closet(self):
        packet = InterProtocol.create_game_status_packet("Room will be closed")
        if self._current_round:
            self._current_round.publish_round_states(packet)





