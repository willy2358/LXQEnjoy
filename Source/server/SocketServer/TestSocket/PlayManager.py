import json

import CardsMaster
import Log
import PlayerClient
from Actions.CallBank import CallBank
from Actions.PassCall import PassCall
from GameRound import GameRound
from GameRules.MajiangGameRule import MajiangGameRule
from GameRules.PokerGameRule import PokerGameRule
from GameStages.CalScores import CalScores
from GameStages.CallBanker import CallBanker
from GameStages.DealCards import DealCards
from GameStages.RandomBanker import RandomBanker
from GameStages.GroupPlayers import GroupPlayers
from GameStages.PlayCards import PlayCards
from GameStages.PublishScores import PublishScores
from GameStages.TeamPlayers import TeamPlayers
from GameStages.TellWinner import TellWinner
from Rooms import Room_Majiang
import InterProtocol
from Rooms import Lobby

__Players = []
Players={}   #{userid:player}
Rooms = {}   #{roomid:room}
GameRules = {} #{ruleid:rule}
__Waiting_Players = {}
__PlayRules = {}

__game_rounds = []


SERVER_CMD_DEAL_BEGIN = "deal_begin"  # 开始发牌
SERVER_CMD_DEAL_FINISH = "deal_finish"   # 结束发牌

CLIENT_REQ_SELECT_ACTION = "sel-act"


# dou di zu
def init_poker_rule_doudizu():
    rule_id = "1212"
    rule = PokerGameRule(rule_id)
    rule.set_player_min_number(3)
    rule.set_player_max_number(3)
    rule.set_cards_number_not_deal(3)
    cards = CardsMaster.Pokers
    rule.set_cards(cards)

    stage = GroupPlayers(rule)
    rule.add_game_stage(stage)

    stage = DealCards(rule)
    rule.add_game_stage(stage)

    stage = CallBanker(rule)
    rule.add_game_stage(stage)
    set_call_banker_action_options(stage)

    stage = TeamPlayers(rule)
    rule.add_game_stage(stage)

    stage = PlayCards(rule)
    rule.add_game_stage(stage)

    stage = TellWinner(rule)
    rule.add_game_stage(stage)

    stage = CalScores(rule)
    rule.add_game_stage(stage)

    stage = PublishScores(rule)
    rule.add_game_stage(stage)

    #__PlayRules[rule_id] = rule
    GameRules[rule_id] = rule

#da tong guai san jiao
def init_majiang_rule_guaisanjiao():
    rule_id = "m1"
    rule = MajiangGameRule(rule_id)
    rule.set_player_min_number(3)
    rule.set_player_max_number(4)
    rule.set_cards(CardsMaster.MaJiang_Wan + CardsMaster.MaJiang_Suo + CardsMaster.MaJiang_Tong)

    stage = RandomBanker(rule)
    rule.add_game_stage(stage)

    GameRules[rule_id] = rule

def init_play_rules():
    #init_poker_rule_doudizu()
    try:
        init_majiang_rule_guaisanjiao()
    except Exception as ex:
        print(ex)


def set_call_banker_action_options(call_banker_stage):
    call_bank = CallBank("Call", "1")

    call_banker_stage.add_player_action(call_bank)

    c11 = call_bank.add_follow_up_action(CallBank("Rob", "1-1"))
    c111 = c11.add_follow_up_action(CallBank("Rob", "1-1-1"))
    c112 = c11.add_follow_up_action(PassCall("Not Rob", "1-1-2"), True)

    c12 = call_bank.add_follow_up_action(PassCall("Not Rob", "1-2"), True)
    c121 = c12.add_follow_up_action(CallBank("Rob", "1-2-1"))
    c122 = c12.add_follow_up_action(PassCall("Not Rob", "1-2-2"), True)

    not_call = PassCall("Not Call", "2")
    call_banker_stage.add_player_action(not_call, True)

    c21 = not_call.add_follow_up_action(CallBank("Call", "2-1"))
    c211 = c21.add_follow_up_action(CallBank("Rob", "2-1-1"))
    c212 = c21.add_follow_up_action(PassCall("Not Rob", "2-1-2"), True)

    c22 = not_call.add_follow_up_action(PassCall("Not Call", "2-2"), True)
    c221 = c22.add_follow_up_action(CallBank("Call", "2-2-1"))
    c222 = c22.add_follow_up_action(PassCall("Not Call", "2-2-2"), True)


