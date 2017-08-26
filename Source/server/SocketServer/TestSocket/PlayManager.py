import json
import random

import GameRule
import PlayerClient
import Utils
from Actions.CallBank import CallBank
from Actions.PassCall import PassCall
from GameStages.CalScores import CalScores
from GameStages.CallBanker import CallBanker
from GameStages.DealCards import DealCards
from GameStages.GroupPlayers import GroupPlayers
from GameStages.PlayCards import PlayCards
from GameStages.PublishScores import PublishScores
from GameStages.TeamPlayers import TeamPlayers
from GameStages.TellWinner import TellWinner
from GameRound import GameRound

__Players = []
__Waiting_Players = {}
__PlayRules = {}

__game_rounds = []


SERVER_CMD_DEAL_BEGIN = "deal_begin"  # 开始发牌
SERVER_CMD_DEAL_FINISH = "deal_finish"   # 结束发牌

CLIENT_REQ_JOIN_GAME = "join-game" # 开始游戏
CLIENT_REQ_SELECT_ACTION = "sel-act"


def init_play_rules():
    rule_id = "1212"
    rule = GameRule.GameRule(rule_id)
    rule.set_player_min_number(3)
    rule.set_player_max_number(3)
    rule.set_cards_number_not_deal(3)
    cards = ["poker_1_c","poker_1_d", "poker_1_h", "poker_1_s",
             "poker_2_c", "poker_2_d", "poker_2_h", "poker_2_s",
             "poker_3_c", "poker_3_d", "poker_3_h", "poker_3_s",
             "poker_4_c", "poker_4_d", "poker_4_h", "poker_4_s",
             "poker_5_c", "poker_5_d", "poker_5_h", "poker_5_s",
             "poker_6_c", "poker_6_d", "poker_6_h", "poker_6_s",
             "poker_7_c", "poker_7_d", "poker_7_h", "poker_7_s",
             "poker_8_c", "poker_8_d", "poker_8_h", "poker_8_s",
             "poker_9_c", "poker_9_d", "poker_9_h", "poker_9_s",
             "poker_10_c", "poker_10_d", "poker_10_h", "poker_10_s",
             "poker_11_c", "poker_11_d", "poker_11_h", "poker_11_s",
             "poker_12_c", "poker_12_d", "poker_12_h", "poker_12_s",
             "poker_13_c", "poker_13_d", "poker_13_h", "poker_13_s",
             "poker_joker_moon", "poker_joker_sun"]
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

    # rule.set_stages(stages)
    __PlayRules[rule_id] = rule


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
        if j_obj["req"] == CLIENT_REQ_JOIN_GAME.lower():
            process_req_join_game(conn, j_obj)
        if j_obj["req"] == CLIENT_REQ_SELECT_ACTION.lower():
            process_player_select_action(conn, j_obj)
    except Exception as ex:
        print(ex)


def update_round_stage(client_conn):
    player = get_player_client_from_conn(client_conn)
    round = player.get_game_round()
    round.test_and_update_current_stage()


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


def get_available_game_round(rule_id):
    for r in __game_rounds:
        if r.get_rule().get_rule_id() != rule_id:
            continue
        if r.can_new_player_in():
            return r
    r = GameRound(get_rule_by_id(rule_id))
    __game_rounds.append(r)
    return r


def process_player_select_action(conn, j_obj):
    player = get_player_client_from_conn(conn)
    round = player.get_game_round()
    round.process_player_select_action(player, j_obj["act-id"])


# command samples: {"req":"join-game", "rule_id":"1212"}
def process_req_join_game(conn, j_req):
    try:
        rule_id = j_req["rule_id"]
        play_round = get_available_game_round(rule_id)
        play_round.add_player(get_player_client_from_conn(conn))
        update_round_stage(conn)
    except Exception as ex:
        print(ex)

