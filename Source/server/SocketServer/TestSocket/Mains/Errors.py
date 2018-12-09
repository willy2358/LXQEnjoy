
ok = 0
unknown_error = 1
invalid_client_token = 10
client_reach_players_limit = 11
wrong_room_number = 111
invalid_packet_format = 112
invalid_request_parameter = 113
player_already_in_game = 114
did_not_call_enter_room = 115
player_already_in_room = 116
room_is_full = 117
room_no_empty_seat = 118
player_not_in_room = 119
player_not_in_game = 120
invalid_seat_id = 121
seat_id_occupied = 122
invalid_player_clientid = 123
player_not_registered = 124
player_not_join_game = 125
player_not_pending_cmd = 126
invalid_cmd = 127
invalid_cmd_param = 128





Errors = {
    ok: "OK",
    unknown_error: "unknown error",
    wrong_room_number : "wrong room number",
    invalid_client_token: "invalid clientid or token",
    client_reach_players_limit: "reached the limits of players",
    invalid_packet_format: "invalid json format request packet",
    invalid_request_parameter: "invalid request parameters",
    player_already_in_game: "player is already in game",
    did_not_call_enter_room: "Player is not in room, should call enter-room to enter room firstly",
    player_already_in_room: "already in room",
    room_is_full: "room is full, no more play can be accepted",
    room_no_empty_seat:"no more empty seat",
    player_not_in_game: "player is not in game",
    player_not_in_room: "player is not in room",
    invalid_seat_id: "invalid seat id",
    seat_id_occupied : "seat has been occupied by other player",
    invalid_player_clientid: "Invalid clientid, please purchase service",
    player_not_registered:"Not registered player, should be registered by authorized organization",
    player_not_join_game: "Not in game, should join game at first",
    player_not_pending_cmd: "Illegal player, should not send cmd when not been asked for",
    invalid_cmd: "Invalid cmd",
    invalid_cmd_param:"Invalid cmd arguments"
}