
import InterProtocol
# import PlayManager
# from GameRounds import GameRound

from Rooms.Closet import Closet
from Clients import Clients
from Errors import *


# __game_rounds = []


def process_player_join_game(player, req_json):
    user_id = req_json[InterProtocol.user_id]

    if player.get_my_closet():
        player.send_error_message("Already in a game")
    else:

        closet = get_available_closet(req_json[InterProtocol.client_id], req_json[InterProtocol.game_id])
        closet.add_player(player)
        # player.send_success_messsage(InterProtocol.client_req_cmd_join_game)
        # closet.start_game()

def process_player_request(player, cmd, req_json):
    if cmd == InterProtocol.client_req_cmd_join_game:
        process_player_join_game(player, req_json)
    else:
        closet = player.get_closet()
        if closet:
            closet.process_player_request(player, cmd, req_json)
        else:
            player.response_err_pack(cmd, Errors.player_not_join_game)


# def get_available_game_round(rule_id):
#     for r in __game_rounds:
#         if r.get_rule().get_rule_id() != rule_id:
#             continue
#         if r.can_new_player_in():
#             return r
#     r = GameRound(PlayManager.get_rule_by_id(rule_id))
#     __game_rounds.append(r)
#     return r

def get_available_closet(clientid, gameid):
    c = Clients.get_client(clientid)
    if c:
        return c.get_available_closet(gameid)

    return None