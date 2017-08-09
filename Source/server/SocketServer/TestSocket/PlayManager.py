import json
import random

import PlayRule
import PlayerClient
import Utils
from CallAction import CallAction
from PlayRound import PlayRound

__Players = []
__Waiting_Players = {}
__PlayRules = {}

__game_rounds = []


SERVER_CMD_DEAL_BEGIN = "deal_begin"  # 开始发牌
SERVER_CMD_DEAL_FINISH = "deal_finish"   # 结束发牌
SERVER_CMD_DEAL_CARD = "deal_card"   # 发牌
SERVER_CMD_CALL_ACTIONS = "call_actions"  # 叫牌

CLIENT_CMD_CARDS_SORTED = "cards_sorted"  # 理牌完成
CLIENT_CMD_BEGIN_PLAY = "join_game" # 开始游戏
CLIENT_CMD_PLAY_CARD = "play_card"


# command:开始发牌: deal_begin
# command:结束发牌: deal_finish
# commands 发牌: deal#{"deal":card}. ex: deal#{"deal":"poker_1_h"}

def init_play_rules():
    rule_id = "1212"
    rule = PlayRule.PlayRule(rule_id)
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

    stages = ["server_group_players",
              "server_deal_cards",
              "client_sort_cards",
              "server_ask_player_call",
              "client_call",
              "server_publish_banker"
              "client_play_cards"
              "server_publish_winner"
              "server_update_players_score"
              ]
    a1 = CallAction("1", "Call")
    a11 = a1.add_follow_up_action(CallAction("1_1", "Rob"))
    a12 = a1.add_follow_up_action(CallAction("1_2", "Not Rob"))

    a111 = a11.add_follow_up_action(CallAction("1_1_1", "Rob"))
    a112 = a11.add_follow_up_action(CallAction("1_1_2", "Not rob"))

    a121 = a12.add_follow_up_action(CallAction("1_2_1", "Rob"))
    a122 = a12.add_follow_up_action(CallAction("1_2_2", "Not rob"))

    a2 = CallAction("2", "Not Call")
    a21 = a2.add_follow_up_action(CallAction("2_1", "Call"))
    a22 = a2.add_follow_up_action(CallAction("2_2","Not call"))

    a211 = a21.add_follow_up_action(CallAction("2_1_1", "Rob"))
    a212 = a21.add_follow_up_action(CallAction("2_1_2", "Not rob"))

    a221 = a22.add_follow_up_action(CallAction("2_2_1", "Call"))
    a222 = a22.add_follow_up_action(CallAction("2_2_2", "end_game"))
    rule.add_call_action(a1)
    rule.add_call_action(a2)

    rule.set_stages(stages)
    __PlayRules[rule_id] = rule


def create_command_packet(command, command_data):
    return command + "#" + command_data


def add_player_client(conn):
    player = PlayerClient.PlayerClient(conn)
    __Players.append(player)
    print('player clients:' + str(len(__Players)))
    print('new player:' + str(conn))


def begin_player_inter_actions(players):
    pass


def record_player_cards_sorted(conn):
    client = get_player_client_from_conn(conn)
    client.set_cards_arranged()
    partners = client.get_play_partners()
    all_arranged = True
    for p in partners:
        if not p.is_cards_sorted():
            all_arranged = False
            break
    if all_arranged:
        all_players = [client] + partners
        begin_player_inter_actions(all_players)


def dispatch_player_commands(conn, comm_text):
    parts = comm_text.split('#')
    if len(parts) == 2:
        if parts[0].lower() == CLIENT_CMD_BEGIN_PLAY.lower() :
            process_command_join_game(conn, parts[1])
        if parts[0].lower() == CLIENT_CMD_PLAY_CARD.lower() :
            process_command_play_card(conn, parts[1])
    elif len(parts) == 1:
        if parts[0].lower() == "play_leave":
            process_command_play_leave(conn)
        if parts[0].lower() == CLIENT_CMD_CARDS_SORTED.lower():
            player = get_player_client_from_conn(conn)
            player.process_cards_sorted()


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
    r = PlayRound(get_rule_by_id(rule_id))
    __game_rounds.append(r)
    return r


# command samples: join_game#"{\"rule_id\":\"1212\"}"
def process_command_join_game(conn, command_text):
    try:
        j_obj = json.loads(command_text)
        if isinstance(j_obj, type(" ")):
            j_obj = json.loads(j_obj)
        rule_id = j_obj["rule_id"]
        play_round = get_available_game_round(rule_id)
        play_round.add_player(get_player_client_from_conn(conn))
        # if rule_id not in __Waiting_Players:
        #     __Waiting_Players[rule_id] = []
        # __Waiting_Players[rule_id].append(get_player_client_from_conn(conn))
        # update_players_waiting_state()
    except Exception as ex:
        print("ex")


def update_players_waiting_state():
    for item in __Waiting_Players:
        play_rule = __PlayRules[item]
        rule_id = play_rule.get_rule_id()
        min_player_num = play_rule.get_player_min_number()
        if len(__Waiting_Players[item]) >= min_player_num:
            players = get_players_of_waiting_rule_id(rule_id, min_player_num)
            for p in players:
                p.set_playing_rule_id(rule_id)
                p.set_player_partners(players)
            remove_waiting_players(rule_id, players)
            begin_new_deal(rule_id, players)


def remove_waiting_players(rule_id, players):
    for p in players:
        __Waiting_Players[rule_id].remove(p)


def begin_new_deal(rule_id, players):
    rule = __PlayRules[rule_id]
    cards = rule.get_cards()
    cards_b = cards[:]
    remain_cards = random.sample(cards_b, rule.get_cards_number_not_deal())
    Utils.list_remove_parts(cards_b, remain_cards)
    player_num = len(players)
    for p in players:
        p.begin_new_deal()

    while len(cards_b) > 0:
        cards_one_deal = random.sample(cards_b, player_num)
        for j in range(player_num):
            players[j].deal_one_card(cards_one_deal[j])
        Utils.list_remove_parts(cards_b, cards_one_deal)

    for p in players:
        p.finish_new_deal()


def get_players_of_waiting_rule_id(rule_id, num):
    players = []
    for i in range(0,num):
        players.append(__Waiting_Players[rule_id][i])

    return players


def process_command_play_card(conn, command_text):
    pass


def process_command_play_leave(conn):
    pass