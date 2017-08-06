import json
import random

import PlayRule
import PlayerClient
import Utils

__Players = []
__Waiting_Players = {}
__PlayRules = {}


def init_play_rules():
    rule_id = "1212"
    rule = PlayRule.PlayRule(rule_id)
    rule.set_player_min_number(3)
    rule.set_player_mzx_number(3)
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
    __PlayRules[rule_id] = rule


def add_player_client(conn):
    player = PlayerClient.PlayerClient(conn)
    __Players.append(player)
    print('player clients:' + str(len(__Players)))
    print('new player:' + str(conn))


def dispatch_player_commands(conn, comm_text):
    parts = comm_text.split('#')
    if len(parts) == 2:
        if parts[0].lower() == "play_rule":
            process_command_play_rule(conn, parts[1])
        if parts[0].lower() == "play_card":
            process_command_play_card(conn, parts[1])
        if parts[0].lower() == "play_leave":
            process_command_play_leave(conn)


def get_player_client_from_conn(conn):
    for c in __Players:
        if c.get_socket_conn() == conn:
            return c

    return None


# command samples: play_rule#"{\"rule_id\":\"1212\"}"
def process_command_play_rule(conn, command_text):
    try:
        j_obj = json.loads(command_text)
        if (isinstance(j_obj, type(" "))):
            j_obj = json.loads(j_obj)
        rule_id = j_obj["rule_id"]
        if rule_id not in __Waiting_Players:
            __Waiting_Players[rule_id] = []
        __Waiting_Players[rule_id].append(get_player_client_from_conn(conn))
        update_players_waiting_state()
    except Exception as ex:
        print("ex")


def update_players_waiting_state():
    for item in __Waiting_Players:
        play_rule = __PlayRules[item]
        rule_id = play_rule.get_play_rule_id()
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
    while len(cards_b) > 0:
        cards_one_deal = random.sample(cards_b, player_num)
        for j in range(player_num):
            players[j].deal_one_card(cards_one_deal[j])
        Utils.list_remove_parts(cards_b, cards_one_deal)


def get_players_of_waiting_rule_id(rule_id, num):
    players = []
    for i in range(0,num):
        players.append(__Waiting_Players[rule_id][i])

    return players


def process_command_play_card(conn, command_text):
    pass


def process_command_play_leave(conn):
    pass