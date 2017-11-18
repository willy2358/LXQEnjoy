
sock_req_cmd = "sockreq"
cmd_type = "cmdtype"


client_req_join_game = "join-game"   # 开始游戏
client_req_select_action = "sel-act"
client_req_reconnect = "reconnect"   # 断线重连
client_req_exe_cmd = "exe-cmd"

room_id = "roomid"
user_id = "userid"
game_id = "gameid"

majiang_player_act_gang = "gang"
majiang_player_act_peng = "peng"
majiang_player_act_hu = "hu"
majiang_player_act_eat = "chi"
majiang_player_act_zimo = "zi mo"
majiang_player_act_new_card = "mo pai"
majiang_player_act_pass = "guo"

min_room_id = 10   # valid room id should > 10


def create_deal_cards_json_packet(player, cards):
    pass


def create_cmd_options_json_packet(player, cmd_options):
    pass


def create_error_json_packet(player, err_msg):
    pass
