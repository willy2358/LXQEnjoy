import json
import os
import threading

from Mains import Log, InterProtocol, Errors

from threading import Timer
from datetime import datetime
from Mains import CmdQueues

from Clients import Clients

from GRules.GRule import GRule
import Mains.Errors as Err

__comm_event = None
__cmds_dispatch_thread = None
__exit = False

ConfigRoot = ""

Conn_Players = {} #{connection, player}
# __Players = []
Players={}   #{userid:player}
Rooms = {}   #{roomid:room}
GameRules = {} #{ruleid:rule}

__Waiting_Players = {}
__PlayRules = {}

__game_rounds = []

__accessors = {}

config_dir = "configs"
config_dir_clients = "clients"
config_dir_rules = "rules"


SERVER_CMD_DEAL_BEGIN = "deal_begin"
SERVER_CMD_DEAL_FINISH = "deal_finish"

CLIENT_REQ_SELECT_ACTION = "sel-act"

cycle_minutes_check_dead = 10
dead_connect_reserve_minutes = 5
timer_clear_dead_connection = None

MAX_PLAYER_NUM_IN_ROOM = 8


def initialize(cmd_evt):
    global __comm_event
    __comm_event = cmd_evt

    load_rules()   # must before load_clients

    load_clients()

    start_cmds_dispatcher()

    start_timer_to_clear_dead_connection()

def exit_service():
    global __exit
    __exit = True

def start_cmds_dispatcher():
    global __cmds_dispatch_thread
    __cmds_dispatch_thread = threading.Thread(group=None, target=dispatch_clients_cmds)
    __cmds_dispatch_thread.setDaemon(True)
    __cmds_dispatch_thread.start()

def dispatch_clients_cmds():
    while not __exit:
        if __comm_event.is_set():
            conn, cmd = CmdQueues.get_cmd()
            if conn and cmd:
                dispatch_player_commands(conn, cmd)
        __comm_event.wait(0.2)
        if __exit:
            break
        conn, cmd = CmdQueues.get_cmd()
        # TODO consider whether event is thread safe
        __comm_event.clear()
        if conn and cmd:
            dispatch_player_commands(conn, cmd)

def start_timer_to_clear_dead_connection():
    global  timer_clear_dead_connection
    timeout = min(cycle_minutes_check_dead, dead_connect_reserve_minutes)
    timer_clear_dead_connection = Timer(timeout * 60, remove_dead_connection)
    timer_clear_dead_connection.start()

def load_clients():
    try:
        clientsDir = os.path.join(ConfigRoot, config_dir,  config_dir_clients)
        Clients.set_config_dir(clientsDir)
        if os.path.exists(clientsDir):
            Clients.reload()
        # Clients.start_watcher()
    except Exception as ex:
        Log.exception(ex)

def load_rules():
    try:
        rulesDir = os.path.join(ConfigRoot, config_dir, config_dir_rules)

        for (root, _, files) in os.walk(rulesDir):
            for f in files:
                if f.endswith(".xml"):
                    gRuleXml = os.path.join(root, f)
                    gf = GRule(gRuleXml)
                    if gf.load():
                        GameRules[gf.get_ruleid()] = gf
                    else:
                        Log.error("game config error:" + gRuleXml)

    except Exception as ex:
        Log.exception(ex)

def get_rule_by_id(ruleid):
    if ruleid in GameRules:
        return GameRules[ruleid]
    else:
        return None

def validate_req_packet(j_obj):
    if InterProtocol.user_id not in j_obj \
            or InterProtocol.client_id not in j_obj \
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

    if not validate_req_packet(j_obj):
        send_err_pack_to_client(conn, "invalid", Errors.invalid_request_parameter)
        return

    try:
        if j_obj[InterProtocol.cmd_type].lower() == InterProtocol.sock_req_cmd.lower():
            process_client_request(conn, j_obj)
    except Exception as ex:
        Log.exception(ex)

def send_pack_to_client(conn, pack):
    j_str = json.dumps(pack)
    msg = "LXQ<(:" + j_str + ":)>QXL"
    return send_msg_to_client(conn, msg)

def send_err_pack_to_client(clientConn, cmd, errCode):
    err_pack = InterProtocol.create_error_pack(cmd, errCode);
    err_str = json.dumps(err_pack)
    msg = "LXQ<(:" + err_str + ":)>QXL"
    send_msg_to_client(clientConn, msg)

def send_msg_to_client(conn, msg):
    try:
        conn.sendall(msg.encode(encoding="utf-8"))
        return True
    except Exception as ex:
        Log.exception(ex)
        return False

def send_welcome_to_new_connection(conn):
    welcome_msg = "welcome,just enjoy!"
    send_msg_to_client(conn, welcome_msg)

def process_register_player(conn, cmd, req_json):

    token = req_json[InterProtocol.authed_token]
    clientid = token[InterProtocol.client_id]
    if not Clients.is_client_valid(clientid, token):
        send_err_pack_to_client(conn, cmd, Errors.invalid_client_token)
        return
    client = Clients.get_client(clientid)
    userid = req_json[InterProtocol.user_id]
    err, player = client.register_player(userid)
    if err == Err.ok:
        # obj = {InterProtocol.user_id: player.get_userid(), InterProtocol.field_sock_token:player.get_token()}
        resp_pack = InterProtocol.create_success_resp_pack(cmd)
        send_pack_to_client(conn, resp_pack)
    else:
        send_err_pack_to_client(cmd, err)

