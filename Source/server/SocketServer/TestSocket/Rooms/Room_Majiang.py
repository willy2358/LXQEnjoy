from Rooms.Room import Room


class Room_Majiang(Room):
    def __init__(self, room_id, game_rule):
        super(Room_Majiang, self).__init__(room_id, game_rule)

    def begin_next_game_round(self):
        pass

    def close_room(self):
        pass

    def process_player_cmd_request(self, player, req_json):
        super(Room_Majiang, self).process_player_cmd_request(player, req_json)
