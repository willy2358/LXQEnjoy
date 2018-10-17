import json
import Errors
import db
import os


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

from GRules.GRule import GRule
import Accessors

Conn_Players = {} #{connection, player}
# __Players = []
Players={}   #{userid:player}
Rooms = {}   #{roomid:room}
GameRules = {} #{gameid:rule}

__Waiting_Players = {}
__PlayRules = {}

__game_rounds = []

__accessors = {}


SERVER_CMD_DEAL_BEGIN = "deal_begin"  # 开始发牌
SERVER_CMD_DEAL_FINISH = "deal_finish"   # 结束发牌

CLIENT_REQ_SELECT_ACTION = "sel-act"

cycle_minutes_check_dead = 10
dead_connect_reserve_minutes = 5
timer_clear_dead_connection = None

MAX_PLAYER_NUM_IN_ROOM = 8


def initialize():
    load_accessors()
    load_games()
    start_timer_to_clear_dead_connection()

def start_timer_to_clear_dead_connection():
    timeout = min(cycle_minutes_check_dead, dead_connect_reserve_minutes)
    timer_clear_dead_connection = Timer(timeout * 60, remove_dead_connection)
    timer_clear_dead_connection.start()

def load_accessors():
    try:
        configDir = os.path.join(os.getcwd(), "accessors")
        Accessors.set_config_dir(configDir)
        if os.path.exists(configDir):
            Accessors.reload()
        Accessors.start_watcher()
    except Exception as ex:
        Log.write_exception(ex)

def load_games():
    try:
        prefile = os.path.join(os.getcwd(), "gconfigs")
        for (root, _, files) in os.walk(prefile):
            for f in files:
                if f.endswith(".xml"):
                    gRuleXml = os.path.join(root, f)
                    gf = GRule(gRuleXml)
                    if gf.load():
                        GameRules[gf.get_gameid()] = gf
                    else:
                        Log.write_error("game config error:" + gRuleXml)

    except Exception as ex:
        Log.write_exception(ex)

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
        print(ex)
        send_err_pack_to_client(conn, 'unknown', Errors.invalid_packet_format)
        return

    if not validate_player(j_obj):
        send_err_pack_to_client(conn, "invalid", Errors.invalid_request_parameter)
        return

    try:
        if j_obj[InterProtocol.cmd_type].lower() == InterProtocol.sock_req_cmd.lower():
            process_client_request(conn, j_obj)
    except Exception as ex:
        Log.write_exception(ex)


def send_msg_to_client(conn, msg):

    try:
        conn.sendall(msg.encode(encoding="utf-8"))
    except Exception as ex:
        Log.write_exception(ex)

def send_err_pack_to_client(clientConn, cmd, errCode):
    err_pack = InterProtocol.create_error_pack(cmd, errCode);
    err_str = json.dumps(err_pack)
    send_msg_to_client(clientConn, err_str)

def send_welcome_to_new_connection(conn):
    welcome_msg = "welcome,just enjoy!"
    send_msg_to_client(conn, welcome_msg)

def process_register_player(conn, req_json):
    pass

def process_create_room(conn, req_json):
    pass

def process_player_request(conn, req_json):
    cmd = req_json[InterProtocol.sock_req_cmd]
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
            if player.get_is_online():
                send_err_pack_to_client(conn, cmd, Errors.player_already_in_game)
                return
            else:
                player.update_connection(conn)
                return
    if player:
        player.update_last_alive()

    roomid = str(req_json[InterProtocol.room_id])
    if not roomid or roomid == "-1" or roomid == "0" or roomid.lower() == "null" or roomid.lower() == "none":
        Lobby.process_player_request(player, req_json)
    else:
        room, err = get_room(cmd, roomid, req_json[InterProtocol.game_id])
        if not room:
            send_err_pack_to_client(conn, cmd, err)
        else:
            room.process_player_cmd_request(player, req_json)

