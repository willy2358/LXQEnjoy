import json

import CardsMaster
import InterProtocol
import Log
from Actions.CallBank import CallBank
from Actions.PassCall import PassCall
from GameRules.GameRule_Majiang import GameRule_Majiang
from GameRules.GameRule_Poker import GameRule_Poker
from GameStages.CalScores_Majiang import CalScores_Majiang
from GameStages.CallBanker import CallBanker
from GameStages.DealCards import DealCards
from GameStages.DealMaJiangs import DealMaJiangs
from GameStages.GroupPlayers import GroupPlayers
from GameStages.PlayCards import PlayCards
from GameStages.PlayMajiang import PlayMajiang
from GameStages.PublishScores import PublishScores
from GameStages.RandomBanker import RandomBanker
from GameStages.TeamPlayers import TeamPlayers
from GameStages.TellWinner import TellWinner
from Rooms import Lobby
from Rooms.Room_Majiang import Room_Majiang
from GameStages.TellWinner_Majiang import TellWinner_Majiang

from threading import Timer
from datetime import datetime,timedelta

from GameStages.CalScores import CalScores

from PlayerClient import PlayerClient

from CardsPattern.PatternModes import PatternModes
from CardsPattern.Mode_AllInRange import Mode_AllInRange
from CardsPattern.Mode_AllPairs import Mode_AllPairs
from CardsPattern.Mode_AnyInRange import Mode_AnyInRange
from CardsPattern.Mode_AnyOutRange import Mode_AnyOutRange
from CardsPattern.Mode_Pair import Mode_Pair
from CardsPattern.Mode_Seq import Mode_Seq
from CardsPattern.Mode_Triple import Mode_Triple

Conn_Players = {} #{connection, player}
# __Players = []
Players={}   #{userid:player}
Rooms = {}   #{roomid:room}
GameRules = {} #{ruleid:rule}
__Waiting_Players = {}
__PlayRules = {}

__game_rounds = []


SERVER_CMD_DEAL_BEGIN = "deal_begin"  # 开始发牌
SERVER_CMD_DEAL_FINISH = "deal_finish"   # 结束发牌

CLIENT_REQ_SELECT_ACTION = "sel-act"

cycle_minutes_check_dead = 10
dead_connect_reserve_minutes = 1
timer_clear_dead_connection = None

# dou di zu
def init_poker_rule_doudizu():
    rule_id = "1212"
    rule = GameRule_Poker(rule_id)
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


# da tong guai san jiao
def init_majiang_rule_guaisanjiao():
    rule_id = "m1"
    rule = GameRule_Majiang(rule_id)
    rule.set_player_min_number(3)
    rule.set_player_max_number(4)
    rule.set_cards(CardsMaster.majiang_wans + CardsMaster.majiang_suos + CardsMaster.majiang_tons)

    stage = RandomBanker(rule)
    rule.add_game_stage(stage)
    stage = DealMaJiangs(rule)
    rule.add_game_stage(stage)
    stage = PlayMajiang(rule)
    rule.add_game_stage(stage)
    stage = TellWinner_Majiang(rule)
    rule.add_game_stage(stage)
    stage = PublishScores(rule)
    rule.add_game_stage(stage)

    rule.ScoreRule.set_base_score(3)
    rule.ScoreRule.set_zimo_score(2)
    rule.ScoreRule.set_ting_kou_count_score(1, 2)
    rule.ScoreRule.set_ting_kou_count_score(2, 1)
    rule.ScoreRule.set_ting_kou_count_score(3, 1)
    rule.ScoreRule.set_ting_kou_count_score(4, 1)
    rule.ScoreRule.set_ting_kou_count_score(5, 1)
    rule.ScoreRule.set_ting_kou_count_score(6, 1)
    rule.ScoreRule.set_ting_kou_count_score(7, 1)
    rule.ScoreRule.set_score_formular("(B + N) * P * W")

    load_majiang_patterns(rule)

    GameRules[rule_id] = rule


