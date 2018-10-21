from Mains import PlayManager, InterProtocol
from GameRounds import GameRound

__game_rounds = []

def process_player_join_game(player, req_json):
    user_id = req_json[InterProtocol.user_id]

    if player.get_game_round():
        player.send_error_message("Already in a game")
    else:
        play_round = get_available_game_round(req_json[InterProtocol.game_id])
        play_round.add_player(player)
        player.send_success_messsage(InterProtocol.client_req_cmd_join_game)
        play_round.test_and_update_current_stage()


def process_player_request(player, req_json):
    if req_json[InterProtocol.sock_req_cmd].lower() == InterProtocol.client_req_cmd_join_game:
        process_player_join_game(player, req_json)


def get_available_game_round(rule_id):
    for r in __game_rounds:
        if r.get_rule().get_rule_id() != rule_id:
            continue
        if r.can_new_player_in():
            return r
    r = GameRound(PlayManager.get_rule_by_id(rule_id))
    __game_rounds.append(r)
    return r
