from Rooms.Room import Room

from GameRounds.GameRound_Majiang import GameRound_Majiang

class Room_Majiang(Room):
    def __init__(self, room_id, game_rule):
        super(Room_Majiang, self).__init__(room_id, game_rule)

    def begin_next_game_round(self):
        pass

    def close_room(self):
        super(Room_Majiang, self).close_room()

    def process_player_cmd_request(self, player, req_json):
        super(Room_Majiang, self).process_player_cmd_request(player, req_json)

    def begin_next_game_round(self):

        game_round = GameRound_Majiang(self._game_rule)
        game_round.set_my_room(self)
        game_round.set_round_end_callback(self.test_continue_next_round)
        for p in self._seated_players:
            p.reset_for_next_round()
            game_round.add_player(p)

        if len(self._last_winners) > 0:
            game_round.set_bank_player(self._last_winners[0])

        self._current_round = game_round
        self._current_round_order += 1
        self._current_round.begin_run()