def load_majiang_patterns(majiang_rule):

    wan_s = CardsMaster.def_wans["wan-1"]
    suo_s = CardsMaster.def_suos["suo-1"]
    ton_s = CardsMaster.def_tons["ton-1"]

    pat = PatternModes("qing-long", 10)
    pat.add_mode(Mode_Seq(wan_s, 3))
    pat.add_mode(Mode_Seq(wan_s + 3, 3))
    pat.add_mode(Mode_Seq(wan_s + 6, 3))
    pat.add_mode(Mode_AllInRange(wan_s, wan_s + 8))
    majiang_rule.add_win_pattern(pat)

    pat = PatternModes("qing-long", 10)
    pat.add_mode(Mode_Seq(suo_s, 3))
    pat.add_mode(Mode_Seq(suo_s + 3, 3))
    pat.add_mode(Mode_Seq(suo_s + 6, 3))
    pat.add_mode(Mode_AllInRange(suo_s, suo_s + 8))
    majiang_rule.add_win_pattern(pat)

    pat = PatternModes("qing-long", 10)
    pat.add_mode(Mode_Seq(ton_s, 3))
    pat.add_mode(Mode_Seq(ton_s + 3, 3))
    pat.add_mode(Mode_Seq(ton_s + 6, 3))
    pat.add_mode(Mode_AllInRange(ton_s, ton_s + 8))
    majiang_rule.add_win_pattern(pat)
    majiang_rule.ScoreRule.set_pattern_score("qing-long", 10)

    pat = PatternModes("qing-pairs", 10)
    pat.add_mode(Mode_AllPairs())
    pat.add_mode(Mode_AllInRange(wan_s, wan_s + 8))
    majiang_rule.add_win_pattern(pat)

    pat = PatternModes("qing-pairs", 10)
    pat.add_mode(Mode_AllPairs())
    pat.add_mode(Mode_AllInRange(suo_s, suo_s + 8))
    majiang_rule.add_win_pattern(pat)

    pat = PatternModes("qing-pairs", 10)
    pat.add_mode(Mode_AllPairs())
    pat.add_mode(Mode_AllInRange(ton_s, ton_s + 8))
    majiang_rule.add_win_pattern(pat)
    majiang_rule.ScoreRule.set_pattern_score("qing-pairs", 10)

    pat = PatternModes("qing", 5)
    pat.add_mode(Mode_AllInRange(wan_s, wan_s + 8))
    majiang_rule.add_win_pattern(pat)

    pat = PatternModes("qing", 5)
    pat.add_mode(Mode_AllInRange(suo_s, suo_s + 8))
    majiang_rule.add_win_pattern(pat)

    pat = PatternModes("qing", 5)
    pat.add_mode(Mode_AllInRange(ton_s, ton_s + 8))
    majiang_rule.add_win_pattern(pat)
    majiang_rule.ScoreRule.set_pattern_score("qing", 5)

    pat = PatternModes("long", 5)
    pat.add_mode(Mode_Seq(wan_s, 3))
    pat.add_mode(Mode_Seq(wan_s + 3, 3))
    pat.add_mode(Mode_Seq(wan_s + 6, 3))
    pat.add_mode(Mode_AnyOutRange(wan_s, wan_s + 8))

    pat = PatternModes("long", 5)
    pat.add_mode(Mode_Seq(suo_s, 3))
    pat.add_mode(Mode_Seq(suo_s + 3, 3))
    pat.add_mode(Mode_Seq(suo_s + 6, 3))
    pat.add_mode(Mode_AnyOutRange(suo_s, suo_s + 8))
    majiang_rule.add_win_pattern(pat)

    pat = PatternModes("long", 5)
    pat.add_mode(Mode_Seq(ton_s, 3))
    pat.add_mode(Mode_Seq(ton_s + 3, 3))
    pat.add_mode(Mode_Seq(ton_s + 6, 3))
    pat.add_mode(Mode_AnyOutRange(ton_s, suo_s + 8))
    majiang_rule.add_win_pattern(pat)
    majiang_rule.ScoreRule.set_pattern_score("long", 5)

    pat = PatternModes("pairs", 5)
    pat.add_mode(Mode_AllPairs())
    pat.add_mode(Mode_AnyInRange(wan_s, wan_s + 8))
    pat.add_mode(Mode_AnyInRange(ton_s, ton_s + 8))
    majiang_rule.add_win_pattern(pat)

    pat = PatternModes("pairs", 5)
    pat.add_mode(Mode_AllPairs())
    pat.add_mode(Mode_AnyInRange(wan_s, wan_s + 8))
    pat.add_mode(Mode_AnyInRange(suo_s, suo_s + 8))
    majiang_rule.add_win_pattern(pat)

    pat = PatternModes("pairs", 5)
    pat.add_mode(Mode_AllPairs())
    pat.add_mode(Mode_AnyInRange(suo_s, suo_s + 8))
    pat.add_mode(Mode_AnyInRange(ton_s, ton_s + 8))
    majiang_rule.add_win_pattern(pat)
    majiang_rule.ScoreRule.set_pattern_score("pairs", 5)

def initialize():
    init_play_rules()

    start_timer_to_clear_dead_connection()

def start_timer_to_clear_dead_connection():
    timeout = min(cycle_minutes_check_dead, dead_connect_reserve_minutes)
    timer_clear_dead_connection = Timer(timeout * 60, remove_dead_connection)
    timer_clear_dead_connection.start()

