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
from GameStages.DiceBanker import DiceBanker
from GameStages.GroupPlayers import GroupPlayers
from GameStages.PlayCards import PlayCards
from GameStages.PublishScores import PublishScores
from GameStages.TeamPlayers import TeamPlayers
from GameStages.TellWinner import TellWinner
from Rooms.Room import Room
from Rooms import Room_Majiang

__Players = []
Players={}   #{userid:player}
Rooms = {}   #{roomid:room}
GameRules = {} #{ruleid:rule}
__Waiting_Players = {}
__PlayRules = {}

__game_rounds = []


SERVER_CMD_DEAL_BEGIN = "deal_begin"  # 开始发牌
SERVER_CMD_DEAL_FINISH = "deal_finish"   # 结束发牌

CLIENT_REQ_JOIN_GAME = "join-game" # 开始游戏
CLIENT_REQ_SELECT_ACTION = "sel-act"
CLIENT_REQ_RECONNECT = "reconnect" #断线重连


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

    stage = DiceBanker(rule)
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
        if j_obj["req"] == CLIENT_REQ_JOIN_GAME.lower():
            process_req_join_game(conn, j_obj)
        if j_obj["req"] == CLIENT_REQ_SELECT_ACTION.lower():
            process_player_select_action(conn, j_obj)
        if j_obj["cmdtype"] == "sockreq":
            process_client_request(conn, j_obj)
    except Exception as ex:
        print(ex)


def process_client_request(conn, req_json):
    try:

        if req_json["sockreq"] == CLIENT_REQ_JOIN_GAME.lower():
            process_req_join_game(req_json)
        if req_json["sock"] == CLIENT_REQ_RECONNECT.lower():
            pass

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
    act_param = None
    if "act-params" in j_obj:
        act_param = j_obj["act-params"]
    round.process_player_select_action(player, j_obj["act-id"], act_param)


# command samples: {"cmdtype":"sockreq","sockreq":"join-game","userid":123456,	"roomid":123333,"gameid":123432}
def process_req_join_game(conn, req_json):
    try:

        user_id = req_json["userid"]

        player = None
        if user_id not in Players:
            player = PlayerClient(conn, user_id)
            Players[user_id] = player
        else:
            player = Players[user_id]

        if "roomid" not in req_json or req_json["roomid"] < 10:
            process_join_lobby_game(player, req_json["gameid"])
        else:
            process_join_room_game(player, req_json["gameid"], req_json["roomid"])

    except Exception as ex:
        Log.write_exception(ex)


def process_join_lobby_game(player, rule_id):
    if None != player.get_game_round():
            player.send_error_message("Already in a game")
    else:
        play_round = get_available_game_round(rule_id)
        play_round.add_player(player)
        #update_round_stage(player.get_socket_conn())
        player.send_success_messsage(CLIENT_REQ_JOIN_GAME)
        play_round.test_and_update_current_stage()


def process_join_room_game(player, game_rule_id, room_id):
    try:
        if room_id not in Rooms:
            create_room_from_db(room_id, game_rule_id)

        if room_id not in Rooms:
            error = "failed to create room, room_id:" + str(room_id)
            player.send_error_message(CLIENT_REQ_JOIN_GAME, error)
            return
        room = Rooms[room_id]
        if not room.can_new_player_seated():
            player.send_error_message(CLIENT_REQ_JOIN_GAME, "Room is full")
            return
        if room.is_player_in(player):
            player.send_error_message(CLIENT_REQ_JOIN_GAME, "Already in room")
            return
        room.add_seated_player(player)
        player.send_success_message(CLIENT_REQ_JOIN_GAME)
        room.test_update_room_state()
    except Exception as ex:
        print(ex)


# TODO create Room from database
def create_room_from_db(room_id, rule_id):
    game_rule = GameRules[rule_id]
    if isinstance(game_rule, MajiangGameRule):
        room = Room_Majiang(room_id, game_rule)

    room.set_min_seated_player_num(3)
    room.set_max_seated_player_num(3)
    Rooms[room_id] = room

