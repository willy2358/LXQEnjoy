
SOCK_REQ_CMD = "sockreq"
CMD_TYPE = "cmdtype"


CLIENT_REQ_JOIN_GAME = "join-game" # 开始游戏
CLIENT_REQ_SELECT_ACTION = "sel-act"
CLIENT_REQ_RECONNECT = "reconnect" #断线重连

ROOM_ID = "roomid"
USER_ID = "userid"
GAME_ID = "gameid"

majiang_player_act_peng = "peng"
majiang_player_act_hu = "hu"
majiang_player_act_eat = "chi"
majiang_player_act_zimo = "zi mo"
majiang_player_act_fetch_card = "mo pai"
majiang_player_act_pass = "guo"

min_room_id = 10   #valid room id should > 10


def create_deal_cards_json_packet(player, cards):
    pass


def create_cmd_options_json_packet(player, cmd_options):
    pass


def create_error_json_packet(player, err_msg):
    pass