def init_play_rules():
    # init_poker_rule_doudizu()
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


def validate_player(j_obj):
    if InterProtocol.user_id not in j_obj \
            or InterProtocol.room_id not in j_obj \
            or InterProtocol.sock_req_cmd not in j_obj:
        return False
    else:
        return True


def dispatch_player_commands(conn, comm_text):

    j_obj = None
    try:
        j_obj = json.loads(comm_text)
    except Exception as ex:
        send_msg_to_client_connection("Invalid request format")
        return

    if not validate_player(j_obj):
        send_msg_to_client_connection("Invalid request parameters")
        return

    try:
        if j_obj[InterProtocol.cmd_type].lower() == InterProtocol.sock_req_cmd.lower():
            process_client_request(conn, j_obj)
    except Exception as ex:
        Log.write_exception(ex)
        print(ex)

def send_msg_to_client_connection(conn, msg):
    try:
        conn.sendall(msg.encode(encoding="utf-8"))
    except Exception as ex:
        Log.write_exception(ex)


def send_welcome_to_new_connection(conn):
    welcome_msg = "welcome,just enjoy!"
    send_msg_to_client_connection(conn, welcome_msg)


def process_client_request(conn, req_json):
    try:
        player = None
        user_id = req_json[InterProtocol.user_id]
        if user_id not in Players:
            player = PlayerClient(conn, user_id)
            Players[user_id] = player
            Log.write_info("new player:" + str(user_id))
            Conn_Players[conn] = player
            Log.write_info("client number:" + str(len(Conn_Players)))
        else:
            player = Players[user_id]
            if player.get_socket_conn() != conn:
                send_msg_to_client_connection("Already in game, try reconnect to refresh connection")
                return
                # if req_json[InterProtocol.player_auth_token] != player.get_session_token():
                #     send_msg_to_client_connection("Wrong player token")
                #     returnß
                # else:
                #player.update_connection(conn)
        if player:
            player.update_last_alive()

        if req_json[InterProtocol.sock_req_cmd].lower() == InterProtocol.client_req_type_reconnect:
            player.update_connection(conn)

        if req_json[InterProtocol.room_id] > InterProtocol.min_room_id:
            if req_json[InterProtocol.sock_req_cmd].lower() == InterProtocol.client_req_type_join_game \
                    and req_json[InterProtocol.room_id] not in Rooms:
                create_room_from_db(req_json[InterProtocol.room_id], req_json[InterProtocol.game_id])

            if req_json[InterProtocol.room_id] in Rooms:
                Rooms[req_json[InterProtocol.room_id]].process_player_cmd_request(player, req_json)
        else:
            # process_lobby_player_request(player, req_json)
            Lobby.process_player_request(player, req_json)

    except Exception as ex:
        Log.write_exception(ex)

# def update_round_stage(client_conn):
#     player = get_player_client_from_conn(client_conn)
#     round = player.get_game_round()
#     round.test_and_update_current_stage()


def get_player_client_from_conn(conn):
    if conn in Conn_Players:
        return Conn_Players[conn]
    else:
        return None

def remove_dead_connection():
    dead = []
    for p in Players:
        now = datetime.now()
        delta = now - Players[p].get_last_alive_time()
        if delta.total_seconds() > dead_connect_reserve_minutes * 60:
            dead.append((p, Players[p].get_socket_conn()))

    for item in dead:
        conn = item[1]
        userid = item[0]
        player = Players[userid]
        room = player.get_my_room()
        if room:
            room.remove_player(player)
        send_msg_to_client_connection(conn,"disconnected as dead connection")
        Players.pop(item[0])
        Conn_Players.pop(item[1])
        conn.close()

    Log.write_info("client number:" + str(len(Conn_Players)))
    start_timer_to_clear_dead_connection()

def get_rule_by_id(rule_id):
    if rule_id in __PlayRules:
        return __PlayRules[rule_id]
    else:
        return None

def process_player_select_action(conn, j_obj):
    player = get_player_client_from_conn(conn)
    round = player.get_game_round()
    act_param = None
    if "act-params" in j_obj:
        act_param = j_obj["act-params"]
    round.process_player_select_action(player, j_obj["act-id"], act_param)

# TODO create Room from database
def create_room_from_db(room_id, rule_id):
    game_rule = GameRules[rule_id]
    if isinstance(game_rule, GameRule_Majiang):
        room = Room_Majiang(room_id, game_rule)

    room.set_min_seated_player_num(3)
    room.set_max_seated_player_num(3)
    Rooms[room_id] = room

def process_client_disconnected(conn):
    player = get_player_client_from_conn(conn)
    if player:
        player.set_is_online(False)
        # remove_dead_connection(conn)
