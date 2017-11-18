import InterProtocol
from GameRounds.GameRound import GameRound


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

    def is_player_in(self, player):
        return player in self.__players

    def get_seated_player_count(self):
        return len(self.__seated_players)

    def can_new_player_seated(self):
        return len(self.__seated_players) < self.__max_seated_players

    def can_new_player_lookon(self):
        return len(self.__lookon_players) < self.__max_lookon_players

    def add_seated_player(self, player):
        if self.can_new_player_seated():
            self.__players.append(player)
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
        if req_json[InterProtocol.SOCK_REQ_CMD].lower() == InterProtocol.client_req_join_game:
            self.process_join_game(player)

    def process_join_game(self, player):
        try:
            if not self.can_new_player_seated():
                player.send_error_message(InterProtocol.client_req_join_game, "Room is full")
                return
            if self.is_player_in(player):
                player.send_error_message(InterProtocol.client_req_join_game, "Already in room")
                return
            self.add_seated_player(player)
            player.send_success_message(InterProtocol.client_req_join_game)
            self.test_update_room_state()
        except Exception as ex:
            print(ex)

    def test_update_room_state(self):
        if self.get_seated_player_count() >= self.__min_seated_players:
            game_round = GameRound(self.__game_rule)
            for p in self.__seated_players:
                game_round.add_player(p)
            self.__current_round = game_round
        if self.__current_round:
            self.__current_round.test_and_update_current_stage()

        if not game_round.get_is_game_end():
            return

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
