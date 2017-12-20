
cmd_type = "cmdtype"
sock_req_cmd = "sockreq"
sock_resp = "sockresp"
sock_result = "result"
sock_result_error = "ERROR"
sock_result_ok = "OK"
sock_error_message = "errmsg"



client_req_type_join_game = "join-game"   # 开始游戏
client_req_select_action = "sel-act"
client_req_type_reconnect = "reconnect"   # 断线重连
client_req_type_exe_cmd = "exe-cmd"
client_req_exe_cmd = "cmd"
client_req_cmd_param = "cmd-data"
client_req_robot_play = "robot-play"

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


cmd_data_cards = "cards"


room_id = "roomid"
user_id = "userid"
game_id = "gameid"


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

def create_play_cards_packet(player, cards):
    l_cards = []
    if isinstance(cards, type([])):
        l_cards = cards
    else:
        l_cards.append(cards)

    state = player_state_normal if player.get_is_online() else player_state_offline
    if player.get_is_robot_play():
        state += "|" + player_state_robot_play

    packet = {
        cmd_type: server_cmd_type_push,
        server_cmd_type_push: server_push_play_cards,
        user_id: player.get_user_id(),
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
            user_id:player.get_user_id()
        }
        return packet

def create_cmd_options_json_packet(player, cmd_options, def_cmd=None, resp_timeout=-1):
    opts = []
    for v in cmd_options:
        opts.append({client_req_exe_cmd:v.get_cmd(),server_push_cmd_param:v.get_cmd_param()})

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


def create_error_json_packet(player, err_msg):
    pass


def create_publish_bank_player_json_packet(bank_player):
    packet = {cmd_type: server_cmd_type_push,
           server_cmd_type_push: server_push_new_banker,
           user_id: bank_player.get_user_id()
           }
    return packet


def create_winners_losers_json_packet(winners, losers):
    ws = []
    for p in winners:
        ws.append({user_id:p.get_user_id(), server_push_score:p.get_won_score()})
    ls = []
    for p in losers:
        ls.append({user_id:p.get_user_id(),server_push_score:p.get_won_score()})
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

def create_players_total_score_in_room(room):
    scores = []
    for p in room.get_seated_players():
        scores.append({user_id: p.get_user_id(), server_push_score: room.get_player_total_score(p)})

    packet = {
        cmd_type: server_cmd_type_push,
        server_cmd_type_push: server_push_scores,
        server_push_scores: scores
    }
    return packet


def create_players_total_score_in_round(game_round):
    scores = []
    for p in game_round.get_players():
        scores.append({user_id: p.get_user_id(), server_push_score: p.get_won_score()})

    packet = {
        cmd_type: server_cmd_type_push,
        server_cmd_type_push: server_push_scores,
        server_push_scores: scores
    }
    return packet