def add_player_client(conn):
    player = PlayerClient.PlayerClient(conn)
    __Players.append(player)
    print('player clients:' + str(len(__Players)))
    print('new player:' + str(conn))


def dispatch_player_commands(conn, comm_text):
    try:
        j_obj = json.loads(comm_text)
        # if j_obj["req"] == CLIENT_REQ_JOIN_GAME.lower():
        #     process_req_join_game(conn, j_obj)
        # if j_obj["req"] == CLIENT_REQ_SELECT_ACTION.lower():
        #     process_player_select_action(conn, j_obj)
        if j_obj[InterProtocol.CMD_TYPE].lower() == InterProtocol.SOCK_REQ_CMD.lower():
            process_client_request(conn, j_obj)
    except Exception as ex:
        print(ex)


def process_client_request(conn, req_json):
    try:
        player = None
        user_id = req_json[InterProtocol.USER_ID]
        if user_id not in Players:
            player = PlayerClient(conn, user_id)
            Players[user_id] = player
        else:
            player = Players[user_id]

        if req_json[InterProtocol.ROOM_ID] > InterProtocol.min_room_id:
            if req_json[InterProtocol.SOCK_REQ_CMD].lower() == InterProtocol.CLIENT_REQ_JOIN_GAME \
                    and req_json[InterProtocol.ROOM_ID] not in Rooms:
                create_room_from_db(req_json[InterProtocol.ROOM_ID], req_json[InterProtocol.GAME_ID])

            if req_json[InterProtocol.ROOM_ID] in Rooms:
                Rooms[req_json[InterProtocol.ROOM_ID]].process_player_cmd_request(player, req_json)
        else:
            #process_lobby_player_request(player, req_json)
            Lobby.process_player_request(player, req_json)

    except Exception as ex:
        print(ex)

# def update_round_stage(client_conn):
#     player = get_player_client_from_conn(client_conn)
#     round = player.get_game_round()
#     round.test_and_update_current_stage()


def get_player_client_from_conn(conn):
    for c in __Players:
        if c.get_socket_conn() == conn:
            return c

    return None


def get_rule_by_id(rule_id):
    if rule_id in __PlayRules:
        return __PlayRules[rule_id]
    else:
        return None

#
# def get_available_game_round(rule_id):
#     for r in __game_rounds:
#         if r.get_rule().get_rule_id() != rule_id:
#             continue
#         if r.can_new_player_in():
#             return r
#     r = GameRound(get_rule_by_id(rule_id))
#     __game_rounds.append(r)
#     return r


def process_player_select_action(conn, j_obj):
    player = get_player_client_from_conn(conn)
    round = player.get_game_round()
    act_param = None
    if "act-params" in j_obj:
        act_param = j_obj["act-params"]
    round.process_player_select_action(player, j_obj["act-id"], act_param)

#
# def process_lobby_player_request(conn, req_json):
#     if req_json[InterProtocol.SOCK_REQ_CMD].lower() == InterProtocol.CLIENT_REQ_JOIN_GAME:
#         process_join_lobby_game(conn, req_json)
#
#
# def process_join_lobby_game(player, req_json):
#     user_id = req_json[InterProtocol.USER_ID]
#
#     if player.get_game_round():
#             player.send_error_message("Already in a game")
#     else:
#         play_round = get_available_game_round(req_json[InterProtocol.GAME_ID])
#         play_round.add_player(player)
#         player.send_success_messsage(InterProtocol.CLIENT_REQ_JOIN_GAME)
#         play_round.test_and_update_current_stage()


# TODO create Room from database
def create_room_from_db(room_id, rule_id):
    game_rule = GameRules[rule_id]
    if isinstance(game_rule, MajiangGameRule):
        room = Room_Majiang(room_id, game_rule)

    room.set_min_seated_player_num(3)
    room.set_max_seated_player_num(3)
    Rooms[room_id] = room

