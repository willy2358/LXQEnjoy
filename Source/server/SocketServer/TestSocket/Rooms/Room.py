import threading

import InterProtocol
from GameRounds.GameRound_Majiang import GameRound_Majiang


class Room:
    def __init__(self, room_id, game_rule):
        self.__room_id = room_id
        self.__game_rule = game_rule
        self.__seated_players = []
        self.__lookon_players = []
        self.__max_seated_players = 0
        self.__min_seated_players = 0
        self.__max_lookon_players = 0
        self.__round_num = 8
        self.__current_round_order = 0
        self.__current_round = None
        self.__last_winners = []
        self._lock_join_game = threading.Lock()

    def is_player_in(self, player):
        return player in self.__seated_players

    def get_seated_player_count(self):
        return len(self.__seated_players)

    def can_new_player_seated(self):
        return len(self.__seated_players) < self.__max_seated_players

    def can_new_player_lookon(self):
        return len(self.__lookon_players) < self.__max_lookon_players

    def add_seated_player(self, player):
        if self.can_new_player_seated():
            self.__seated_players.append(player)
            return True
        else:
            return False
        
    def add_lookon_player(self, player):
        if self.can_new_player_lookon():
            self.__lookon_players.append(player)
            return True
        else:
            return False

    def process_player_cmd_request(self, player, req_json):
        req_cmd = req_json[InterProtocol.sock_req_cmd].lower()
        if req_cmd == InterProtocol.client_req_join_game:
            self.process_join_game(player)

    def process_join_game(self, player):
        try:
            if self._lock_join_game.acquire(5): # timeout 5 seconds
                if not self.can_new_player_seated():
                    player.send_error_message(InterProtocol.client_req_join_game, "Room is full")
                    return
                if self.is_player_in(player):
                    player.send_error_message(InterProtocol.client_req_join_game, "Already in room")
                    return
                self.add_seated_player(player)
                player.send_success_message(InterProtocol.client_req_join_game)

                if self.get_seated_player_count() >= self.__min_seated_players:
                    game_round = GameRound_Majiang(self.__game_rule)
                    game_round.set_round_end_callback(self.test_continue_next_round)
                    for p in self.__seated_players:
                        game_round.add_player(p)
                    self.__current_round = game_round

        except Exception as ex:
            print(ex)
        finally:
            self._lock_join_game.release()

    def test_continue_next_round(self):
        if self.__current_round.get_is_game_end():
            if self.__current_round_order < self.__round_num:
                self.begin_next_game_round()
            else:
                self.close_room()

    def begin_next_game_round(self):
        pass

    def close_room(self):
        pass

    def set_max_seated_player_num(self, max_number):
        self.__max_seated_players = max_number

    def set_min_seated_player_num(self, min_number):
        self.__min_seated_players = min_number

    def set_max_lookon_player_num(self, max_number):
        self.__max_lookon_players = max_number

    def set_round_number(self, number):
        self.__round_num = number