def process_client_request(conn, req_json):
    try:
        player = None
        cmd = req_json[InterProtocol.sock_req_cmd]
        if cmd == InterProtocol.client_req_cmd_reg_player:
            process_register_player(conn, req_json)
        elif cmd == InterProtocol.client_req_cmd_new_room:
            process_create_room(conn, req_json)
        else:
            process_player_request(conn, req_json)

    except Exception as ex:
        Log.write_exception(ex)

def is_room_for_inner_test(room_id):
    sr_id = str(room_id)
    return sr_id.startswith("LX")

def get_room(cmd, room_id, game_id):
    if room_id in Rooms:
        return Rooms[room_id],Errors.ok

    if cmd.lower() == InterProtocol.client_req_cmd_enter_room.lower():
        if is_room_for_inner_test(room_id):
            return create_room(room_id, game_id), Errors.ok
        else:
            if check_is_valid_room_no(room_id, game_id):
                return create_room(room_id, game_id), Errors.ok
            else:
                return None, Errors.wrong_room_number
    else:
        return None, Errors.did_not_call_enter_room

def create_inner_test_room(roomid, gameid):
    game_rule = GameRules[gameid]
    room = None
    if isinstance(game_rule, GameRule_Majiang):
        room = Room_Majiang(roomid, game_rule)

    room.set_min_seated_player_num(game_rule.get_player_min_number())
    room.set_max_seated_player_num(game_rule.get_player_max_number())
    room.set_max_player_number(MAX_PLAYER_NUM_IN_ROOM)
    Rooms[roomid] = room
    return room

def check_is_valid_room_no(roomid, gameid):

    try:
        dbConn = db.get_connection()
        with dbConn.cursor() as cursor:
            sql = " SELECT count(room_no) as rcount" \
                  " FROM `room` " \
                  " WHERE room_no=%s and gameid=%s"
            cursor.execute(sql, (roomid, gameid))
            result = cursor.fetchone()
            if result["rcount"] < 1:
                return False
            else:
                return True

    except Exception as ex:
        Log.write_exception(ex)
        return False


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
        send_msg_to_client(conn, "disconnected as dead connection")
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
def create_room(room_id, rule_id):
    game_rule = GameRules[rule_id]

    room = None
    if isinstance(game_rule, GameRule_Majiang):
        room = Room_Majiang(room_id, game_rule)
        room.set_min_seated_player_num(game_rule.get_player_min_number())
        room.set_max_seated_player_num(game_rule.get_player_max_number())
        room.set_max_player_number(MAX_PLAYER_NUM_IN_ROOM)
    ret = True
    if not is_room_for_inner_test(room_id):
        ret = load_room_settings_from_db(room)

    if ret:
        Rooms[room_id] = room
        return room
    else:
        return None


def load_room_settings_from_db(room):
    try:
        dbConn = db.get_connection()
        with dbConn.cursor() as cursor:
            # Read a single record
            sql = "SELECT `userid`, `room_no`,`gameid`,`round_num`,`ex_ip_cheat`,`ex_gps_cheat`,`fee_stuff_id`, " \
                  " s1.`stuffname` as `fee_stuff_name`," \
                  "`fee_amount_per_player`,`fee_creator_pay_all`,`stake_stuff_id`," \
                  "s2.`stuffname` as `stake_stuff_name`,`stake_base_score`" \
                  " FROM `room` as r, stuff as s1, stuff as s2 " \
                  " WHERE room_no=%s and r.fee_stuff_id = s1.stuffid and r.stake_stuff_id = s2.stuffid"
            cursor.execute(sql, (room.get_room_id()))
            result = cursor.fetchone()
            print(result)
            room.set_round_number(result["round_num"])
            room.set_fee_stuff(result["fee_stuff_id"], result["fee_stuff_name"])
            room.set_stake_stuff(result["stake_stuff_id"], result["stake_stuff_name"])
            return True
    except Exception as ex:
        return False

def process_client_disconnected(conn):
    player = get_player_client_from_conn(conn)
    if player:
        player.set_is_online(False)
        # remove_dead_connection(conn)
