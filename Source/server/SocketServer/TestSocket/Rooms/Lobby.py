from Mains import InterProtocol
# import PlayManager
# from GameRounds import GameRound
import threading

from Clients import Clients
from Mains.Errors import *
from Mains import Log


# __game_rounds = []

_lock_seated_players = threading.Lock()

def process_player_join_game(player, req_json):
    user_id = req_json[InterProtocol.user_id]

    if player.get_closet():
        player.response_err_pack(InterProtocol.client_req_cmd_join_game, Errors.player_already_in_game)
    else:
        #ToDo need to think carefully about the lock and error message, and pich another closet if possible
        closet = get_available_closet(req_json[InterProtocol.client_id], req_json[InterProtocol.game_id])
        if closet:
            try:
                if _lock_seated_players.acquire(5):
                    if closet.add_player(player):
                        player.set_seatid(len(closet.get_scene_players()))
                        pack = InterProtocol.create_success_resp_pack(InterProtocol.client_req_cmd_join_game)
                        player.response_success_pack(pack)
                        closet.publish_players_status()

                        closet.test_to_start_game()
            except Exception as ex:
                Log.exception(ex)
            finally:
                _lock_seated_players.release()



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