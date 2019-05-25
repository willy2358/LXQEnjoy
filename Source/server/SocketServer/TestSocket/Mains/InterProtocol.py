from Mains import Errors

cmd_type = "cmdtype"
sock_req_cmd = "sockreq"
sock_resp = "sockresp"
sock_result = "result"
sock_result_error = "ERROR"
sock_result_ok = "OK"
sock_error_message = "errmsg"
sock_error_code = "errcode"
sock_result_data = "result-data"

resp_players = "players"
resp_seated_players = "seated-players"
resp_room = "room"
resp_seats_ids = "seats"
resp_player = "player"

client_req_cmd_reg_player = "reg-player"  # register player
client_req_cmd_new_room = "new-room"      # create a new room
client_req_cmd_join_game = "join-game"   # 加入游戏
client_req_cmd_leave_game = "leave-game" #离开游戏
client_req_select_action = "sel-act"
client_req_type_reconnect = "reconnect"   # 断线重连
client_req_type_exe_cmd = "exe-cmd"
client_req_get_cards = "get-cards"     #取得当前可活动牌列表


client_req_exe_cmd = "cmd"
client_req_cmd_param = "cmd-param"
client_req_robot_play = "robot-play"
client_req_cmd_new_closet = "new-closet"
client_req_cmd_enter_room = "enter-room"
client_req_cmd_leave_room = "leave-room"
client_req_play_cards = "play-cards"

field_closets = "closets"
field_closetid = "closetid"
field_expire = "expire"
field_gameid = "gameid"

field_roomtoken = "roomtoken"
field_players = "players"

field_salt = "salt"

field_seatid = "seatid"


field_signature = "signature"


field_sock_token="sock-token"

field_token = "token"




player_auth_token = "user_token"

server_cmd_type_push = "sockpush"
server_push_new_banker = "new-banker"
server_push_deal_cards = "deal-cards"
server_push_cmd_opts = "cmd-opts"
server_push_def_cmd = "def-cmd"
server_push_cmd_param = "cmd-param"
server_push_cmd_resp_timeout = "resp-timeout"
server_push_game_end = "game-end"
server_push_winners = "winners"
server_push_losers = "losers"
server_push_player_exed_cmd = "exed-cmd"
server_push_scores = "scores"
server_push_score = "score"
server_push_game_status = "game-status"
server_push_status_data = "status-data"
server_push_game_players = "game-players"
server_push_players = "players"
server_push_play_cards = "play-cards"
server_push_cards_state = "cards-state"
server_push_active_cards = "active-cards"
server_push_freezed_cards = "frozen-cards"
server_push_shown_card_groups = "shown-cards-groups"
server_push_private_cards_count = "private-cards-count"
server_push_pending_player = "pending-player"
server_push_pub_msg = "pub-msg"
server_push_round_status = "round-status"
server_push_player_status = "player-status"

pack_field_msg = "msg"
pack_field_silent="silent"
pack_field_cmd_alias = "cmd_alias"

cmd_data_cards = "cards"

room_id = "roomid"
user_id = "userid"
game_id = "gameid"
seat_id = "seatid"
client_id = "clientid"  #机构id
authed_token = "token"

player_state = "player-state"
player_state_normal = "normal"
player_state_offline = "offline"
player_state_robot_play = "robot-play"

majiang_player_act_gang = "gang"
majiang_player_act_peng = "peng"
majiang_player_act_hu = "hu"
majiang_player_act_chi = "chi"
majiang_player_act_zimo = "zi mo"
majiang_player_act_mopai = "mo pai"
majiang_player_act_pass = "guo"
majiang_player_act_play_card = "play-cards"

# the cmd with less index has the higher priority. that is  majiang_player_act_zimo has the highest priority.
majiang_acts_priorities = [majiang_player_act_zimo, majiang_player_act_hu,
                           majiang_player_act_gang, majiang_player_act_peng,
                           majiang_player_act_chi, majiang_player_act_mopai,
                           majiang_player_act_play_card, majiang_player_act_pass ]

min_room_id = 10   # valid room id should > 10

def create_player_cards_data_pack(player):
    packet = {
        cmd_type: sock_resp,
        sock_resp: client_req_get_cards,
        sock_result: sock_result_ok,
        cmd_data_cards: player.get_free_cards()
    }

    return packet

def create_success_resp_data_pack(cmd, dataName, dataObj):
    packet = {
        cmd_type: sock_resp,
        sock_resp: cmd,
        sock_result: sock_result_ok,
        sock_result_data: dataName
    }

    if dataName and dataObj:
        packet[dataName] = dataObj

    return packet

def create_success_resp_pack(cmd):
    packet = {
        cmd_type: sock_resp,
        sock_resp: cmd,
        sock_result: sock_result_ok,
        sock_result_data:""
    }

    return packet


def create_cards_state_packet(player, isForOwn = True):
    packet = {
        cmd_type: server_cmd_type_push,
        server_cmd_type_push: server_push_cards_state,
        user_id: player.get_userid(),
        server_push_private_cards_count:player.get_private_cards_count(),
        server_push_active_cards: player.get_active_cards() if isForOwn else [],
        server_push_freezed_cards: player.get_frozen_cards() if isForOwn else [],
        server_push_shown_card_groups:player.get_shown_card_groups()
    }

    return packet

