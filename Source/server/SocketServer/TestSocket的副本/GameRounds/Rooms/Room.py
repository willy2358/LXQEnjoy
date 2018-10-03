import threading

import InterProtocol
from GameRounds.GameRound_Majiang import GameRound_Majiang


class Room:
    def __init__(self, room_id, game_rule):
        self._room_id = room_id
        self._game_rule = game_rule
        self._seated_players = []
        self._lookon_players = []
        self._max_seated_players = 0
        self._min_seated_players = 0
        self._max_lookon_players = 0
        self._round_num = 2
        self._current_round_order = 0
        self._current_round = None
        self._last_winners = []
        self._players_total_score = {}
        self._lock_join_game = threading.Lock()

    def is_player_in(self, player):
        return player in self._seated_players

    def get_seated_player_count(self):
        return len(self._seated_players)

    def get_seated_players(self):
        return self._seated_players

    def get_last_winners(self):
        return self._last_winners

    def get_player_total_score(self, player):
        if player in self._players_total_score:
            return self._players_total_score[player]
        else:
            return 0

    def can_new_player_seated(self):
        return len(self._seated_players) < self._max_seated_players

    def can_new_player_lookon(self):
        return len(self._lookon_players) < self._max_lookon_players

    def add_seated_player(self, player):
        if self.can_new_player_seated():
            self._seated_players.append(player)
            player.set_my_room(self)
            return True
        else:
            return False
    def remove_player(self, player):
        if player in self._seated_players:
            self._seated_players.remove(player)
        if player in self._lookon_players:
            self._lookon_players.remove(player)
        
    def add_lookon_player(self, player):
        if self.can_new_player_lookon():
            self._lookon_players.append(player)
            return True
        else:
            return False

    def set_last_winners(self, winners):
        self._last_winners = winners

    def process_player_cmd_request(self, player, req_json):
        req_cmd = req_json[InterProtocol.sock_req_cmd].lower()
        if req_cmd == InterProtocol.client_req_cmd_join_game:
            self.process_join_game(player)
        elif req_cmd == InterProtocol.client_req_type_exe_cmd:
            if InterProtocol.client_req_exe_cmd not in req_json:
                err = InterProtocol.create_request_error_packet(req_cmd)
                player.send_server_cmd_packet(err)
            elif self._current_round:
                cmd = req_json[InterProtocol.client_req_exe_cmd]
                const_param = InterProtocol.client_req_cmd_param
                cmd_param = req_json[const_param] if const_param in req_json else None
                self._current_round.process_player_execute_command(player, cmd, cmd_param)
        elif req_cmd == InterProtocol.client_req_robot_play:
            flag = str(req_json[InterProtocol.client_req_robot_play])
            if flag.lower().startswith('y'):
                self._current_round.process_player_robot_play_request(player, True)
            elif flag.lower().startswith('n'):
                self._current_round.process_player_robot_play_request(player, False)
            else:
                err = InterProtocol.create_request_error_packet(req_cmd)
                player.send_server_cmd_packet(err)

    def process_join_game(self, player):
        try:
            if self._lock_join_game.acquire(5): # timeout 5 seconds
                cmd = InterProtocol.client_req_cmd_join_game
                # if self.is_player_in(player):
                #     #player.send_error_message(InterProtocol.client_req_type_join_game, "Already in room")
                #     player.send_success_message(InterProtocol.client_req_cmd_join_game);
                #     #player.send_cards_state();
                #     return
                if not self.can_new_player_seated():
                    err_resp = InterProtocol.create_error_pack(cmd, )
                    player.send_error_message(InterProtocol.client_req_cmd_join_game, "Room is full")
                    return
                self.add_seated_player(player)
                player.send_success_message(InterProtocol.client_req_cmd_join_game)
                self.publish_seated_players()

                if self.get_seated_player_count() >= self._min_seated_players:
                    # game_round = GameRound_Majiang(self._game_rule)
                    # game_round.set_my_room(self)
                    # game_round.set_round_end_callback(self.test_continue_next_round)
                    # for p in self._seated_players:
                    #     game_round.add_player(p)
                    # self._current_round = game_round
                    # game_round.begin_run()
                    self.test_continue_next_round()

        except Exception as ex:
            print(ex)
        finally:
            self._lock_join_game.release()

    def publish_seated_players(self):
        players = []
        for i in range(0, len(self._seated_players)):
            player = self._seated_players[i]
            players.append({'userid':player.get_user_id()})

        pack = InterProtocol.create_game_players_packet(players)
        for p in self._seated_players:
            p.send_server_cmd_packet(pack)

    def test_continue_next_round(self):
        if self._current_round_order < self._round_num:
            self.begin_next_game_round()
        else:
            self.close_room()

    def update_player_total_score(self, player):
        if player not in self._players_total_score:
            self._players_total_score[player] = player.get_won_score()
        else:
            self._players_total_score[player] += player.get_won_score()


    def begin_next_game_round(self):
        pass
        # game_round = GameRound_Majiang(self.__game_rule)
        # game_round.set_my_room(self)
        # game_round.set_round_end_callback(self.test_continue_next_round)
        # for p in self._seated_players:
        #     game_round.add_player(p)
        # self._current_round = game_round
        # self._current_round_order += 1

    def close_room(self):
        packet = InterProtocol.create_game_status_packet("Room will be closed")
        if self._current_round:
            self._current_round.publish_round_states(packet)

    def set_max_seated_player_num(self, max_number):
        self._max_seated_players = max_number

    def set_min_seated_player_num(self, min_number):
        self._min_seated_players = min_number

    def set_max_lookon_player_num(self, max_number):
        self._max_lookon_players = max_number

    def set_round_number(self, number):
        self._round_num = number