def validate_client_player(conn, cmd, req_json):
    # token = req_json[InterProtocol.authed_token]
    # validate client
    clientid = req_json[InterProtocol.client_id]
    client = Clients.get_client(clientid)
    if not client:
        send_err_pack_to_client(conn, cmd, Errors.invalid_player_clientid)
        return False, None, None
    # validate user
    userid = req_json[InterProtocol.user_id]
    ret = client.is_player_registered(userid)
    if not ret:
        send_err_pack_to_client(conn, cmd, Errors.player_not_registered)
        return False, None, None

    return True, client, client.get_player_by_id(userid)

def process_player_request(conn, cmd, req_json):
    ret, client, player = validate_client_player(conn, cmd, req_json)
    if not ret:
        return

    if conn not in Conn_Players:
        Conn_Players[conn] = player
        player.set_sock_conn(conn)
        Log.info("client number:" + str(len(Conn_Players)))

    #     if player.get_socket_conn() != conn:
    #         if player.get_is_online():
    #             send_err_pack_to_client(conn, cmd, Errors.player_already_in_game)
    #             return
    #         else:
    #             player.update_connection(conn)
    #             return
    if player:
        if player.get_sock_conn() != conn:
            if player.get_is_online():
                send_err_pack_to_client(conn, cmd, Errors.player_already_in_game)
            else:
                player.update_connection(conn)
        player.update_last_alive()


    if client and player:
        client.process_player_request(player, cmd, req_json)

def process_client_request(conn, req_json):
    try:
        cmd = req_json[InterProtocol.sock_req_cmd]
        if cmd == InterProtocol.client_req_cmd_reg_player:
            process_register_player(conn, cmd, req_json)
        else:
            process_player_request(conn, cmd, req_json)

    except Exception as ex:
        Log.exception(ex)

# def is_room_for_inner_test(room_id):
#     sr_id = str(room_id)
#     return sr_id.startswith("LX")
#
# def get_room(cmd, room_id, game_id):
#     if room_id in Rooms:
#         return Rooms[room_id],Errors.ok
#
#     if cmd.lower() == InterProtocol.client_req_cmd_enter_room.lower():
#         if is_room_for_inner_test(room_id):
#             return create_room(room_id, game_id), Errors.ok
#         else:
#             if check_is_valid_room_no(room_id, game_id):
#                 return create_room(room_id, game_id), Errors.ok
#             else:
#                 return None, Errors.wrong_room_number
#     else:
#         return None, Errors.did_not_call_enter_room
#
# def create_inner_test_room(roomid, gameid):
#     game_rule = GameRules[gameid]
#     room = None
#     if isinstance(game_rule, GameRule_Majiang):
#         room = Room_Majiang(roomid, game_rule)
#
#     room.set_min_seated_player_num(game_rule.get_player_min_number())
#     room.set_max_seated_player_num(game_rule.get_player_max_number())
#     room.set_max_player_number(MAX_PLAYER_NUM_IN_ROOM)
#     Rooms[roomid] = room
#     return room
#
# def check_is_valid_room_no(roomid, gameid):
#
#     try:
#         dbConn = db.get_connection()
#         with dbConn.cursor() as cursor:
#             sql = " SELECT count(room_no) as rcount" \
#                   " FROM `room` " \
#                   " WHERE room_no=%s and gameid=%s"
#             cursor.execute(sql, (roomid, gameid))
#             result = cursor.fetchone()
#             if result["rcount"] < 1:
#                 return False
#             else:
#                 return True
#
#     except Exception as ex:
#         Log.write_exception(ex)
#         return False


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

    Log.info("client number:" + str(len(Conn_Players)))
    start_timer_to_clear_dead_connection()

def get_rule_by_id(rule_id):

    if rule_id in GameRules:
        return GameRules[rule_id]
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
# def create_room(room_id, rule_id):
#     game_rule = GameRules[rule_id]
#
#     room = None
#     if isinstance(game_rule, GameRule_Majiang):
#         room = Room_Majiang(room_id, game_rule)
#         room.set_min_seated_player_num(game_rule.get_player_min_number())
#         room.set_max_seated_player_num(game_rule.get_player_max_number())
#         room.set_max_player_number(MAX_PLAYER_NUM_IN_ROOM)
#     ret = True
#     if not is_room_for_inner_test(room_id):
#         ret = load_room_settings_from_db(room)
#
#     if ret:
#         Rooms[room_id] = room
#         return room
#     else:
#         return None


# def load_room_settings_from_db(room):
#     try:
#         dbConn = db.get_connection()
#         with dbConn.cursor() as cursor:
#             # Read a single record
#             sql = "SELECT `userid`, `room_no`,`gameid`,`round_num`,`ex_ip_cheat`,`ex_gps_cheat`,`fee_stuff_id`, " \
#                   " s1.`stuffname` as `fee_stuff_name`," \
#                   "`fee_amount_per_player`,`fee_creator_pay_all`,`stake_stuff_id`," \
#                   "s2.`stuffname` as `stake_stuff_name`,`stake_base_score`" \
#                   " FROM `room` as r, stuff as s1, stuff as s2 " \
#                   " WHERE room_no=%s and r.fee_stuff_id = s1.stuffid and r.stake_stuff_id = s2.stuffid"
#             cursor.execute(sql, (room.get_room_id()))
#             result = cursor.fetchone()
#             print(result)
#             room.set_round_number(result["round_num"])
#             room.set_fee_stuff(result["fee_stuff_id"], result["fee_stuff_name"])
#             room.set_stake_stuff(result["stake_stuff_id"], result["stake_stuff_name"])
#             return True
#     except Exception as ex:
#         return False

def process_client_disconnected(conn):
    player = get_player_client_from_conn(conn)
    if player:
        player.set_is_online(False)
        # remove_dead_connection(conn)