def create_pending_player_packet(player):
    packet = {
        cmd_type: server_cmd_type_push,
        server_cmd_type_push: server_push_pending_player,
        user_id: player.get_userid()
    }

    return packet

def create_msg_packet(msg):
    packet = {
        cmd_type: server_cmd_type_push,
        server_cmd_type_push: server_push_pub_msg,
        pack_field_msg: msg
    }
    return packet

def create_play_cards_packet(player, cards, cmd_alias = server_push_play_cards):
    l_cards = []
    if isinstance(cards, list):
        l_cards = cards
    else:
        l_cards.append(cards)

    state = player_state_normal if player.get_is_online() else player_state_offline
    if player.get_is_robot_play():
        state += "|" + player_state_robot_play

    packet = {
        cmd_type: server_cmd_type_push,
        server_cmd_type_push: server_push_play_cards,
        pack_field_cmd_alias: cmd_alias,
        user_id: player.get_userid(),
        cmd_data_cards: l_cards,
        player_state:state
    }
    return packet

def create_game_status_packet(status, status_data = None):
    packet = {
        cmd_type: server_cmd_type_push,
        server_cmd_type_push: server_push_game_status,
        server_push_game_status: status,
        server_push_status_data:status_data
    }
    return packet

# def create_round_status_packet(status_data):


def create_game_players_packet(players):
    packet = {
        cmd_type: server_cmd_type_push,
        server_cmd_type_push:server_push_game_players,
        server_push_players:players,
    }

    return packet

def create_deal_cards_json_packet(player, cards):
    packet = {
        cmd_type: server_cmd_type_push,
        server_cmd_type_push: server_push_deal_cards,
        cmd_data_cards: cards
    }
    return packet

def create_player_exed_cmd_json_packet(player, cmd, cmd_data):

    if cmd == server_push_play_cards:
        return create_play_cards_packet(player, cmd_data)
    else:
        packet = {
            cmd_type: server_cmd_type_push,
            server_cmd_type_push: server_push_player_exed_cmd,
            server_push_player_exed_cmd: cmd,
            server_push_cmd_param:cmd_data,
            user_id:player.get_userid()
        }
        return packet

def create_cmd_options_json_packet(player, cmd_options, def_cmd=None, resp_timeout=-1):
    opts = []
    for v in cmd_options:
        opts.append({client_req_exe_cmd:v.get_cmd(),server_push_cmd_param:v.get_cmd_param(), pack_field_silent:v.is_silent()})

    packet = {
        cmd_type: server_cmd_type_push,
        server_cmd_type_push: server_push_cmd_opts,
        server_push_cmd_opts:opts,
        server_push_cmd_resp_timeout:resp_timeout
    }
    if def_cmd:
        packet[server_push_def_cmd] = {client_req_exe_cmd:def_cmd.get_cmd(),
                                       server_push_cmd_param:def_cmd.get_cmd_param()}

    return packet


# def create_error_json_packet(player, err_msg):
#     pass

def create_error_pack(req_cmd, errCode, errArg=None):
    pack = {
        cmd_type: sock_resp,
        sock_resp:req_cmd,
        sock_result:sock_result_error,
        sock_error_code:errCode,
        sock_error_message: Errors.Errors[errCode] if not errArg else Errors.Errors[errCode].format(errArg)
    }

    return pack


def create_publish_bank_player_json_packet(bank_player):
    packet = {cmd_type: server_cmd_type_push,
           server_cmd_type_push: server_push_new_banker,
           user_id: bank_player.get_userid()
           }
    return packet


def create_winners_losers_json_packet(winners, losers):
    ws = []
    for p in winners:
        ws.append({user_id:p.get_userid(), server_push_score:p.get_won_score()})
    ls = []
    for p in losers:
        ls.append({user_id:p.get_userid(), server_push_score:p.get_won_score()})
    packet = {
        cmd_type: server_cmd_type_push,
        server_cmd_type_push: server_push_game_end,
        server_push_winners:ws,
        server_push_losers:ls
    }
    return packet

def create_request_error_packet(player_req_cmd):
    packet = {
        cmd_type: sock_resp,
        sock_resp: player_req_cmd,
        sock_result: sock_result_error,
        sock_error_message: "invalid request"
    }
    return packet

def create_closet_players_acc_score_packet(closet):
    scores = []
    for p in closet.get_players():
        scores.append({user_id: p.get_userid(), server_push_score: closet.get_player_acc_score(p)})

    packet = {
        cmd_type: server_cmd_type_push,
        server_cmd_type_push: server_push_scores,
        server_push_scores: scores
    }
    return packet


def create_players_total_score_in_round(game_round):
    scores = []
    for p in game_round.get_players():
        scores.append({user_id: p.get_userid(), server_push_score: p.get_won_score()})

    packet = {
        cmd_type: server_cmd_type_push,
        server_cmd_type_push: server_push_scores,
        server_push_scores: scores
    }
    return packet